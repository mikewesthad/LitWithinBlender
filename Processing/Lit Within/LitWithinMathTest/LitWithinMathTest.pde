float x = 400;
float y = 400;
float r = 50;
float speed = 25;
float thickness = 5;
float branchAngle = 15.0;

float x1;
float y1;
float x2;
float y2;
float p1x;
float p1y;
float p2x;
float p2y;
float p3x;
float p3y;
float p4x;
float p4y;
float angle = 0.0;

void setup() {
  size(800,800); 
  
  // Clear the screen
  background(200);
  
  // Draw a soma
  fill(255);
  stroke(0);
  ellipse(x,y,2*r,2*r);
  
  
  x1 = x + cos(radians(-angle)) * r;
  y1 = y + sin(radians(-angle)) * r;
  x2 = x + cos(radians(-angle)) * (r + speed);
  y2 = y + sin(radians(-angle)) * (r + speed);  
  
  p1x = x1 + cos(radians(-(angle+90))) * thickness/2;
  p1y = y1 + sin(radians(-(angle+90))) * thickness/2;
  p2x = x1 + cos(radians(-(angle-90))) * thickness/2;
  p2y = y1 + sin(radians(-(angle-90))) * thickness/2;
  p3x = x2 + cos(radians(-(angle+90))) * thickness/2;
  p3y = y2 + sin(radians(-(angle+90))) * thickness/2;
  p4x = x2 + cos(radians(-(angle-90))) * thickness/2;
  p4y = y2 + sin(radians(-(angle-90))) * thickness/2;

  fill(255);
  stroke(color(0,0,255));
  quad(p1x, p1y, p3x, p3y, p4x, p4y, p2x, p2y);  
  
  frameRate(30);
}

void draw() {
  
  // Increment angle
  angle += random(-90,+90);
  
  
  // Next quad starts with the last points of the prior quad
  x1 = x2;
  y1 = y2;
  x2 = x1 + cos(radians(-angle)) * speed;
  y2 = y1 + sin(radians(-angle)) * speed; 
  p1x = p3x;
  p1y = p3y;
  p2x = p4x;
  p2y = p4y;
  p3x = x2 + cos(radians(-(angle+90))) * thickness/2;
  p3y = y2 + sin(radians(-(angle+90))) * thickness/2;
  p4x = x2 + cos(radians(-(angle-90))) * thickness/2;
  p4y = y2 + sin(radians(-(angle-90))) * thickness/2;  
  quad(p1x, p1y, p3x, p3y, p4x, p4y, p2x, p2y); 
  

}


void initialTest() {
  // Increment angle
  angle += 1;
  
  // Clear the screen
  background(200);
  
  // Draw a reference bounding rectangle
  noFill();
  stroke(255);
  quad(x-r, y-r, x+r, y-r, x+r, y+r, x-r, y+r);
  
  // Draw a soma
  fill(255);
  stroke(0);
  ellipse(x,y,2*r,2*r);
  
  // Draw a line from soma center to the start of the dendrite
  float x1 = x + cos(radians(-angle)) * r;
  float y1 = y + sin(radians(-angle)) * r;
  float x2 = x + cos(radians(-angle)) * (r + speed);
  float y2 = y + sin(radians(-angle)) * (r + speed);  
  stroke(100);
  line(x, y, x1, y1);
  
  // Draw a quad segment of the dendrite
  float p1x = x1 + cos(radians(-(angle+90))) * thickness/2;
  float p1y = y1 + sin(radians(-(angle+90))) * thickness/2;
  float p2x = x1 + cos(radians(-(angle-90))) * thickness/2;
  float p2y = y1 + sin(radians(-(angle-90))) * thickness/2;
  float p3x = x2 + cos(radians(-(angle+90))) * thickness/2;
  float p3y = y2 + sin(radians(-(angle+90))) * thickness/2;
  float p4x = x2 + cos(radians(-(angle-90))) * thickness/2;
  float p4y = y2 + sin(radians(-(angle-90))) * thickness/2;  
  fill(255);
  stroke(color(0,0,255));
  quad(p1x, p1y, p3x, p3y, p4x, p4y, p2x, p2y);
  
  
  // Draw a second quad segment that branches off at an angle
  float newAngle = angle + branchAngle;
  float x3 = x2 + cos(radians(-newAngle)) * speed;
  float y3 = y2 + sin(radians(-newAngle)) * speed;  
  float p5x = x3 + cos(radians(-(newAngle+90))) * thickness/2;
  float p5y = y3 + sin(radians(-(newAngle+90))) * thickness/2;
  float p6x = x3 + cos(radians(-(newAngle-90))) * thickness/2;
  float p6y = y3 + sin(radians(-(newAngle-90))) * thickness/2;  
  fill(255);
  stroke(color(255,0,0));
  quad(p3x, p3y, p5x, p5y, p6x, p6y, p4x, p4y);
  
    
  // Draw a second quad segment that branches off at an angle
  newAngle = newAngle + branchAngle;
  float x4 = x3 + cos(radians(-newAngle)) * speed;
  float y4 = y3 + sin(radians(-newAngle)) * speed;  
  float p7x = x4 + cos(radians(-(newAngle+90))) * thickness/2;
  float p7y = y4 + sin(radians(-(newAngle+90))) * thickness/2;
  float p8x = x4 + cos(radians(-(newAngle-90))) * thickness/2;
  float p8y = y4 + sin(radians(-(newAngle-90))) * thickness/2;  
  fill(255);
  stroke(color(0,255,0));
  quad(p6x, p6y, p8x, p8y, p7x, p7y, p5x, p5y);


  noFill();
  stroke(0);
  ellipse(x,y,2*(r+speed),2*(r+speed));
  ellipse(x,y,3*(r+speed),3*(r+speed));
  ellipse(x,y,4*(r+speed),4*(r+speed));
}
