int numCells = 1000;
int cellParameters = 3; // x, y, size
float[][] cells;

float minDistance = 100;
float minSize = 5;
float maxSize = 10;
float deathSize = 5;
float speed = 1;

void setup() {
  size(800, 800);
  background(255);
  initalizeCells();
  drawCells();
}

void initalizeCells() {
  cells = new float[numCells][cellParameters];
  for(int i=0; i<numCells; i++) {
    float s = random(minSize, maxSize);
    float x = random(s/2, width-s/2);
    float y = random(s/2, height-s/2);
    
    cells[i][0] = x;
    cells[i][1] = y;
    cells[i][2] = s;
  } 
}

void drawCells() {
  for(int i=0; i<numCells; i++) {
    float x = cells[i][0];
    float y = cells[i][1];
    float s = cells[i][2];
    float intensity = (s-minSize)/(maxSize-minSize);
    color c = color(0,0,255*intensity);
    
    noStroke();
    fill(c);
    ellipse(x, y, s, s);
  }   
}

boolean spaceCells() {
  boolean cellsSpaced = true;
  for(int a=0; a<numCells; a++) {
    for(int b=a+1; b<numCells; b++) {
      float ax = cells[a][0];
      float ay = cells[a][1];
      float as = cells[a][2];
      float bx = cells[b][0];
      float by = cells[b][1];
      float bs = cells[a][2];
      if (dist(ax,ay,bx,by) < minDistance) {
        cellsSpaced = false;
        // Create vector from point a to point b
        float vx = bx - ax;
        float vy = by - ay;
        // Normalize the vector
        float length = pow(vx,2) + pow(vy,2);
        vx /= length;
        vy /= length;
        // Move a and b away from each other
        ax += -speed * vx;
        ay += -speed * vy;        
        bx += speed * vx;
        by += speed * vy;  
      }      
      cells[a][0] = ax;
      cells[a][1] = ay;
      cells[b][0] = bx;
      cells[b][1] = by;
    }
  }
  return cellsSpaced;
}

void draw() {
  speed *= 1.02;
  spaceCells();
  drawCells();
  
}

