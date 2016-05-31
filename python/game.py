#!/usr/bin/python
#-*- coding: utf-8 -*-


from abc import ABCMeta, abstractmethod


class Game(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def legal_moves(self):
        pass

    @abstractmethod
    def state_after_move(self, move):
        pass

    @abstractmethod
    def terminal(self):
        pass

    @abstractmethod
    def winner(self):
        pass

    @abstractmethod
    def loser(self):
        pass

    @abstractmethod
    def utility(self, agent):
        pass

    @abstractmethod
    def evaluate(self, agent):
        pass

    @staticmethod
    def string_to_move(move):
        pass

    @staticmethod
    def play(game, agent):
        while True:
            print(game)
            move = raw_input("input your move:")
            move = game.string_to_move(move)
            if move in game.legal_moves():
                game = game.state_after_move(move)
                print(game)
                if game.terminal():
                    break
                game = game.state_after_move(agent.get_move(game))
                if game.terminal():
                    print(game)
                    break
            else:
                print('illegal move.')
