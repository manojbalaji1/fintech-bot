var main = document.getElementById("main");
var recordButton = document.getElementById("recordButton");

function record() {
    document.getElementById("recordButton").classList.add('btn-danger');
    document.getElementById("recordButton").classList.remove('btn-success');
    document.getElementById("recordButton").value = "Recording.....";

    window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
    let finalTranscript = '';
    let recognition = new window.SpeechRecognition();
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;
    recognition.continuous = false;
    let interimTranscript = null;
    recognition.onresult = (event) => {
       interimTranscript = event.results[0][0].transcript;
        document.getElementById('speech').innerHTML = finalTranscript + '<i style="color:black;">ME :' + interimTranscript + '</>';
    }
    recognition.start();
    var obj = JSON.parse('{ "message":"hi"}');
    recognition.addEventListener('end', function() { 
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {

        
            if (this.readyState == 4 && this.status == 200) {

                document.getElementById("recordButton").classList.remove('btn-danger');
                document.getElementById("recordButton").classList.add('btn-success');
                document.getElementById("recordButton").value = "Record";

                console.log('hello')
                console.log(JSON.parse(this.responseText));
                obj = JSON.parse(this.responseText);
                var message = obj.message;
              document.getElementById('idiot').innerHTML = 'Bot : ' + obj.message;
              
              //code for speaking

              var msg = new SpeechSynthesisUtterance();
                var voices = window.speechSynthesis.getVoices();
                msg.voice = voices[10]; // Note: some voices don't support altering params
                msg.voiceURI = 'native';
                msg.volume = 1; // 0 to 1
                msg.rate = 1; // 0.1 to 10
                msg.pitch = 2; //0 to 2
                msg.text = message;
                msg.lang = 'en-US';

                msg.onend = function(e) {
                console.log('Finished in ' + event.elapsedTime + ' seconds.');
                };

                speechSynthesis.speak(msg);

            }
        };
        xhttp.open("GET", "http://localhost:5000/question?message="+interimTranscript, true);
        xhttp.send();
        console.log(interimTranscript)
        
       //document.getElementById("idiot").innerHTML = obj.message;
    });
}

function send(interimTranscript) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        document.getElementById("demo").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "http://0.0.0.0:5000/question?message="+interimTranscript, true);
    xhttp.send();
    console.log(interimTranscript)
}