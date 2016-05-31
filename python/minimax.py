#!/usr/bin/python
#-*- coding: utf-8 -*-


from agent import Agent


class MiniMaxAgent(Agent):

    def __init__(self, player, depth=None):
        self.player = player
        self.depth = depth

    def get_move(self, state):
        return self._alpha_beta_pruning(state, self.depth)

    def _alpha_beta_pruning(self, state, depth):
        temp = self._max_value(state, -float('inf'), float('inf'), depth)
        value, move = temp
        return move

    def _max_value(self, state, alpha, beta, depth):
        if state.terminal():
            return state.utility(self), None
        if depth is not None:
            if depth == 0:
                return state.evaluate(self), None
            depth -= 1
        maxmin_value, maxmin_move = -float('inf'), None
        for move in state.legal_moves():
            ts = state.state_after_move(move)
            temp_value, temp_move = self._min_value(ts, alpha, beta, depth)
            if temp_value > maxmin_value:
                maxmin_value, maxmin_move = temp_value, move
            if maxmin_value >= beta:
                return maxmin_value, maxmin_move
            alpha = max(alpha, maxmin_value)
        return maxmin_value, maxmin_move

    def _min_value(self, state, alpha, beta, depth):
        if state.terminal():
            return state.utility(self), None
        if depth is not None:
            if depth == 0:
                return state.evaluate(self), None
            depth -= 1
        minmax_value, minmax_move = float('inf'), None
        for move in state.legal_moves():
            ts = state.state_after_move(move)
            temp_value, temp_move = self._max_value(ts, alpha, beta, depth)
            if temp_value < minmax_value:
                minmax_value, minmax_move = temp_value, move
            if minmax_value <= alpha:
                return minmax_value, minmax_move
            beta = min(beta, minmax_value)
        return minmax_value, minmax_move
