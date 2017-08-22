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

def AG(distance):
    "Population -  random individual" 
    #moveForward(val)
    #moveBackward(val)
    #moveLeft(val)
    #moveRight(val)
    #moveUp(val)
    #moveDown(val)
    turnLeft = 0
    turnRight = 1


    FITNESS = collisionProbability(distance)
    print "FITNESS:", FITNESS
    while not FITNESS:
       individual = random.randint(0, 1)
       if individual == 1:
          #drone.turnAngle(-90,0.5,1)
          time.sleep(2)
          #drone.hover()
          distance = sensor.get_distance()
          FITNESS = collisionProbability(distance)
          print "turn left"
          print "FITNESS: ", FITNESS

       else:
          #drone.turnAngle(90,0.5,1)
          time.sleep(2)
          #drone.hover()
          distance = sensor.get_distance()
          FITNESS = collisionProbability(distance)
          print "turn right"
          print "FITNESS: ", FITNESS

def collisionProbability(distance):
   #drone.hover()
   a1 = sensor.get_distance()
   a2 = sensor.get_distance()
   a3 = sensor.get_distance()
   event = 0
   print "Distance found: ", distance
   print "amostra1: ", a1, "amostra2: ", a2, "amostra3: ", a3
   if a1 > 50:
      event = event + 1
   if a2 > 50:
      event = event + 1
   if a3 > 50:
      event = event + 1

   collision = event * 33			# (event / 3) * 100 => Percentage of measure is correct
   print "event: ", event
   print "No collision occurs: ", collision, "%"
   if collision == 99:
      t = distance / 50                                 # speed: 50 cm/s (10% of max speed) 
      t = t + 0.5					# Get out of inertia
      #drone.moveForward(0.1)	
      print "Drone is move forward with 50cm/s durant", t, "s"
      time.sleep(t)
      #drone.hover()
      return True
   elif collision == 66:
      t = distance / 50                                 # speed: 50 cm/s (10% of max speed) 
      #drone.moveForward(0.1)	
      print "Drone is move forward with 50cm/s durant", t, "s"
      time.sleep(t)
      #drone.hover()
      return True
   else:
      return False
   

########## Drone configure #############

#drone = ps_drone.Drone()                                 # Start using drone                   
#drone.startup()                                          # Connects to drone and starts subprocesses

#drone.reset()                                            # Sets drone's status to good (LEDs turn green when red)
#while (drone.getBattery()[0] == -1):   time.sleep(0.1)   # Wait until drone has done its reset
#print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])  # Gives a battery-status
#if drone.getBattery()[1] == "empty":   sys.exit()        # Give it up if battery is empty

#drone.useDemoMode(True)                                  # Just give me 15 basic dataset per second (is default anyway)
#drone.getNDpackage(["demo"])                             # Packets, which shall be decoded
#time.sleep(0.5)                                          # Give it some time to awake fully after reset

#drone.takeoff()                                          # Fly, drone, fly !
#while drone.NavData["demo"][0][2]:     time.sleep(0.1)   # Wait until the drone is really flying (not in landed-mode anymore)

######## Mainprogram begin #############
print "The Drone is flying now, land it with any key"
time.sleep(2)
#drone.moveUp(0.1)
time.sleep(1)
#drone.hover()


######## auto flight #############
try:
   end = False
   while not end:
      distance = sensor.get_distance()                  # Get distance from sensor
      if distance <= 50:
#         drone.hover()                                # Stop and hold position
         print "Drone found an obstacle at ", distance, "cm"
         print "Genetic Algorithm is running..."
         AG(distance)
   
      else:
         collisionProbability(distance) 
   
#   print "Batterie: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])	# Gives a battery-status

except KeyboardInterrupt:
   print "User cancelled"

except:
   print "Unexpected error:"
   raise

finally:
   print "Drone is landing"
#   drone.stop()
#   time.sleep(1)
#   drone.land()

