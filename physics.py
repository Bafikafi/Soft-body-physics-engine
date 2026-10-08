import pygame
import consts

GRAVITY_ACCELERATION = 9.8


def apply_gravity_force(obj):
    vel = list(obj.velocity)
    vel[1] += GRAVITY_ACCELERATION * consts.DELTA
    print(vel[1])
    obj.velocity = tuple(vel)
