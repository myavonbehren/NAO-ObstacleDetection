import move_head
import take_picture
import detect_blue

import qi
import argparse
import sys
import time
import almath

def capture_and_detect(session, head_position):
    '''
    Captures an image using NAO's camera from a specified head
    position, detects the presence of blue in the image, and
    provides corresponding feedback.

    Args:
        session (qi.Session): The Qi session for connecting to
                              NAO's services.
                              
        head_position (str): The desired head position for image capture.
                             Options: 'center', 'right', 'left'.

    Returns:
        bool: True if blue is detected in the captured image, False
              otherwise.
    '''
    if head_position == 'center':
        move_head.center(session)
    elif head_position == 'right':
        move_head.right(session)
    elif head_position == 'left':
        move_head.left(session)

    img = take_picture.pic(position + '.png', 0)

    if detect_blue.detect(img):
        speech_service = session.service("ALTextToSpeech")
        speech_service.say('Blue detected on the ' + position)
        return True
    return False

def main(session):
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    motion_service.wakeUp()
    posture_service.goToPosture("StandInit", 0.5)

    positions = ['center', 'right', 'left']
    blue_detected = False

    for position in positions:
        if capture_and_detect(session, position):
            blue_detected = True

    time.sleep(5)
    motion_service.stopMove()
    motion_service.rest()


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
    main(session)
