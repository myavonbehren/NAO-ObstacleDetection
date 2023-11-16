import qi
import argparse
import sys
import time
import almath
import math
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

ObstacleDetection = None

class ObstacleDetection(ALModule):
    '''
    A simple module able to react when
    an object is detected.
    '''
    def __init__(self, name):
        ALModule.__init__(self, name)
        
        self.min_safe_distance = round(0.555*3.28, 2)

        self.motion = ALProxy("ALMotion")
        self.memory = ALProxy("ALMemory")
        self.sonar = ALProxy("ALSonar")
        self.posture = ALProxy("ALRobotPosture")
        self.tts = ALProxy("ALTextToSpeech")

    def run(self):
        '''
        Wakes up the robot, subscribes to obstacle detection,
        and continuously checks for obstacles every 3 seconds.
        If Control C is pressed, unsubscribes from obstacle
        detection, stops the robot, and moves it to the rest
        position.
        '''
        self.sonar.subscribe("myApplication")
        self.motion.wakeUp()
        self.motion.moveInit()
        try:
            while True:
                self.handle_obstacles()
                time.sleep(3)
        except KeyboardInterrupt:
            self.sonar.unsubscribe("myApplication")
            self.motion.stopMove()
            self.motion.rest()


    def check(self):
        '''Checks the left and right sonar values fives times,
        takes the average, and returns True if the robot senses
        an obstacle closer or equal to the minimum safe distance
        of 1.82 feet.

        Returns:
            Tuple[bool, bool]: A tuple indicating obstacle presence
            on the left and right sides.
        '''
        
        left_sum = 0
        right_sum = 0

        for _ in range(5):
            left_sum += round(self.memory.getData("Device/SubDeviceList/US/Left/Sensor/Value") * 3.28, 2)
            right_sum += round(self.memory.getData("Device/SubDeviceList/US/Right/Sensor/Value") * 3.28, 2)
            time.sleep(0.04)

        left_avg = round(left_sum/5, 2)
        right_avg = round(right_sum/5, 2)
        
        self.obstacle_left = left_avg <= self.min_safe_distance
        self.obstacle_right = right_avg <= self.min_safe_distance

        return self.obstacle_left, self.obstacle_right

        
    def handle_obstacles(self):
        '''
        Uses the check function to retrieve sonar values and
        takes appropriate actions based on obstacles. Checks
        the left and right sonar values and determines if there
        are obstacles in the robot's path. If no obstacles are
        detected, the robot moves forward and announces
        "Nothing in my way." If obstacles are detected, the
        robot stops, announces "Oh uh something is in my way,"
        and executes a turn.
        '''
        
        obstacle_left, obstacle_right = self.check()
        
        if not obstacle_left and not obstacle_right:
            self.motion.move(0.4, 0, 0)
            self.tts.say("Nothing in my way")
        else:
            self.motion.stopMove()
            self.tts.say("Oh uh something is in my way")
            self.motion.move(0, 0, 15 * almath.TO_RAD)


def main(IP, port, session):
    myBroker = ALBroker("myBroker", "0.0.0.0", 0, IP, port)        

    global ObstacleDetection
    ObstacleDetection = ObstacleDetection("Avoid")
    
    try:
        ObstacleDetection.run()
    except KeyboardInterrupt:
        myBroker.shutdown()
        print "Interrupted by user, shutting down"
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.4.32",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(args.ip, args.port, session)
