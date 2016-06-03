#!/usr/bin/python
#-*- coding: utf-8 -*-


from abc import ABCMeta, abstractmethod
import random
import pickle
from agent import Agent
from feature_extractors import IdentityExtractor, MNKGameSimpleExtractor


class QLearningAgent(Agent):

    """
    Q-Learning Agent.
    Estimates Q-Values (as well as policies) from experience rather than a
    model.
    """

    def __init__(self, mdp, alpha=0.5, epsilon=0.5, episodes=100):
        """
        """
        self.mdp = mdp
        self.alpha = alpha
        self.epsilon = epsilon
        self.episodes = episodes

    def pick_action(self, state):
        """
        Compute the action to take in the current state. With probability
        self.epsilon, we should take a random action and take the best policy
        action otherwise.
        Note that if there are no legal actions, which is the case at the
        terminal state, you should choose None as the action.
        """
        actions = self.mdp.actions(state)
        if random.random() < self.epsilon:
            if len(actions) != 0:
                return random.choice(actions)
            else:
                return None
        else:
            return self.mdp.policy_extraction(state)

    def update(self, state, action, next_state, reward):
        """
        The parent class calls this to observe a
        state, action => next_state and reward transition.
        You should do your Q-Value update here.
        """
        value = self.mdp.value(next_state)
        sample = reward + self.mdp.discount * value
        qvalue = self.mdp.qvalue(state, action)
        temp = (1 - self.alpha) * qvalue + self.alpha * sample
        self.mdp.qvalues[(state, action)] = temp

    def learning(self):
        """
        """
        for episode in range(self.episodes):
            print('learning episode ' + str(episode))
            state = self.mdp.start_state()
            while not self.mdp.terminal(state):
                action = self.pick_action(state)
                next_state, reward = self.mdp.take_action(state, action)
                self.update(state, action, next_state, reward)
                state = next_state
        print(len(self.mdp.qvalues))

    def get_move(self, state):
        """
        """
        return self.mdp.policy_extraction(state)

    def serialize(self, filename='mdp.pkl'):
        """
        """
        pickle.dump(self.mdp, open(filename, 'wb'))

    def deserialize(self, filename='mdp.pkl'):
        """
        """
        self.mdp = pickle.load(open(filename, 'rb'))


class ApproximateQLearningAgent(QLearningAgent):

    """
    ApproximateQLearningAgent
    """

    def __init__(self, mdp, alpha=0.5, epsilon=0.5, episodes=100, feature_extractor=IdentityExtractor()):
        QLearningAgent.__init__(self, mdp, alpha, epsilon, episodes)
        self.feature_extractor = feature_extractor
        self.weights = {}

    def estimate_and_set_qvalue(self, state, action):
        """
        Should return Q(state,action) = weights * features
        where * is the dot product operator
        """
        features = self.feature_extractor.extract_features(state, action)
        qvalue = 0
        for f in features:
            qvalue += self.weights.get(f, 0.0) * features[f]
        self.mdp.qvalues[(state, action)] = qvalue
        return qvalue

    def update(self, state, action, next_state, reward):
        """
        Should update your weights based on transition
        """
        qvalue = self.estimate_and_set_qvalue(state, action)
        value = self.mdp.compute_value_from_qvalue(next_state)
        difference = reward + self.mdp.discount * value - qvalue
        features = self.feature_extractor.extract_features(state, action)
        for f in features:
            self.weights.setdefault(f, 0.0)
            self.weights[f] += self.alpha * difference * features[f]
        print(value)
        print(qvalue)
        print(self.alpha)
        print(difference)
        print(features)
        print(self.weights)

    def serialize(self, filename='weights.pkl'):
        """
        """
        pickle.dump([self.mdp, self.weights], open(filename, 'wb'))

    def deserialize(self, filename='weights.pkl'):
        """
        """
        self.mdp, self.weights = pickle.load(open(filename, 'rb'))


