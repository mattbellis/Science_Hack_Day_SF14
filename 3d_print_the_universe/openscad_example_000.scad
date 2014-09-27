module mymod()
{

    sphere(r = 5);
    translate([20,0,0])
    {
        sphere(r = 8);
    }

    translate([20,0,0])
    {
        rotate([0,270,0])
        {
            cylinder(h=20,r1=2,r2=1);
        }
    }
}

mymod();
