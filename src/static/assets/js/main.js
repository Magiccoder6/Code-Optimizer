
function getInputStrings(){
    var content = editor.getValue();
    console.log(String(content).trim())
}

function clearConsole(){
    document.getElementById('console').innerHTML = ""
}

function runCompiler(){
    var content = String(editor.getValue()).trim();
    
    sendRequest(content).then((data)=>{
        var display = document.getElementById('console')
        display.appendChild(document.createElement('br'))
        
        //Lexer Results
        if(data.lexerResult.error != 'None'){
            var b = document.createElement('b')

            b.innerText = data.lexerResult.error
            b.classList.add(['text-danger'])
            display.appendChild(b)
        }
        if(data.lexerResult.tokens != 'Tokens None'){
            var b = document.createElement('b')
            b.innerText = `----> ${data.lexerResult.tokens}`
            b.classList.add(['text-success'])
            display.appendChild(b)
        }
        
        display.appendChild(document.createElement('br'))

        if(data.lexerResult.error == 'None'){//if there is no tokenisation error show parse results
            //Parser Results
            if(data.parserResult.error != 'None'){
                var b = document.createElement('b')
                b.innerText = data.parserResult.error
                b.classList.add(['text-danger'])
                display.appendChild(b)
            }
            if(data.parserResult.result != 'None'){
                var b = document.createElement('b')
                b.innerText = `----> ${data.parserResult.result}`
                b.classList.add(['text-success'])
                display.appendChild(b)

                display.appendChild(document.createElement('hr'))
                var b2 = document.createElement('b')
                b2.innerText = `Optimized\n\n ${data.parserResult.optimizedCode}`
                b2.classList.add(['text-info'])
                display.appendChild(b2)
            }
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