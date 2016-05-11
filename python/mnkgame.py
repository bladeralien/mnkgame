#!/usr/bin/python
#-*- coding: utf-8 -*-


from copy import deepcopy
import sys
sys.path.append('../../')
from game import Game, alpha_beta_pruning


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

    def terminal(self):
        pattern = [player * self.k for player in MNKGame.players]
        for i in range(self.m):
            for j in range(self.n + 1 - self.k):
                temp = self.pieces[i][j: j + self.k]
                temp = [p if p is not None else '-' for p in temp]
                if ''.join(temp) in pattern:
                    return True
        for j in range(self.n):
            for i in range(self.m + 1 - self.k):
                temp = [self.pieces[i + c][j] for c in range(self.k)]
                temp = [p if p is not None else '-' for p in temp]
                if ''.join(temp) in pattern:
                    return True
        for i in range(self.m + 1 - self.k):
            for j in range(self.n + 1 - self.k):
                temp = [self.pieces[i + c][j + c] for c in range(self.k)]
                temp = [p if p is not None else '-' for p in temp]
                if ''.join(temp) in pattern:
                    return True
        for i in range(self.k - 1, self.m):
            for j in range(self.n + 1 - self.k):
                temp = [self.pieces[i - c][j + c] for c in range(self.k)]
                temp = [p if p is not None else '-' for p in temp]
                if ''.join(temp) in pattern:
                    return True

    def utility(self):
        if self.terminal():
            # Hard Coding
            if self.current_player == 'X':
                return 1
            else:
                return 0

    def evaluate(self):
        if not self.terminal():
            return 0.5

    @classmethod
    def read_move_from_raw_input(cls):
        move = raw_input("input your move:")
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

    # TicTacToe
    # game = MNKGame(3, 3, 3)
    # Gomoku
    game = MNKGame(19, 19, 5)
    MNKGame.play(game, 3)