if __name__ == '__main__':

    from mnkgame import MNKGame
    from mdp_mnkgame import MNKGameMDP
    from sys import argv
    script, phase = argv
    if phase == 'train':
        agent = ApproximateQLearningAgent(MNKGameMDP(0.99, 3, 3, 3,'O'), episodes=10000, feature_extractor=MNKGameSimpleExtractor())
        agent.learning()
        agent.serialize()
        print(agent.weights)
    if phase == 'test':
        agent = ApproximateQLearningAgent(MNKGameMDP(0.99, 3, 3, 3,'O'), episodes=10000, feature_extractor=MNKGameSimpleExtractor())
        agent.deserialize()
        print(agent.weights)
    game = MNKGame(3, 3, 3) # Mini Gomoku
    MNKGame.play(game, agent)


#     ###################
#     # Pacman Specific #
#     ###################
#     def observationFunction(self, state):
#         """
#             This is where we ended up after our last action.
#             The simulation should somehow ensure this is called
#         """
#         if not self.lastState is None:
#             reward = state.getScore() - self.lastState.getScore()
#             self.observeTransition(self.lastState, self.lastAction, state, reward)
#         return state

#     def registerInitialState(self, state):
#         self.startEpisode()
#         if self.episodesSoFar == 0:
#             print 'Beginning %d episodes of Training' % (self.numTraining)

#     def final(self, state):
#         """
#           Called by Pacman game at the terminal state
#         """
#         deltaReward = state.getScore() - self.lastState.getScore()
#         self.observeTransition(self.lastState, self.lastAction, state, deltaReward)
#         self.stopEpisode()

#         # Make sure we have this var
#         if not 'episodeStartTime' in self.__dict__:
#             self.episodeStartTime = time.time()
#         if not 'lastWindowAccumRewards' in self.__dict__:
#             self.lastWindowAccumRewards = 0.0
#         self.lastWindowAccumRewards += state.getScore()

#         NUM_EPS_UPDATE = 100
#         if self.episodesSoFar % NUM_EPS_UPDATE == 0:
#             print 'Reinforcement Learning Status:'
#             windowAvg = self.lastWindowAccumRewards / float(NUM_EPS_UPDATE)
#             if self.episodesSoFar <= self.numTraining:
#                 trainAvg = self.accumTrainRewards / float(self.episodesSoFar)
#                 print '\tCompleted %d out of %d training episodes' % (
#                        self.episodesSoFar,self.numTraining)
#                 print '\tAverage Rewards over all training: %.2f' % (
#                         trainAvg)
#             else:
#                 testAvg = float(self.accumTestRewards) / (self.episodesSoFar - self.numTraining)
#                 print '\tCompleted %d test episodes' % (self.episodesSoFar - self.numTraining)
#                 print '\tAverage Rewards over testing: %.2f' % testAvg
#             print '\tAverage Rewards for last %d episodes: %.2f'  % (
#                     NUM_EPS_UPDATE,windowAvg)
#             print '\tEpisode took %.2f seconds' % (time.time() - self.episodeStartTime)
#             self.lastWindowAccumRewards = 0.0
#             self.episodeStartTime = time.time()

#         if self.episodesSoFar == self.numTraining:
#             msg = 'Training Done (turning off epsilon and alpha)'
#             print '%s\n%s' % (msg,'-' * len(msg))
#     def startEpisode(self):
#         """
#           Called by environment when new episode is starting
#         """
#         self.lastState = None
#         self.lastAction = None
#         self.episodeRewards = 0.0
# .
#     def stopEpisode(self):
#         """
#           Called by environment when episode is done
#         """
#         if self.episodesSoFar < self.numTraining:
#             self.accumTrainRewards += self.episodeRewards
#         else:
#             self.accumTestRewards += self.episodeRewards
#         self.episodesSoFar += 1
#         if self.episodesSoFar >= self.numTraining:
#             # Take off the training wheels
#             self.epsilon = 0.0    # no exploration
#             self.alpha = 0.0      # no learning

#     def isInTraining(self):
#         return self.episodesSoFar < self.numTraining

#     def isInTesting(self):
#         return not self.isInTraining()
#     def observe_transition(self, state, action, next_state, deltaReward):
#         """
#         Called by environment to inform agent that a transition has
#         been observed. This will result in a call to self.update
#         on the same arguments
#         """
#         self.episodeRewards += deltaReward
#         self.update(state,action,nextState,deltaReward)
