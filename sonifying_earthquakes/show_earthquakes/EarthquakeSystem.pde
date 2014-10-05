// A class to describe a group of Earthquakes
// An ArrayList is used to manage the list of Earthquakes 

class EarthquakeSystem {

  ArrayList earthquakes;    // An arraylist for all the Earthquakes
  PVector origin;        // An origin point for where Earthquakes are born

  EarthquakeSystem(int num, PVector v) {
    earthquakes = new ArrayList();              // Initialize the arraylist
    origin = v.get();                        // Store the origin point
    for (int i = 0; i < num; i++) {
      earthquakes.add(new Earthquake(origin,0,0,0,0));    // Add "num" amount of earthquakes to the arraylist
    }
  }

  int size() {
    return earthquakes.size();
  }

  void run() {
    // Cycle through the ArrayList backwards b/c we are deleting
    for (int i = earthquakes.size()-1; i >= 0; i--) {
      Earthquake p = (Earthquake) earthquakes.get(i);
      p.run();
      if (p.dead()) {
        earthquakes.remove(i);
      }
    }
  }

  void addEarthquake() {
    earthquakes.add(new Earthquake(origin,0,0,0,0));
  }
  
  void addEarthquake(float x, float y, float mag, float edepth, int emonth, int eday) {
      ////println("ADDING: " + emonth);
    earthquakes.add(new Earthquake(new PVector(x,y),mag,edepth,emonth,eday));
    ////println("here");
  }

  void addEarthquake(Earthquake p) {
    earthquakes.add(p);
  }

  // A method to test if the earthquake system still has earthquakes
  boolean dead() {
    if (earthquakes.isEmpty()) {
      return true;
    } else {
      return false;
    }
  }

}

