# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 22:53:19 2020

@author: Lunxr
"""
##### This code produces a simulation of a 2-body problem that the user gets to make #####

#
###
#
#
###
#

### Libraries ###
import math as mt # need math functions
from math import pi # need pi value
import matplotlib.pyplot as plt
import turtle # use to draw
from random import seed # used for same sequence of random values 
                        # best used for debugging
from random import randint # random integer values



### Star or Planet ###
# this function uses the input of planet or star to change the wording of my code based on answer
def choice(ans):
    # looks for these inputs from user
    if ans in ('planet', 'Planet'):
        word = "planet" # user said planet, so planet will show up in inputs
    if ans in ('star', 'Star'):
        word = "star" # user said star, so star will show up in inputs
    return word
question = str(input("Would you like a planet or star to orbit the primary star? * "))
answer = choice(question) # use above function to change words in the user inputs
# want to take star or planet and change input statements
if answer == "planet":
    unit = "Jupiter"
    phrase = " "
else:
    unit = "Solar"
    phrase = " companion "
orbits = int(input("How many orbits would you like to see (1,2,3,...)? * ")) # run code for this long



### Scaling ###
# this function and part of code is used to scale up the distances per pixel
def real(ans): 
    if ans in ('y', 'Y', 'yes', 'Yes'): # if y then use realistic scale
        return True 
    if ans in ('n', 'N', 'no', 'No'): # if n then use unrealistic scale
        return False
# ask the user if they want realism or not, the boole statements will scale accodingly
pregunta = str(input("Would you like a realistic system? (Y/N) * "))
respuesta = real(pregunta) # calls function to be checked, which then uses appropriate scale factors
if respuesta == True: # will ask again since realism is not ideal
    stopper = str(input("Are you sure? You won't see much if yes. (Y/N) * "))
    again = real(stopper)
    if again == True: 
        d = 1
        n = 1
    else:
        no_real = 'no'
        respuesta = real(no_real)
else:
    if answer == "planet": 
        n = 2
        d = 350
    if answer == "star": # used to scale object size
        n = 0.5
        d = 350



### Variables ###
## user inputs ##
print("\nWhen the simmulation is done, click on one of the stars to close out.")
print("Semi-major axis is the distance between your object and the center of mass.")
if answer == "star":
    print("Note that a binary star system might have a value > 1000 AU.")
elif answer == "planet":
    print("For reference, Jupiter is ~5 AU while Saturn is ~10 AU away from the Sun.")
a = float(input(f"What is the semi-major axis of your {answer:s} in AU?\n1 AU is the distance between the Sun and Earth. * "))
ecc = float(input("What is the eccentricity of your orbit (a value between 0.0-1.0)? * "))
print("\nYou might want to use numbers > 0.0 and < 10.0 but any number works.")
if answer == "star":
    print("Your primary (first) star should have a larger mass than your companion (second) star.")
star_r = float(input("In Solar Radii, how large is your primary star? * "))
star_m = float(input("In Solar Masses, how massive is your primary star? * "))
object_r = float(input(f"In {unit:s} Radii, how large is your{phrase:s}{answer:s}? * "))
object_m = float(input(f"In {unit:s} Masses, how massive is your{phrase:s}{answer:s}? * "))

## initialized variables ##
phi = 0
t = 0
x = y = 0 
years = 0



### Conversions ###

# convert AU to solar radii for a
new_a = (a / 0.00465) # 1 solar radii = 0.00465 AU

# these are more initial conditions for two bodies but are solely used for making objects
r_o_top = (new_a*(1 - ecc**2))
scale = r_o_top / d
in_r_o = ((new_a*(1 - ecc**2)) / (1 + (ecc*mt.cos(0)))) / scale
# radius at phi = 0
focal = (new_a*ecc) / scale # focal point of orbit is where star will be

# conversions manipulated by n for scaling (see 'Scaling' above)
if answer == "planet":
    # need to convert planet radius to solar radii
    new_object_r = n*(object_r / 9.951) # 1 solar radii = 9.951 jupiter radii
    new_star_r = n*star_r
    # need masses to be equal, so convert to solar mass for the planet
    new_object_m = object_m / 1047.57 # 1 solar mass = 1047.57 jupiter mass
    # now the masses of each body are both in solar masses
if answer == "star": # units will be the same for both so only need pixel scale
    new_object_r = n*object_r
    new_star_r = n*star_r
    new_object_m = object_m
# now the radii and a are all in solar radii, and masses are in solar masses

# want to show years on object in Earth years -> a must be in AU
p = ((a**3) / (star_m + new_object_m))**(1/2) # period of blue object 
period = p*31540000 # 1 year = 31540000 sec -> Orbit in Earth years

vel_o_sum = (2*pi*in_r_o*695700*scale) / period # initial orbital velocity 

# lists used for plot
plist = [0]
vlist = [vel_o_sum]



### Window settings ###
# window setup
wn = turtle.Screen()
wn.title("Orbits -- 2 Body Problem")
wn.bgcolor("black")
wn.setup(width=1350, height=850) # may vary depending on computer screen
wn.setworldcoordinates(-675, -425, 675, 425) # sets coordinates of screen



### Draws Elements ###   
## Star background ##
# places a point representing a star at a random place in the window
bg = turtle.Turtle()
bg.hideturtle()
bg.color("white")
bg.shape("circle")
bg.penup()
bg.speed(0) # no animations -> maximizes speed
seed(87) # seed random number generator
for n in range(200): 
    # vary the size of the shapes with slight differences
    val = randint(1,10)
    new_val = val / 40
    bg.shapesize(new_val, new_val) # want small circles
    # generates random x and y coordinates
    valx = randint(-675,675)
    valy = randint(-425,425)
    # creates stars
    bg.goto(valx,valy) # sends to random coordinates
    bg.stamp() # stamps a white circle at the current coordinate
    wn.update() # essentially cements the stamps into the screen

## Bodies ##
# Creates Star
star = turtle.Turtle()
star.penup()
star.setpos(-focal,0) # the star will be always be opposite side of CoM than object
star.shape("circle")
star.color("yellow")
star.shapesize(new_star_r, new_star_r) # star and object arent same size
wn.update() # update for same reason as star background
# Creates Object
obj = turtle.Turtle()
obj.penup()
obj.setpos(in_r_o,0) # puts objectt at starting point on +x axis
obj.shape("circle")
obj.color("blue")
obj.shapesize(new_object_r, new_object_r) # object and star arent the same size
wn.update() # update for same reason as star background

## Paths ##
# Creates path of star
path_s = turtle.Turtle()
path_s.hideturtle()
path_s.penup()
path_s.color("grey")
path_s.pensize(0.2) # want small trail
# Creates path of object
path_o = turtle.Turtle()
path_o.hideturtle()
path_o.penup()
path_o.color("grey")
path_o.pensize(0.2) # want small trail

## Creates Legend scale for the unrealistic scale ##
scale_dist = in_r_o
if respuesta == False:
    leg = turtle.Turtle()
    leg.hideturtle()
    leg.color("red")
    leg.speed(0) # want this made as quickly as possible
    # makes horizontal component the length of r_p
    leg.penup()
    leg.goto(600,-370)
    leg.pendown()
    leg.goto(600 - scale_dist,-370)
    # goes back to right side to make vertical part
    leg.penup()
    leg.goto(600,-370)
    leg.pendown()
    leg.goto(600,-360)
    # goes to left side to make other vertical part
    leg.penup()
    leg.goto(600 - scale_dist,-370)
    leg.pendown()
    leg.goto(600 - scale_dist,-360)
    # prints how large the scale is in AU reference is distance at closest approach
    leg.penup()
    leg.goto(600,-355)
    leg.write(f"{a:,.3f} AU", align="right")
    
## Creates Legend for properties ##
prop = turtle.Turtle()
prop.hideturtle()
prop.color("red")
prop.pensize(15)
prop.speed(0)
# makes Position text
prop.penup()
prop.goto(330,-250)
prop.write("Current Distance between objects:", align="left")
# Creates Position Pen that updates
pen_pos = turtle.Turtle()
pen_pos.hideturtle()
pen_pos.color("red")
pen_pos.pensize(15)
pen_pos.speed(10)
pen_pos.penup()
pen_pos.goto(600,-250)
# makes Velocity text
prop.penup()
prop.goto(330,-280)
prop.write(f"Current Orbital Velocity (blue {answer:s}):", align="left")
# Creates Velocity Pen that updates
pen_vel = turtle.Turtle()
pen_vel.hideturtle()
pen_vel.color("red")
pen_vel.pensize(15)
pen_vel.speed(10)
pen_vel.penup()
pen_vel.goto(600,-280)
# makes Time text
prop.penup()
prop.goto(330,-310)
prop.write(f"Orbits Completed (years on blue {answer:s}):", align="left")
# Creates Time Pen that updates
pen_t = turtle.Turtle()
pen_t.hideturtle()
pen_t.color("red")
pen_t.pensize(15)
pen_t.speed(10)
pen_t.penup()
pen_t.goto(600,-310)
# makes Earth Year Text
prop.penup()
prop.goto(330,-340)
prop.write(f"1 year on blue {answer:s} = {p:,.3f} Earth years", align="left")



### Circular Motion ###
# Main loop that makes the star and planet move relative to CoM
while True:
    while phi <= 2*pi*orbits: # want multiple orbits
        if t <= (200*orbits + 1): # want small increments for more smooth motion
            
            ## EoM ##
            phi = (t*pi) / 100 # small theta values for same increment reason
            
            # object time #
            r_o = ((new_a*(1 - ecc**2)) / (1 + (ecc*mt.cos(phi)))) / scale # radial equation from object to CoM
            x_o = r_o*mt.cos(phi) + ((new_a*ecc) / scale) 
            y_o = r_o*mt.sin(phi)
            obj.goto(x_o,y_o) # send object to updated position
            # makes path that follows object
            path_o.goto(x_o,y_o)
            path_o.pendown()
    
            # now the star #
            r_s = - (new_object_m * r_o) / star_m # use center of mass to determine star distance
            x_s = r_s*mt.cos(phi) 
            y_s = r_s*mt.sin(phi)
            star.goto(x_s,y_s) # send star to updated position
            # makes path that follows star
            path_s.goto(x_s,y_s)
            path_s.pendown()
            
            ## Features ##
            
            # for legend #
            # convert to AU and account for scaling. all the values in r_diff eq are in solar radii
            # used to show difference between distance of objects
            
            # not right
            r_diff = ((r_s*scale) - (r_o*scale) + (new_object_r / n) + (new_star_r / n))*0.00465 # turns to AU
            mag_r_diff = abs(r_diff) # just magnitude
            
       
            v_o = (2*pi*r_o*695700*scale) / period # 1 solar radii = 695700 km. account for scaling
            # want to print current position velocity and number of orbits
            pen_pos.clear()
            pen_pos.write(f"{mag_r_diff:,.3f} AU", align="right")
            pen_vel.clear()
            pen_vel.write(f"{v_o:,.3f} km/s", align="right")
            pen_t.clear()
            pen_t.write(f"{years:,.3f}", align="right")
            
            # plot lists #
            vlist = vlist + [v_o]
            plist = plist + [years]
            
            ## Iterables ##
            vel_o_sum += v_o
            years += 0.005
            t += 1
            
            if t == (200*orbits + 1): # time to stop
                phi = 1002
                ave_vel_o = vel_o_sum / (200*orbits + 1)
                print(f'Average Orbital Velocity = {ave_vel_o:,.3f} km/s')
                
                ## plots ##
                pmin = float(min(plist))
                pmax = float(max(plist))
                vmin = float(min(vlist)) - 0.5
                vmax = float(max(vlist)) + 0.5
                plt.title('Orbital Velocity Evolution')
                plt.xlabel(f"Time (years on {answer:s})")
                plt.ylabel(f"Velocity of {answer:s} (km/s)")
                plt.axis([pmin,pmax,vmin,vmax])
                plt.plot(plist, vlist, 'o', markersize = 4, color = 'blue', linestyle = '--', linewidth = 1.0)
                plt.show()
                
                turtle.exitonclick() # when the window is clicked the program ends
                
            wn.update() # want to update window to show object move without leaving its impression            
#### observe this planetary system ####
