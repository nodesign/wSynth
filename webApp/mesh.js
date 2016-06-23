var points = [];
var distance = [];
var targetX, targetY;
var deformedPoints = [];
var widthPixels = 30;
var heightPixels = 20;
var dimension = 30;
var radius = 150;
var ws;
var xGesture, yGesture, zGesture;

function setup() {
    createCanvas(windowWidth, windowHeight);
    ws = new WebSocket('ws://localhost:8080/');

    for (var y=0; y<heightPixels; y++) {
        for (var x=0; x<widthPixels; x++) {
            var v = createVector(x*dimension,y*dimension);
            points.push(v);
        }
    }
    console.log("got it");
    

    ws.onmessage = function(event) {
      //console.log('Count is: ' + event.data);
      var data = event.data.split(" ");
      //console.log(parseInt(data[0]));
      xGesture = parseInt(data[0]);
      
      if (xGesture<24000) x = 24000;
      if (xGesture>38000) x = 38000;
      xGesture = map(xGesture, 24000,38000, 0,600);

      yGesture = parseInt(data[1]);
      
      if (yGesture<38000) y = 38000;
      if (yGesture>46000) y = 46000;
      yGesture = map(yGesture, 38000,46000, 300,0);

      zGesture = map(parseInt(data[2]), 0,10000, 0.5,1);
      
      targetX = xGesture;
      targetY = yGesture;
      //redraw();
      //console.log(targetX + " " + targetY + " " + zGesture);
      
    };
    
}


function draw() {

    //targetX = mouseX;
    //targetY = mouseY;
    background(0);

    fill(255);

    for (var i in points) {
        var d = dist(targetX, targetY, points[i].x, points[i].y);
        var x,y;
        if (d<radius) {
            var dd = map(d, 0,radius,0,3);
            var force = map(exp(dd), 0,20, zGesture,1.0);
            x = lerp(targetX, points[i].x, force);
            y = lerp(targetY, points[i].y, force);
        } else {
            x = points[i].x;
            y = points[i].y;
        }
        deformedPoints.push(createVector(x,y));
    }

    for (var i in points) {
        var xx = deformedPoints[i].x;
        var yy = deformedPoints[i].y;
        noStroke();
        ellipse(xx,yy, 5,5);
    }

    stroke(255);

    for (var y=0; y<heightPixels; y++) {
        for (var x=0; x<widthPixels; x++) {
            var p = y*widthPixels+x;
            var p1 = y*widthPixels+(x-1);
            var p2 = (y-1)*widthPixels+x;

            if (x>0)
                line(deformedPoints[p].x, deformedPoints[p].y, deformedPoints[p1].x, deformedPoints[p1].y);
            if (y>0)
                line(deformedPoints[p].x, deformedPoints[p].y, deformedPoints[p2].x, deformedPoints[p2].y);
        }
    }

    noFill();
    stroke(255,0,0);
    ellipse(targetX, targetY, radius,radius);
    deformedPoints = [];
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
  maxDistance = dist(0,0, width, height);
}

function mouseReleased() {
    console.log(mouseX + " " + mouseY);
}

