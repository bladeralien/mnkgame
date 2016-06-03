#!/usr/bin/python
#-*- coding: utf-8 -*-


from mdp import MarkovDecisionProcess
from mnkgame import MNKGame
import random


class MNKGameMDP(MarkovDecisionProcess):

    """
    """

    def __init__(self, discount, m, n, k, player):
        super(MNKGameMDP, self).__init__(discount)
        self.m = m
        self.n = n
        self.k = k
        self.player = player

    def start_state(self):
        state = MNKGame(self.m, self.n, self.k)
        if self.player == 'O':
            state = state.state_after_move(random.choice(state.legal_moves()))
        return state

    def actions(self, state):
        return state.legal_moves()

    def terminal(self, state):
        return state.terminal()

    def take_action(self, state, action):
        state = state.state_after_move(action)
        move = random.choice(state.legal_moves())
        state = state.state_after_move(move)
        reward = 0
        if state.winner() == self.player:
            reward = 1
        if state.loser() == self.player:
            reward = -1
        return state, reward

    def states(self):
        pass

    def transition(self, state, action):
        pass

    def reward(self, state, action, next_state):
        pass