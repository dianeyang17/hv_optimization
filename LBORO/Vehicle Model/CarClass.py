#!/usr/bin/python3

###############################
###    IMPORT LIBRARIES     ###
###############################
import time
from PowertrainClass2 import PowertrainControllerClass
from AerodynamicsClass import AerodynamicsClass


class CarClass(object):
    '''Class for an electric vehicle'''
    _powertrain   = None
    _aero_model   = None
    _vehicle_mass = None
    _speed = None

    ###############################
    ###     INITIALISATION      ###
    ###############################
    def __init__(self, kwargs=None):
        if (kwargs is None):
            raise Exception("Must define car data!")
        else:
            self._powertrain   = PowertrainControllerClass(kwargs)
            self._aero_model   = AerodynamicsClass(kwargs)
            self._vehicle_mass = kwargs.get('car_mass')

    ###############################
    ###      UPDATE LOOP        ###
    ###############################
    def update(self, dt):
        self._powertrain.update(dt)

        self._aero_model.update(self._speed)

        total_force = self._powertrain.force - self._aero_model.force

        accn = total_force / self._vehicle_mass
        self.speed = self.speed + accn*dt
        return


    ###############################
    ###     BATTERY CHARGER     ###
    ###############################
    def charge_battery(self, target_soc):
        self._battery.charge_to(target_soc)


    ###############################
    ###        GETTERS          ###
    ###############################

    # Actual vehicle speed
    @property
    def speed(self):
        return self._speed

    # Target speed
    @property
    def target_speed(self,):
        return self._powertrain.target_speed


    # Aerodynamic Load
    @property
    def aero_force(self):
        return self._aero_model.force

    # Road Friction Drag
    @property
    def road_drag(self):
        return self._powertrain.road_drag

    # Powertrain Force
    @property
    def powertrain_force(self):
        return self._powertrain.force


    # Speed Controller PID
    @property
    def speed_ctrl_pid(self):
        return self._powertrain.speed_ctrl_pid

    # Motor Controller PID
    @property
    def motor_ctrl_pid(self):
        return self._powertrain.motor_ctrl_pid

    # Brake Controller PID
    @property
    def brake_ctrl_pid(self):
        return self._powertrain.brake_ctrl_pid


    # Motor Rotational
    @property
    def motor_rotation(self):
        return self._powertrain.motor_rotation

    # Axle Rotation
    @property
    def axle_rotation(self):
        return self._powertrain.axle_rotation

    # Wheel Rotational
    @property
    def wheel_rotation(self):
        return self._powertrain.wheel_rotation


    # Battery Electricity
    @property
    def battery_electricity(self):
        return self._powertrain.battery_elec

    # ESC Electricity
    @property
    def esc_electricity(self):
        return self._powertrain.esc_elec

    # Motor Electricity
    @property
    def motor_electricity(self):
        return self._powertrain.motor_elec


    ###############################
    ###        SETTERS          ###
    ###############################

    # Actual vehicle speed
    @speed.setter
    def speed(self, value):
        if (value <= 0.0): value = 0.0
        self._speed = value
        self._powertrain.speed = value

    # Target speed
    @target_speed.setter
    def target_speed(self, speed):
        self._powertrain.target_speed = speed


###############################
###############################
######       END         ######
###############################
###############################