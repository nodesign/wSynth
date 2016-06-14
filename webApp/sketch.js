var value = 0;
var x, y;
var drawIt = false;
var cnt = 40;
var note, velocity;
var ws;

var w,h;
var note = 0;
var previousNote = -1;
function setup() {
    createCanvas(windowWidth, windowHeight);
    ws = new WebSocket('ws://192.168.1.10:8080/');
    w = round(width/10);
    h = round(height/12);

}


function draw() {
    background(0);


    for (var i=0; i<10; i++) {
        for (var j=0; j<12; j++) {
            stroke(128);

            var x = i*w;
            var y = j*h;

            if ((mouseX>x) && (mouseX<x+w) && (mouseY>y) && (mouseY<y+h)) {
                fill(255);
                note = j*10+i;
                if (note != previousNote) {
                    ws.send("144 " + note + " 127"); // Note ON
                    if (previousNote != -1)
                        ws.send("128 " + previousNote + " 127"); // Note OFF
                    previousNote = note;
                    console.log(note);
                }
                //console.log(note);
            } else {
                fill(0);
            }
            rect(x,y, w-1,h-1);
        }
    }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}