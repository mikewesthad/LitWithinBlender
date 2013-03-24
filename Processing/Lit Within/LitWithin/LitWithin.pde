// Soma parameters
int numSomas = 10;
int somaParameters = 3; // x, y, size
float[][] somas;

float minDistance = 50;
float minSize = 10;
float maxSize = 20;
float deathSize = 5;
float speed = 50;


// Branching parameters
Cell[] cells;
ArrayList branches = new ArrayList();

// Developmental stage flags
boolean somaSpacingStage = false;
boolean neuriteGrowingStage = false;



void setup() {
  size(800, 800);
  startSomaSpacingStage();
}



// #################################################################
// Draw Functions
// #################################################################

void draw() {
  // Call the appropriate update based on the current stage
  if (somaSpacingStage) somaSpacingDraw();
  else if (neuriteGrowingStage) neuriteGrowingDraw();
}

void somaSpacingDraw() {
  // Clear screen
  background(255);
  
  // Update somas
  boolean somasAreSpaced = spaceSomas();
  drawSomas();
  
  // Check if time to switch stages
  if (somasAreSpaced){
    stopSomaSpacingStage();
    startNeuriteGrowingStage();
  }
}

void neuriteGrowingDraw() {
  // Update all the dendrites
  for (int i=0; i<cells.length; i++) {
    cells[i].updateActiveBranches();
  }
  
}

// #################################################################
// Neurite Growing Stage
// #################################################################

void startNeuriteGrowingStage() {
    neuriteGrowingStage = true;
    cells = new Cell[numSomas];
    for (int i=0; i<numSomas; i++) {
      float x = somas[i][0];
      float y = somas[i][1];
      float s = somas[i][2];
      Cell c = new Cell(x, y, 10);
      cells[i] = c;
    }
  
}

class Cell {
  
  float x;
  float y;
  float somaSize;
  float cellRadius;
  
  ArrayList activeBranches; 
  
  int initialBranches;
 
  color somaColor;
  
  Cell(float iX, float iY, int iBranches) {
    x = iX;
    y = iY;
    initialBranches = iBranches;
    
    activeBranches = new ArrayList();
    createInitialBranches();
    
  }
  
  void createInitialBranches() {
    for (int i=0; i<initialBranches; i++) {
      float heading = 360.0/initialBranches * float(i);
      float resources = 600.0;
      float headingRange = 45.0;
      float speed = 2.0;
      BranchHead b = new BranchHead(x, y, heading, resources, headingRange, speed, color(random(0,255),0,0));
      activeBranches.add(b);
    }    
  }
  
  void updateActiveBranches() {
    
    int i=0;
    while (i < activeBranches.size()) {
      BranchHead b = (BranchHead) activeBranches.get(i);
      if (b.isAlive()) {
        b.grow();
        b.display();
        if (random(0,1) < 0.1) {
          float x = b.x;
          float y = b.y;
          float heading = b.heading;
          float resources = b.resources;
          float headingRange = b.headingRange;
          float speed = b.speed;
          color c = b.c;
          BranchHead newB = new BranchHead(x, y, heading-45.0, resources/2.0, headingRange, speed, c);
          BranchHead newB2 = new BranchHead(x, y, heading+45.0, resources/2.0, headingRange, speed, c);
          activeBranches.remove(i);
          activeBranches.add(newB);
          activeBranches.add(newB2);
          i--;
        }
      }
      i++;
    }
  }
  
}

class BranchHead {
  float x;
  float y;
  float heading;  // Counter-clockwise from x axis
  float resources;
  float headingRange;
  float speed;
  
  float oldX;
  float oldY;
  color c;
  
  BranchHead(float iX, float iY, float iHeading, float iResources, float iHeadingRange, float iSpeed, color ic) {
    x = iX;
    y = iY;
    heading = -iHeading;
    resources = iResources;
    headingRange = iHeadingRange;
    speed = iSpeed;
    c = ic;
  }
  
  boolean isAlive() {
    if (resources > 0) {
      return true;
    }
    return false;    
  }
 
  void grow() {
    if (isAlive()) {
      oldX = x;
      oldY = y;
      heading += random(-headingRange/2.0, headingRange/2.0);
      x += cos(radians(heading)) * speed;
      y += sin(radians(heading)) * speed;
      resources -= dist(x,y,oldX,oldY);
    }
  }
 
  void display() {
    stroke(c);
    line(oldX, oldY, x, y);
  } 
}


// #################################################################
// Soma Spacing Stage
// #################################################################

void startSomaSpacingStage() {
  background(255);
  initalizeSomas();
  drawSomas();
  somaSpacingStage = true;
}

void stopSomaSpacingStage() {
  somaSpacingStage = false;
}

void initalizeSomas() {
  somas = new float[numSomas][somaParameters];
  for(int i=0; i<numSomas; i++) {
    float s = random(minSize, maxSize);
    float x = random(s/2, width-s/2);
    float y = random(s/2, height-s/2);
    
    somas[i][0] = x;
    somas[i][1] = y;
    somas[i][2] = s;
  } 
}

void drawSomas() {
  for(int i=0; i<numSomas; i++) {
    float x = somas[i][0];
    float y = somas[i][1];
    float s = somas[i][2];
    float intensity = (s-minSize)/(maxSize-minSize);
    color c = color(0,0,255*intensity);
    
    noStroke();
    fill(c);
    ellipse(x, y, s, s);
  }   
}

boolean spaceSomas() {
  boolean somasSpaced = true;
  for(int a=0; a<numSomas; a++) {
    for(int b=a+1; b<numSomas; b++) {
      float ax = somas[a][0];
      float ay = somas[a][1];
      float as = somas[a][2];
      float bx = somas[b][0];
      float by = somas[b][1];
      float bs = somas[a][2];
      if (dist(ax,ay,bx,by) < minDistance) {
        somasSpaced = false;
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
        
        somas[a][0] = ax;
        somas[a][1] = ay;
        somas[b][0] = bx;
        somas[b][1] = by;
      }      
    }
  }
  return somasSpaced;
}
