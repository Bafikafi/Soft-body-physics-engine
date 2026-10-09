import pygame
import consts

GRAVITY_ACCELERATION = 800


def apply_gravity_force(obj):
    obj.velocity.y += GRAVITY_ACCELERATION * consts.DELTA
