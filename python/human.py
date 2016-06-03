#!/usr/bin/python
#-*- coding: utf-8 -*-


from agent import Agent


class HumanAgent(Agent):

    """
    """

    def __init__(self, player):
        """
        """
        self.player = player

    def get_move(self, state):
        """
        """
        while True:
            move = raw_input("input your move:")
            move = state.string_to_move(move)
            if move in state.legal_moves():
                return move
            else:
                print('illegal move.')
