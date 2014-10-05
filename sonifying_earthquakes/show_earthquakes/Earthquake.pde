// A simple Earthquake class

class Earthquake {
  PVector loc;
  float r;
  float edepth;
  float timer;
  int R = 255;
  int G = 255;
  int B = 255;
  int transparency;
  int emonth;
  int eday;
  int pflag;
  
  // Another constructor (the one we are using here)
  Earthquake(PVector l, float mag, float edepth, int emonth, int eday) {
    this.emonth = emonth;
    this.eday = eday;
    this.loc = l.get();
    this.edepth = edepth;
    this.r = pow(3.5,(mag-4));
    //println(mag," ",r);
    //timer = 20*mag;
    timer = 3600;
    //println("HERE: " + emonth + " " + eday);
  }

  void run() {
    update();
    render();
  }

  // Method to update location
  void update() {
    timer -= 1.0;
  }

  // Method to display
  void render() {
    //stroke(255,timer);
    //fill(100,timer);
    float alphadepth = edepth/670.; // Go from 0-1.0
    alphadepth *= 100.;
    alphadepth = 100. - alphadepth;

    int day_of_year = 30*(emonth-1) + eday;

    float phase_of_year = 6.28*(day_of_year/366.);

    float scale = (cos(phase_of_year) + 1)/2.;

    //println(day_of_year + " " + emonth + " " + eday + " " + scale + " " + alphadepth);

    R = 255-int(scale*255);
    G = 0;
    B = int(scale*255);

    //println("THERE ------- HERE: " + " " + scale + " " + phase_of_year + " " + day_of_year + " " + emonth + " " + eday + " " + loc.get() + " " + edepth + " " + alphadepth + " " + R + " " + G + " " + B);
    stroke(R,G,B,alphadepth);
    fill(R,G,B,alphadepth);
    if (abs(pflag)==2)
    {
      fill(R,G,B,100);
    }
    ellipseMode(CENTER);
    ellipse(loc.x,loc.y,r,r);
    pushMatrix();
    stroke(255);
    popMatrix();
  }
  
  // Is the Earthquake still useful?
  boolean dead() {
    if (timer <= 0.0) {
      return true;
    }
    //else if (loc.x<0 || loc.x>screen_width || loc.y<0 || loc.y>screen_height) {
      //return false;
    //} 
    else {
      return false;
    }
  }
  
   void displayVector(PVector v, float x, float y, float scayl) {
    pushMatrix();
    stroke(255);
    /*
    float arrowsize = 4;
    // Translate to location to render vector
    translate(x,y);
    stroke(255);
    // Call vector heading function to get direction (note that pointing up is a heading of 0) and rotate
    rotate(v.heading2D());
    // Calculate length of vector & scale it to be bigger or smaller if necessary
    float len = v.mag()*scayl;
    // Draw three lines to make an arrow (draw pointing up since we've rotate to the proper direction)
    line(0,0,len,0);
    line(len,0,len-arrowsize,+arrowsize/2);
    line(len,0,len-arrowsize,-arrowsize/2);
    */
    popMatrix();
  } 

}

