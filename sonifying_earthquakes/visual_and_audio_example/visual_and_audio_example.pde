import ddf.minim.*;

float window_width = 640;
float window_height = 360;

int t = 0;
float x = 0;
float y = 0;
float circle_radius=140;

Minim minim;
AudioPlayer noise;

// The statements in the setup() function 
// execute once when the program begins
void setup() {
    size(640, 360);  // Size must be the first statement
    stroke(255);     // Set line drawing color to white
    frameRate(30);   // How many frames per second to show.

    minim = new Minim(this);
    noise = minim.loadFile("noise.mp3");
}

// This function is run everytime a new frame is 
// shown. 
void draw() { 
  
    background(0);   // Set the background to black
    
    if (t%60==0)
    {
        x = random(0,window_width);
        y = random(0,window_height);
        //if (!noise.isPlaying()) 
        if (true)
        {
            noise.rewind(); 
            noise.play();
            println("Playing noise.");
        }
    }
  
    // Draw an ellipse.
    float scale = (t%60)*circle_radius*(1./60);
    fill(255,(t%60)*50*(1./60)+50);
    stroke(255,(t%60)*50*(1./60)+50);
    ellipse(x,y,scale,scale);


    t += 1;
} 

void stop()
{
    noise.close();
    minim.stop();
}
