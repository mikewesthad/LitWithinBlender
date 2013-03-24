int numCells = 1000;
int cellParameters = 3; // x, y, size
float[][] cells;

float minDistance = 50;
float minSize = 10;
float maxSize = 20;
float deathSize = 5;
float speed = 50;

boolean somaSpacingStage = false;
boolean neuriteGrowingStage = false;

void setup() {
  size(800, 800);
  background(255);
  initalizeSomas();
  drawSomas();
  somaSpacingStage = true;
}

void initalizeSomas() {
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

void drawSomas() {
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

boolean spaceSomas() {
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
        
        if (ax < 0) ax = 0;
        if (ay < 0) ay = 0;
        if (ax > width) ax = width;
        if (ay > height) ay = height;
        
        if (bx < 0) bx = 0;
        if (by < 0) by = 0;
        if (bx > width) bx = width;
        if (by > height) by = height;
        
        cells[a][0] = ax;
        cells[a][1] = ay;
        cells[b][0] = bx;
        cells[b][1] = by;
      }      
    }
  }
  return cellsSpaced;
}


void draw() {
  if (somaSpacingStage) somaSpacingUpdate();
  
}

void somaSpacingUpdate() {
  background(255);
  
  boolean cellsAreSpaced = spaceSomas();
  if (cellsAreSpaced){
    somaSpacingStage = false;
    neuriteGrowingStage = true;
  }
  drawSomas();
}
