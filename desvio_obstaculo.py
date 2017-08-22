#########
# desvio_obstaculo.py
#
# DISCIPLINA: Inteligencia artificial
# ALUNO:
#  Fabio Machado Costa
#  Florencia Malenchini
#  Lucas Almeida
#
# DEPENDENCIES: a POSIX OS, PS-Drone-API 2.0 beta or higher.
#
###########

import time, sys, random
import ps_drone                                          # Import PS-Drone-API
import hcsr04 as sensor                                  # Import HC-SR04 Ultrasonic Sensor

STUCK = 0
 
def HC(distance):
    "Population -  random individual" 
    #moveBackward(val)
    #moveLeft(val)
    #moveRight(val)
    #moveUp(val)
    #moveDown(val)
    turnRight = 0
    turnLeft = 1
    moveForward = 2
    
    STUCK = 0
    
    COLLISION = True
    while COLLISION and STUCK <= 3:
       individual = random.randint(0, 2)
       if individual == 1:
          print "Im turning left"
          drone.turnAngle(-90,1,1)
          distance = sensor.get_distance()
          COLLISION = collisionProbability(distance)
          print "COLLISION: ", COLLISION

       elif individual == 0:
          print "Im turning right"
          drone.turnAngle(90,1,1)
          # time.sleep(1)
          # drone.hover()
          distance = sensor.get_distance()
          COLLISION = collisionProbability(distance)
          print "COLLISION: ", COLLISION
       else:
          print "Im turning forward: " 
          distance = sensor.get_distance()
          COLLISION = collisionProbability(distance)
          print "COLLISION: ", COLLISION
       STUCK = STUCK + 1
       if STUCK > 3:
          print "Oh my God , Im stuck!"
          drone.moveUp(0.3)
          time.sleep(2)
          drone.hover()
          distance = sensor.get_distance()
	  COLLISION = collisionProbability(distance)
          if not COLLISION:
             drone.moveDown(0.3)
             time.sleep(2)
             drone.hover() 
          else:
             drone.land()
             sys.exit() 

            

def collisionProbability(distance):
   print "Im checking distance..."
   distance = sensor.get_distance()

   print "It is: ", distance, "cm"
  
   
   pmenor50 = 0.95
   pmaior50menor70 = 0.75
   pmaior70 = 0.5
   pobstsala = 0.5
  
   if distance < 50:
      pcollision = pmenor50*pobstsala*100         # speed: 50 cm/s (10% of max speed) 
   elif distance >= 50 and distance < 70:
      pcollision = pmaior50menor70*pobstsala*100
   else:
      pcollision = pmaior70*pobstsala*100
		
   print pcollision, "% of NO COLLISION"
   if pcollision < 45 and pcollision > 25:
      t = distance/50  + 1
      print "Yaaaay! I can go forward!!"
      drone.doggyHop()
      time.sleep(2)							# Get out of inertia
      drone.moveForward(0.1)	
      print "Im moving forward with 50cm/s during", t, "s"
      time.sleep(t)
      drone.hover()
      STUCK = 0
      return False
   elif pcollision <= 25:
      t = distance/50  + 1.5
      print "Yaaaay! I can go forward!!"
      drone.doggyHop()
      time.sleep(2)							# Get out of inertia
      drone.moveForward(0.1)	
      print "Im  moving forward with 50cm/s during", t, "s"
      time.sleep(t)
      drone.hover()
      STUCK = 0	
      return False
   else:
      print "Oh no! I cant go forward"
      drone.doggyWag()
      time.sleep(2)
      print "I found an obstacle at ", distance, "cm"
      return True
   

########## Drone configure #############

drone = ps_drone.Drone()                                 # Start using drone                   
drone.startup()                                          # Connects to drone and starts subprocesses

drone.reset()                                            # Sets drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0] == -1):   time.sleep(0.1)   # Wait until drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])  # Gives a battery-status
if drone.getBattery()[1] == "empty":   sys.exit()        # Give it up if battery is empty

drone.useDemoMode(True)                                  # Just give me 15 basic dataset per second (is default anyway)
drone.getNDpackage(["demo"])                             # Packets, which shall be decoded
time.sleep(0.5)                                          # Give it some time to awake fully after reset

drone.takeoff()                                          # Fly, drone, fly !
while drone.NavData["demo"][0][2]:     time.sleep(0.1)   # Wait until the drone is really flying (not in landed-mode anymore)

######## Mainprogram begin #############
print "The Drone is flying now, land it with any key"
drone.moveUp(0.1)
time.sleep(1)
drone.hover()
print "Are you ready drone?"
print "Yeah!"
drone.doggyHop()
time.sleep(1)
######### auto flight #############
try:
   while True:
      distance = sensor.get_distance()                  # Get distance from sensor
      print "Hill Climbing is running..."
      HC(distance)
   
   print "Batterie: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])	# Gives a battery-status

except KeyboardInterrupt:
   print "User cancelled"

except:
   print "Unexpected error:", sys.exit()
   raise

finally:
   print "Drone is landing"
   drone.stop()
   time.sleep(1)
   drone.land()
   sys.exit()
