
function getInputStrings(){
    var content = editor.getValue();
    console.log(String(content).trim())
}

function clearConsole(){
    document.getElementById('console').innerHTML = ""
}

function decorateView(loaderId, blockId, callback, result){
    return new Promise((resolve, reject)=>{
        var lexLoader = document.getElementById(loaderId)
        lexLoader.style.display = 'block'

        setTimeout(function(){
            callback()
            var lex_block = document.getElementById(blockId)
            lex_block.classList.remove(['bg-light'])
            lex_block.classList.add(['bg-'+result])
            lexLoader.style.display = 'none'
            resolve()
        }, 2000)
    })
}

function clearBlocks(){
    var lb = document.getElementById('lex_block')
    lb.classList.remove(['bg-success'])
    lb.classList.remove(['bg-danger'])
    lb.classList.add(['bg-light'])
    var syn = document.getElementById('syn_block')
    syn.classList.remove(['bg-success'])
    syn.classList.remove(['bg-danger'])
    syn.classList.add(['bg-light'])
    var opt = document.getElementById('opt_block')
    opt.classList.remove(['bg-success'])
    opt.classList.remove(['bg-danger'])
    opt.classList.add(['bg-light'])
    var gen = document.getElementById('gen_block')
    gen.classList.remove(['bg-success'])
    gen.classList.remove(['bg-danger'])
    gen.classList.add(['bg-light'])
}

function runCompiler(){
    clearBlocks()
    var lexLoader = document.getElementById('lex_loader')
    lexLoader.style.display = 'block'

    var content = String(editor.getValue()).trim();
    
    sendRequest(content).then((data)=>{
        var display = document.getElementById('console')
        display.appendChild(document.createElement('br'))
        
        //Lexer Results
        if(data.lexerResult.error != 'None'){
            function modifier(){
                var b = document.createElement('b')
                b.innerText = data.lexerResult.error
                b.classList.add(['text-danger'])
                display.appendChild(b)
            }
            decorateView('lex_loader', 'lex_block', modifier, 'danger').then(()=>{})
        }
        if(data.lexerResult.tokens != 'Tokens None'){
            function modifier(){
                var b = document.createElement('b')
                b.innerText = `----> ${data.lexerResult.tokens}`
                b.classList.add(['text-success'])
                display.appendChild(b)
            }

            decorateView('lex_loader', 'lex_block', modifier, 'success').then(()=>{
                display.appendChild(document.createElement('br'))

                //Parser Results
                if(data.parserResult.error != 'None'){
                    function modifier(){
                        var b = document.createElement('b')
                        b.innerText = data.parserResult.error
                        b.classList.add(['text-danger'])
                        display.appendChild(b)
                    }
                    decorateView('syn_loader', 'syn_block', modifier, 'danger').then(()=>{})
                }

                if(data.parserResult.result != 'None'){
                    function modifier(){
                        var b = document.createElement('b')
                        b.innerText = `----> ${data.parserResult.result}`
                        b.classList.add(['text-success'])
                        display.appendChild(b)
                    }

                    function modifier1(){
                        display.appendChild(document.createElement('hr'))
                        var b2 = document.createElement('b')
                        b2.innerText = `Optimized\n\n ${data.parserResult.optimizedCode}`
                        b2.classList.add(['text-info'])
                        display.appendChild(b2)
                    }

                    decorateView('syn_loader', 'syn_block', modifier, 'success').then(()=>{
                        decorateView('opt_loader', 'opt_block', modifier1, 'success').then(()=>{
                            decorateView('gen_loader', 'gen_block', ()=>{}, 'success').then(()=>{
                                consoleBody = document.getElementById('body')
                                consoleBody.scrollTop = consoleBody.scrollHeight; //scroll to bottom
                            })
                        })
                    })
                }
            })
            
        }
    }).catch((error)=>{
        console.log(error)
    })
}

function sendRequest(programData){
    return new Promise((resolve, reject)=>{
        var xhr = new XMLHttpRequest();

        var url = '/run'; 
        var data = {'programData': programData};

        var jsonData = JSON.stringify(data);

        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve(JSON.parse(xhr.responseText))
            } else {
                reject(xhr.statusText)
            }
        };

        xhr.send(jsonData);
    })
}