"""
Input handling via keyboard
"""

from twisted.internet.task import LoopingCall
from twisted.internet import reactor
import math

import pygame.event
import pygame.mouse
import pygame.time
import sys

# TODO: Can we have a keymap file?
from pygame import (K_a as ATTACK,
                    K_s as SCAN,
                    K_d as BUILD,
                    K_w as UPGRADE,
                    K_ESCAPE as QUIT,
                    K_DOWN as MOVE_DOWN,
                    K_UP as MOVE_UP,
                    K_LEFT as MOVE_LEFT,
                    K_RIGHT as MOVE_RIGHT,
                    K_z as SWITCH_TEAMS)

from game.vector import Vector2D

class PlayerController(object):
    """
    Input handler for L{game.player.Player} objects.

    @ivar player: The player being controlled.
    @ivar downDirections: List of currently held arrow keys.
    """
    _actions = set([ATTACK, SCAN, BUILD, UPGRADE, SWITCH_TEAMS])

    def __init__(self, perspective, view):
        self.perspective = perspective
        self.position = Vector2D(0, 0)
        self.speed = 10
        self.view = view
        self._actionQueue = []
        self._currentAction = None

        self._movingUp = False
        self._movingDown = False
        self._movingLeft = False
        self._movingRight = False


    def go(self):
        self.previousTime = pygame.time.get_ticks()
        self._inputCall = LoopingCall(self._handleInput)
        d = self._inputCall.start(0.03)
        return d


    def stop(self):
        self._inputCall.stop()


    def _updatePosition(self, dt):
        #if not pygame.mouse.get_focused() or not dt:
        #    return
        if not dt:
            return
        destination = self.view.worldCoord(Vector2D(pygame.mouse.get_pos()))

        directionX = 0
        directionY = 0

        if (self._movingUp):
            directionY = -1
        elif self._movingDown:
            directionY = 1

        if (self._movingLeft):
            directionX = -1
        elif self._movingRight:
            directionX = 1

        direction = Vector2D(directionX, directionY)#destination - self.position
        #if direction < (self.speed * dt):
        #    self.position = destination
        #else:
        #    self.position += (dt * self.speed) * direction.norm()
        if directionX != 0 or directionY != 0:
            self.position += (dt * self.speed) * direction.norm()

        self.perspective.callRemote('updatePosition', self.position)
        #self.view.setCenter(self.position)


    def _startedAction(self, action):

        lastAction = self._currentAction
        self._currentAction = action

        if self._currentAction == SWITCH_TEAMS:
            self.perspective.callRemote("switchTeams")

        if self._currentAction == ATTACK:
            self.perspective.callRemote('startAttacking')
        elif self._currentAction == BUILD:
            self.perspective.callRemote('startBuilding')
        elif self._currentAction == SCAN:
            self.perspective.callRemote('startScanning')
            self.view.addAction("sweep")
        elif self._currentAction == UPGRADE:
            #make upgrade key toggle the upgrade action
            if lastAction != UPGRADE:
                self.perspective.callRemote('startUpgrading')
            else:# lastAction == UPGRADE:
                self.perspective.callRemote('finishUpgrading')
        else:
            self._currentAction = None


    def _finishedAction(self):
        if self._currentAction == ATTACK:
            self.perspective.callRemote('finishAttacking')
        elif self._currentAction == BUILD:
            self.perspective.callRemote('finishBuilding')
        elif self._currentAction == SCAN:
            self.perspective.callRemote('finishScanning')
        #elif self._currentAction == UPGRADE:
        #    self.perspective.callRemote('finishUpgrading')
        self._currentAction = None

        return

    def motionKeyPress(self, key):
        if key == MOVE_UP:
            self._movingUp = True

        if key == MOVE_DOWN:
            self._movingDown = True

        if key == MOVE_LEFT:
            self._movingLeft = True

        if key == MOVE_RIGHT:
            self._movingRight = True


    def motionKeyRelease(self, key):
        if key == MOVE_UP:
            self._movingUp = False

        if key == MOVE_DOWN:
            self._movingDown = False

        if key == MOVE_LEFT:
            self._movingLeft = False

        if key == MOVE_RIGHT:
            self._movingRight = False

    def isMotionKey(self, key):
        return key == MOVE_UP or key == MOVE_DOWN or key == MOVE_LEFT or key == MOVE_RIGHT

    def _handleInput(self):
        """
        Handle currently available pygame input events.
        """
        time = pygame.time.get_ticks()
        self._updatePosition((time - self.previousTime) / 1000.0)
        self.previousTime = time

        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == QUIT)):
                reactor.stop()
                sys.exit()
                
            if (event.type == pygame.KEYDOWN):
                if (event.key in self._actions):
                    self._actionQueue.append(event.key)

                self.motionKeyPress(event.key)


            elif (event.type == pygame.KEYUP):
                self.motionKeyRelease(event.key)
                if (event.key in self._actions):
                    if self._currentAction == event.key:
                        self._finishedAction()
                    else:
                        if not event.key in self._actionQueue:
                            print "mystery key error: " + str(event.key)
                        if event.key in self._actionQueue:
                            self._actionQueue.remove(event.key)

        if (not self._currentAction) and self._actionQueue:
            self._startedAction(self._actionQueue.pop())
