#!/usr/bin/python3

###############################
###    IMPORT LIBRARIES     ###
###############################
import math
import abc


###############################
###    UTILITY FUNCTIONS    ###
###############################

# Convert rpm to radians/sec
def rpm_to_rads(rpm:'Revolutions per minute') -> 'Radians/second':
    return rpm / 60.0 * (2.0 * math.pi)

# Convert radians/sec to rpm
def rads_to_rpm(rads:'Radians/second') -> 'Revolutions per minute':
    return rads * 60.0 / (2.0 * math.pi)


class RotatingThingData(object):
    '''Class describing the data of a rotating object'''
    _key_torque = 'torque'
    _key_speed  = 'speed'
    _torque     = 0.0
    _speed      = 0.0

    ###############################
    ###     INITIALISATION      ###
    ###############################
    def __init__(self):
        return 


    ###############################
    ###        GETTERS          ###
    ###############################

    # Interesting rotational object data
    @property
    def rotational_data(self):
        return {self._key_torque : self._torque, self._key_speed : self._speed}

    # Torque
    @property
    def torque(self):
        return self._torque

    # Angular speed
    @property
    def speed(self):
        return self._speed

    # Python dict key for torque
    @property
    def key_torque(self):
        return self._key_torque

    # Python dict key for angular speed
    @property
    def key_speed(self):
        return self._key_speed


    ###############################
    ###        SETTERS          ###
    ###############################
    
    # Interesting rotational object data
    @rotational_data.setter
    def rotational_data(self, data_dict):
        self._torque = data_dict.get(self._key_torque)
        self._speed  = data_dict.get(self._key_speed)

    # Torque
    @torque.setter
    def torque(self, tq):
        self._torque = tq

    # Angular speed
    @speed.setter
    def speed(self, rad_sec):
        self._speed = rad_sec


###############################
###############################
######       END         ######
###############################
###############################


class RotatingThingClass(abc.ABC, RotatingThingData):
    '''Abstract base class describing the mechanics of a basic rotating object'''
    _w_last        = 0.0
    _p             = 0.0
    _dt            = 0.0
    _diameter      = None
    _area          = None
    _mass          = None
    _circumference = None

    ###############################
    ###     INITIALISATION      ###
    ###############################
    def __init__(self, kwargs):
        self._diameter      = kwargs.get('diameter')
        self._area          = kwargs.get('area', (math.pi * (self._diameter / 2.0)**2) if self._diameter is not None else None)
        self._mass          = kwargs.get('mass')
        self._circumference = math.pi * self._diameter if self._diameter is not None else None

        super(abc.ABC, self).__init__()

        return super(RotatingThingData, self).__init__()


    ###############################
    ###      UPDATE LOOP        ###
    ###############################
    def update(self, dt):
        self._dt = dt
        self.torque -=  self.inertia_torque_x
        return None


    ###############################
    ###        GETTERS          ###
    ###############################

    # Object diameter
    @property
    def diameter(self):
        return self._diameter

    # Object radius
    @property
    def radius(self):
        return self._diameter / 2.0

    # Object reference area
    @property
    def area(self):
        return self._area

    # Object reference mass
    @property
    def mass(self):
        return self._mass

    # Mechanical power
    @property
    def power(self):
        return self.torque * self.speed

    # Torque
#    @property
#    def torque(self):
#        return super(RotatingThingClass, self).torque

    # Angular speed
    #@property
    #def speed(self):
    #    return super(RotatingThingClass, self).speed

    # Force
    @property
    def force(self):
        return self.torque * self.radius

    # Moment of inertia (x axis) [ABSTRACT]
    @property
    @abc.abstractmethod
    def inertia_x(self):
        return 'Should never reach here'

    # Inertial torque
    @property
    def inertia_torque_x(self):
        try:
            return self.inertia_x * ( self.speed - self._w_last ) / self._dt
        except ZeroDivisionError:
            return 0.0


    ###############################
    ###        SETTERS          ###
    ###############################

    # Torque
    @RotatingThingData.torque.setter
    def torque(self, tq):
        self._torque = tq

    # Angular speed
    @RotatingThingData.speed.setter
    def speed(self, rad_sec):
        if (rad_sec < 0.0):
            print("Rotational speed cannot be negative")
            raise ValueError
            return None
        self._w_last = self._speed
        self._speed = rad_sec


###############################
###############################
######       END         ######
###############################
###############################


class RotatingDiscClass(RotatingThingClass):
    '''Class for a rotating disc'''

    ###############################
    ###     INITIALISATION      ###
    ###############################
    def __init__(self, kwargs):
        return super().__init__(kwargs)


    ###############################
    ###        GETTERS          ###
    ###############################
    @property
    def inertia_x(self):
        return (self.mass * self.radius**2) / 2.0


###############################
###############################
######       END         ######
###############################
###############################


class RotatingCylinderClass(RotatingThingClass):
    '''Class for a rotating solid cylinder'''
    _length = None

    ###############################
    ###     INITIALISATION      ###
    ###############################
    def __init__(self, kwargs):
        self._length = kwargs.get('length')
        return super().__init__(kwargs)


    ###############################
    ###        GETTERS          ###
    ###############################

    # Moment of inertia (x axis)
    @property
    def inertia_x(self):
        return (self.mass * self.radius**2) / 2.0

    # Cylinder length (height)
    @ property
    def length(self):
        return self._length


###############################
###############################
######       END         ######
###############################
###############################


class RotatingCylinderShellClass(RotatingThingClass):
    '''Class for a rotating thin walled cylinder'''
    _length = None

    ###############################
    ###     INITIALISATION      ###
    ###############################
    def __init__(self, kwargs):
        self._length = kwargs['length'] if 'length' in kwargs else None
        return super().__init__(kwargs)


    ###############################
    ###        GETTERS          ###
    ###############################

    # Moment of inertia (x axis)
    @property
    def inertia_x(self):
        return self.mass * self.length**2

    # Cylinder length (height)
    @ property
    def length(self):
        return self._length


###############################
###############################
######       END         ######
###############################
###############################