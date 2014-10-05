import ddf.minim.*;
import ddf.minim.signals.WhiteNoise;
import ddf.minim.ugens.*;


float[][] pos = new float[1000][3];

PImage merc = new PImage();

//float window_width = 640;
//float window_height = 360;
//float window_width = 1.8*640;
//float window_height = 1.8*360;
float window_width = 1380;
float window_height = 760;

float biggest_mag = 5.0;

// just plays a burst of noise of the specified tint and amplitude
class NoiseInstrument implements Instrument
{
    // create all variables that must be used throughout the class
    Noise myNoise;

    // constructors for the intsrument
    NoiseInstrument( float amplitude, Noise.Tint noiseTint )
    {
    // create new instances of any UGen objects as necessary
    // white noise is used for this instrument
    myNoise = new Noise( amplitude, noiseTint );
    }

    // every instrument must have a noteOn( float ) method
    void noteOn( float dur )
    {
    myNoise.patch( out );
    }

    // every instrument must have a noteOff() method
    void noteOff()
    {
    // unpatch the output 
    // this causes the entire instrument to stop calculating sampleframes
    // which is good when the instrument is no longer generating sound.
    myNoise.unpatch( out );
    }
}

EarthquakeSystem es;

int ecount;
int eframe = 0;

int t = 0;
float x = 0;
float y = 0;
float circle_radius=140;

Minim minim;
AudioPlayer noise;
AudioOutput out;
//WhiteNoise whitenoise;
NoiseInstrument whitenoise;

Table table;
TableRow row;


// The statements in the setup() function 
// execute once when the program begins
void setup() {
    size(int(window_width), int(window_height));  // Size must be the first statement
    stroke(255);     // Set line drawing color to white
    frameRate(60);   // How many frames per second to show.

    //merc = loadImage("data/mercator.jpg");
    //merc.resize(int(1.0*window_width),int(0.9*window_height));


    //table = loadTable("select_data_earthquakes1974.csv","header");
    table = loadTable("select_data_earthquakes1974.csv");
    //println(table.getRowCount());
    minim = new Minim(this);
    out = minim.getLineOut(Minim.MONO, 512);
    //noise = minim.loadFile("noise.mp3");
    noise = minim.loadFile("stickhit.mp3");
    //noise = minim.loadFile("rocksfalling.mp3");

    //whitenoise = new WhiteNoise(1.0);
    whitenoise = new NoiseInstrument( 0.5, Noise.Tint.WHITE );
    out.playNote(0,120.,whitenoise);

    ecount = 0;

    es = new EarthquakeSystem(0, new PVector(width/2,height/2,0));

}

// This function is run everytime a new frame is 
// shown. 
void draw() { 
  
    background(0);   // Set the background to black

    //image(merc,0,-70);
    
        /*
    if (t%60==0)
    {
        x = random(0,window_width);
        y = random(0,window_height);
        //if (!noise.isPlaying()) 
        if (true)
        {
            noise.rewind(); 
            noise.setGain(-20);
            noise.play();
            //println("Playing noise.");
        }
    }
        */


    row = table.getRow(ecount);
    eframe = row.getInt(0); // The frame/time in which to display an earthquake.
    int year = row.getInt(1);

    biggest_mag = 5.0;
    while (t==eframe)
    {

      int month = row.getInt(2);
      int day = row.getInt(3);
      float lat = row.getFloat(4);
      float lon = row.getFloat(5);
      float depth = row.getFloat(6);
      float mag = row.getFloat(7);
      float y = ((-1 * lat) + 90.) * (window_height / 180.);
      float x = (lon + 180.) * (window_width / 360.);
      //mag -= 4;
      //mag *= 10;
      //println(lat + " " + lon + " " + x + " " + y + " " + mag + " " + month + " " + day);
      es.addEarthquake(x,y,mag,depth,month,day);

      //noise.rewind(); 
      //noise.setGain(pow(3.5,(mag-4)));
      //noise.play();
      //float signal[] = {-1.,0.,1.};
      //whitenoise.generate(signal);
      //out.playNote(0,1.5,whitenoise);
      //out.shiftVolume(3,2,100);
      if (biggest_mag<mag)
      {
          biggest_mag = mag;
      }

      ecount += 1;
      row = table.getRow(ecount);
      eframe = row.getInt(0); // The frame/time in which to display an earthquake.
    }
    int gain = int(((biggest_mag-5)/5.)*120) - 20;
    //println("gain --------------------------- " + gain + " " + biggest_mag);
    out.setGain(gain);
    //out.setBalance(-1);
    //out.setGain(-100);

    es.run();

  
    // Draw an ellipse.
    //float scale = (t%60)*circle_radius*(1./60);
    //fill(255,(t%60)*50*(1./60)+50);
    //stroke(255,(t%60)*50*(1./60)+50);
    //ellipse(lat,lon,10,10);
    //ellipse(x,y,scale,scale);

    fill(255, 255, 255, 100);
    String s = str(year);
    text(s, 15, 30,400,400);
    textSize(48);



    t += 1;

    String name = "output/frames"+nf(t,4)+".png";
    //saveFrame(name);

} 

void stop()
{
    //noise.close();
    minim.stop();
}

