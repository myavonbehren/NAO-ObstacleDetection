import qi
import argparse
import sys
import time
import almath


def left(session):
    '''
    Moves head to the left.
    '''
    motion_service  = session.service("ALMotion")

    motion_service.setStiffnesses("Head", 1.0)
    
    names      = "HeadYaw"
    angleLists = [30.0*almath.TO_RAD]

    timeLists  = [1.0]
    isAbsolute = True
    motion_service.angleInterpolation(names, angleLists, timeLists, isAbsolute)


    motion_service.setStiffnesses("Head", 0.0)

def right(session):
    '''
    Moves head to the right.
    '''
    motion_service  = session.service("ALMotion")

    motion_service.setStiffnesses("Head", 1.0)

    names      = "HeadYaw"
    angleLists = [-30.0*almath.TO_RAD]

    timeLists  = [1.0]
    isAbsolute = True
    motion_service.angleInterpolation(names, angleLists, timeLists, isAbsolute)


    motion_service.setStiffnesses("Head", 0.0)

def center(session):
    '''
    Moves head to the center.
    '''
    motion_service  = session.service("ALMotion")

    motion_service.setStiffnesses("Head", 1.0)

    names      = "HeadYaw"
    angleLists = [0]

    timeLists  = [1.0]
    isAbsolute = True
    motion_service.angleInterpolation(names, angleLists, timeLists, isAbsolute)


    motion_service.setStiffnesses("Head", 0.0)
