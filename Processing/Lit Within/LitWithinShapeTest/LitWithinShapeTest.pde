float x = 400;
float y = 400;
float r = 50;
float speed = 10;
float thickness = 5;
float branchAngle = 15.0;

float angle = 0.0;

PShape dendrite;
PShape soma;

ArrayList leftPoints;
ArrayList rightPoints;

PVector p1 = new PVector(0,0);
PVector p2 = new PVector(0,0);
PVector v1 = new PVector(0,0);
PVector v2 = new PVector(0,0);
PVector v3 = new PVector(0,0);
PVector v4 = new PVector(0,0);


import processing.dxf.*;
boolean record = false;

void setup() {
  size(800,800,P2D); 
  frameRate(10);
  
  // Clear the screen
  background(200);
  
  // Draw a soma
  soma = createShape(ELLIPSE, 0, 0, 2*r, 2*r);
  soma.setFill(color(255));
  soma.setStrokeWeight(1);
  soma.setStroke(color(0));
  
  // Calculate the line that represents the dendrite segment
  p1.x = x + cos(radians(-angle)) * r;
  p1.y = y + sin(radians(-angle)) * r;
  p2.x = p1.x + cos(radians(-angle)) * speed;
  p2.y = p1.y + sin(radians(-angle)) * speed;
  
  // Add thickness to the dendrite segment by calculating a quad from the line
  v1.x = p1.x + cos(radians(-(angle+90))) * thickness/2;
  v1.y = p1.y + sin(radians(-(angle+90))) * thickness/2;
  v2.x = p1.x + cos(radians(-(angle-90))) * thickness/2;
  v2.y = p1.y + sin(radians(-(angle-90))) * thickness/2;
  v3.x = p2.x + cos(radians(-(angle+90))) * thickness/2;
  v3.y = p2.y + sin(radians(-(angle+90))) * thickness/2;
  v4.x = p2.x + cos(radians(-(angle-90))) * thickness/2;
  v4.y = p2.y + sin(radians(-(angle-90))) * thickness/2;
  
  leftPoints = new ArrayList();
  leftPoints.add(v1.get());
  leftPoints.add(v3.get());
  
  rightPoints = new ArrayList();
  rightPoints.add(v2.get());
  rightPoints.add(v4.get());
  
  updateDendrite();
  shape(dendrite);
}

void updateDendrite() {
  dendrite = createShape();
  dendrite.beginShape();  
  dendrite.fill(color(255,255,255));
  dendrite.strokeWeight(1);
  dendrite.stroke(color(255,255,255));
  for (int i=0; i<leftPoints.size(); i++) {
    PVector p = (PVector) leftPoints.get(i);
    dendrite.vertex(p.x, p.y);
  }  
  for (int i=rightPoints.size()-1; i>=0; i--) {
    PVector p = (PVector) rightPoints.get(i);
    dendrite.vertex(p.x, p.y);
  }
  dendrite.endShape();
}


void draw() {
  if (record) beginRaw(DXF, "output.dxf");
  
  // Increment angle
  angle += random(-20, +20);
  
  // Next quad starts with the last points of the prior quad
  p1.x = p2.x;
  p1.y = p2.y;
  p2.x = p1.x + cos(radians(-angle)) * speed;
  p2.y = p1.y + sin(radians(-angle)) * speed; 
  v3.x = p2.x + cos(radians(-(angle+90))) * thickness/2;
  v3.y = p2.y + sin(radians(-(angle+90))) * thickness/2;
  v4.x = p2.x + cos(radians(-(angle-90))) * thickness/2;
  v4.y = p2.y + sin(radians(-(angle-90))) * thickness/2;  
  leftPoints.add(v3.get());
  rightPoints.add(v4.get());
  updateDendrite();
  
  
  // Clear the screen
  background(200);
  shape(soma, 400, 400);
  shape(dendrite, 0, 0);
  
  if (record) {
    endRaw();
    record = false;
  }
}

void keyPressed() {
  if (keyCode == ENTER) record = true;  
}
