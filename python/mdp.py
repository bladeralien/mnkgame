#!/usr/bin/python
#-*- coding: utf-8 -*-


from abc import ABCMeta, abstractmethod


class MarkovDecisionProcess(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def states(self):
        """
        Return a list of all states in the MDP. Not generally possible for
        large MDPs.
        """
        pass

    @abstractmethod
    def start_state(self):
        """
        Return the start state of the MDP.
        """
        pass

    @abstractmethod
    def actions(self, state):
        """
        Return list of possible actions from 'state'.
        """
        pass

    @abstractmethod
    def transition(self, state, action):
        """
        Returns list of (next_state, prob) pairs representing the states
        reachable from 'state' by taking 'action' along with their transition
        probabilities.
        Note that in Q-Learning and reinforcment learning in general, we do
        not know these probabilities nor do we directly model them.
        """
        pass

    @abstractmethod
    def reward(self, state, action, next_state):
        """
        Get the reward for the state, action, next_state transition. Not
        available in reinforcement learning.
        """
        pass

    @abstractmethod
    def terminal(self, state):
        """
        Returns true if the current state is a terminal state. By convention,
        a terminal state has zero future rewards. Sometimes the terminal
        state(s) may have no possible actions.
        It is also common to think of the terminal state as having a self-loop
        action 'pass' with zero reward; the formulations are equivalent.
        """
        pass

    @abstractmethod
    def take_action(self, state, action):
        """
        """
        pass

    def __init__(self, discount=1.0):
        """
        """
        self.discount = discount
        self.qvalues = {}

    def value(self, state):
        """
        Return the value of the state.
        """
        return self.compute_value_from_qvalue(state)

    def qvalue(self, state, action):
        """
        Returns Q(state,action)
        Should return 0.0 if we have never seen a state
        or the Q node value otherwise
        """
        return self.qvalues.get((state, action), 0.0)

    def solve(self, iterations=100):
        """
        Run iteration for a given number of iterations using the supplied
        discount factor.
        """
        for i in range(iterations):
            qvalues = {}
            for state in self.states():
                for action in self.actions(state):
                    qvalue = self.compute_qvalue_from_value(state, action)
                    qvalues[(state, action)] = qvalue
            self.qvalues = qvalues

    def compute_qvalue_from_value(self, state, action):
        """
        Compute the Q-value of action in state from the value function.
        """
        qvalue = 0.0
        for next_state, prob in self.transition(state, action):
            reward = self.reward(state, action, next_state)
            qvalue += prob * (reward + self.discount * self.value(next_state))
        return qvalue

    def compute_value_from_qvalue(self, state):
        """
        Returns max_action Q(state,action) where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
        """
        qvalues = []
        for action in self.actions(state):
            qvalues.append(self.qvalue(state, action))
        if len(qvalues) != 0:
            return max(qvalues)
        else:
            return 0.0

    def policy_extraction(self, state):
        """
        The policy is the best action in the given state according to the
        values currently stored in self.values.
        You may break ties any way you see fit.
        Note that if there are no legal actions, which is the case at the
        terminal state, you should return None.
        """
        qvalues = []
        for action in self.actions(state):
            qvalue = self.qvalue(state, action)
            qvalues.append((action, qvalue))
        if len(qvalues) != 0:
            return max(qvalues, key = lambda item: item[1])[0]
        else:
            return None
