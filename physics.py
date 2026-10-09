import pygame
import consts

GRAVITY_ACCELERATION = 2


def apply_gravity_force(obj):
    obj.velocity.y += GRAVITY_ACCELERATION * consts.DELTA
