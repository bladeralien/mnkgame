#!/usr/bin/python
#-*- coding: utf-8 -*-


from __future__ import division
import time
import random
from math import log, sqrt
from agent import Agent


class Node(object):

    def __init__(self, state, move=None):
        self.state = state
        self.plays = 0
        self.wins = 0
        self.children = []
        self.parent = None
        self.expanded = set()
        self.move = move

    def add_child(self, node):
        self.children.append(node)
        self.expanded.add(node.move)
        node.parent = self

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        pattern = 'move: {} wins: {} plays: {}'
        return pattern.format(self.move, self.wins, self.plays)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.state == other.state


class MonteCarloAgent(Agent):

    def __init__(self, player, time_limit=3, C=sqrt(2)):
        self.player = player
        self.time_limit = time_limit
        self.C = C
        self.nodes = {}

    def get_move(self, state):
        if state in self.nodes:
            root = self.nodes[state]
        else:
            root = Node(state)
        start = time.time()
        count = 0
        while time.time() - start < self.time_limit:
            selected = self.selection_and_expansion(root)
            result = self.simulation(selected.state)
            self.back_propagation(selected, result)
            count += 1
        for child in root.children:
            print('{}: ({}/{})'.format(child.move, child.wins, child.plays))
        print('{} simulations performed.'.format(count))
        return self.best_move(root)

    def selection_and_expansion(self, root):
        cur_node = root
        while True:
            if cur_node.state.terminal():
                return cur_node
            legal_moves = cur_node.state.legal_moves()
            if len(cur_node.children) < len(legal_moves):
                unexpanded = []
                for move in legal_moves:
                    if move not in cur_node.expanded:
                        unexpanded.append(move)
                assert(len(unexpanded) > 0)
                move = random.choice(unexpanded)
                state = cur_node.state.state_after_move(move)
                child = Node(state, move)
                cur_node.add_child(child)
                self.nodes[state] = child
                return child
            else:
                cur_node = self.best_child(cur_node)
        return cur_node

    def best_child(self, node):
        values = {}
        for child in node.children:
            if node.state.current_player == self.player:
                mean_hat = child.wins / child.plays
            else:
                mean_hat = (child.plays - child.wins) / child.plays
            interval = sqrt(log(node.plays) / child.plays)
            values[child] = mean_hat + self.C * interval
        return max(values, key=values.get)

    def simulation(self, state):
        while True:
            if state.terminal():
                if state.winner() == self.player:
                    return 1
                if state.loser() == self.player:
                    return 0
                return 0.5
            print('in a simulation loop')
            print(state)
            legal_moves = state.legal_moves()
            print(legal_moves)
            move = random.choice(legal_moves)
            print(move)
            state = state.state_after_move(move)

    @staticmethod
    def back_propagation(node, delta):
        while node.parent is not None:
            node.plays += 1
            node.wins += delta
            node = node.parent
        node.plays += 1
        node.wins += delta

    @staticmethod
    def best_move(node):
        temp = [(child.move, child.plays) for child in node.children]
        return max(temp, key = lambda item: item[1])[0]
