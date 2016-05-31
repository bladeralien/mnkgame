#!/usr/bin/python
#-*- coding: utf-8 -*-


from abc import ABCMeta, abstractmethod


class Agent(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, state, player):
        pass

    @abstractmethod
    def get_move(self, state):
        pass
