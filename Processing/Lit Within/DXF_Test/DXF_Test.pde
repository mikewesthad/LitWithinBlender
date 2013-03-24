import processing.dxf.*;

void setup() {
 size(800,800,P3D);
 translate(400,400,0);
  beginRaw(DXF, "output.dxf");
 sphere(100);
endRaw(); 
}
