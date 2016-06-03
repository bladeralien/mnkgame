#!/usr/bin/python
#-*- coding: utf-8 -*-


from math import e
from copy import deepcopy
from game import Game
from minimax import MiniMaxAgent
from mcts import MonteCarloAgent
from human import HumanAgent


class MNKGame(Game):

    # Xs and Os
    players = ('X', 'O')

    def __init__(self, m, n, k, pieces=None, current_player='X'):
        assert(m >= 3 and n >= 3 and k >= 3)
        assert(m >= k or n >= k)
        self.m = m
        self.n = n
        self.k = k
        if pieces == None:
            self.pieces = []
            for i in range(self.m):
                self.pieces.append([])
                for j in range(self.n):
                    self.pieces[-1].append(None)
        else:
            self.pieces = pieces
        assert(current_player in MNKGame.players)
        self.current_player = current_player

    def legal_moves(self):
        moves = []
        for i in range(self.m):
            for j in range(self.n):
                if self.pieces[i][j] is None:
                    moves.append((i, j))
        return moves

    def state_after_move(self, move):
        # Deepcopy
        i, j = move
        pieces = deepcopy(self.pieces)
        current_player = self.current_player
        pieces[i][j] = current_player
        # Hard Coding
        current_player = 'O' if current_player == 'X' else 'X'
        return MNKGame(self.m, self.n, self.k, pieces, current_player)

    def _terminal_helper(self):
        patterns = [player * self.k for player in MNKGame.players]
        for i in range(self.m):
            for j in range(self.n + 1 - self.k):
                temp = self.pieces[i][j: j + self.k]
                temp = [p if p is not None else '-' for p in temp]
                temp = ''.join(temp)
                for pattern in patterns:
                    if pattern == temp:
                        return pattern[0]
        for j in range(self.n):
            for i in range(self.m + 1 - self.k):
                temp = [self.pieces[i + c][j] for c in range(self.k)]
                temp = [p if p is not None else '-' for p in temp]
                temp = ''.join(temp)
                for pattern in patterns:
                    if pattern == temp:
                        return pattern[0]
        for i in range(self.m + 1 - self.k):
            for j in range(self.n + 1 - self.k):
                temp = [self.pieces[i + c][j + c] for c in range(self.k)]
                temp = [p if p is not None else '-' for p in temp]
                temp = ''.join(temp)
                for pattern in patterns:
                    if pattern == temp:
                        return pattern[0]
        for i in range(self.k - 1, self.m):
            for j in range(self.n + 1 - self.k):
                temp = [self.pieces[i - c][j + c] for c in range(self.k)]
                temp = [p if p is not None else '-' for p in temp]
                temp = ''.join(temp)
                for pattern in patterns:
                    if pattern == temp:
                        return pattern[0]
        if self.legal_moves() == []:
            return 'T'

    def terminal(self):
        if self._terminal_helper() in ('X', 'O', 'T'):
            return True
        return False

    def winner(self):
        temp = self._terminal_helper()
        if temp in ('X', 'O'):
            return temp

    def loser(self):
        temp = self._terminal_helper()
        if temp in ('X', 'O'):
            return 'O' if temp == 'X' else 'X'

    def utility(self, agent):
        if self.terminal():
            if self.current_player != agent.player:
                return 1
            else:
                return 0

    def evaluate(self, agent):
        if not self.terminal():
            score = 0
            opponent = 'O' if agent.player == 'X' else 'X'
            for i in range(self.m):
                for j in range(self.n + 1 - self.k):
                    temp = self.pieces[i][j: j + self.k]
                    score += temp.count(agent.player) - temp.count(opponent)
            for j in range(self.n):
                for i in range(self.m + 1 - self.k):
                    temp = [self.pieces[i + c][j] for c in range(self.k)]
                    score += temp.count(agent.player) - temp.count(opponent)
            for i in range(self.m + 1 - self.k):
                for j in range(self.n + 1 - self.k):
                    temp = [self.pieces[i + c][j + c] for c in range(self.k)]
                    score += temp.count(agent.player) - temp.count(opponent)
            for i in range(self.k - 1, self.m):
                for j in range(self.n + 1 - self.k):
                    temp = [self.pieces[i - c][j + c] for c in range(self.k)]
                    score += temp.count(agent.player) - temp.count(opponent)
            score = 1 / (1 + e ** score)
            return score

    @staticmethod
    def string_to_move(move):
        i, j = [int(x) for x in move.split(',')]
        return (i, j)

    def __str__(self):
        lines = []
        lines.append(self.current_player + '\'s turn to move.')
        for i in range(self.m):
            line = [p if p is not None else '-' for p in self.pieces[i]]
            lines.append(''.join(line))
        return '\n'.join(lines)

    def __eq__(self, other):
        """
        Overloads '==' such that two game with the same configuration
        are equal.
        """
        return self.__str__() == other.__str__()

    def __hash__(self):
        return hash(self.__str__())


if __name__ == '__main__':

    game = MNKGame(3, 3, 3) # TicTacToe
    # game = MNKGame(19, 19, 5) # Gomoku
    # agent = MiniMaxAgent('O', 3)
    agent1 = HumanAgent('X')
    agent2 = MonteCarloAgent('O', 5)
    MNKGame.play(game, agent1, agent2)
