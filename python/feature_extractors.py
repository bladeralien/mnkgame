#!/usr/bin/python
#-*- coding: utf-8 -*-


class FeatureExtractor(object):
    def extract_features(self, state, action):
        """
        Returns a dict from features to counts. Usually, the count will just
        be 1.0 for indicator functions.
        """
        pass


class IdentityExtractor(FeatureExtractor):
    def extract_features(self, state, action):
        features = {}
        features[(state,action)] = 1.0
        return features


class MNKGameSimpleExtractor(FeatureExtractor):
    def extract_features(self, state, action):
        features = {}
        for i in range(state.m):
            for j in range(state.n):
                features[(i, j)] = 0
                if state.pieces[i][j] == state.current_player:
                    features[(i, j)] = 1
                elif state.pieces[i][j] is not None:
                    features[(i, j)] = -1
        features[action] = 1
        for f in features:
            features[f] /= 10.0
        return features


# class MNKGameSimpleExtractor(FeatureExtractor):
#     def extract_features(self, state, action):
#         current_player = state.current_player
#         state = state.state_after_move(action)
#         features = {}
#         if state.pieces[1][1] == current_player:
#             features['center'] = 1
#         elif state.pieces[1][1] is not None:
#             features['center'] = -1
#         for i, j in [(0, 0), (0, 2), (2, 0), (2, 2)]:
#             if state.pieces[i][j] == current_player:
#                 features.setdefault('corner', 0)
#                 features['corner'] += 1
#             elif state.pieces[i][j] is not None:
#                 features.setdefault('corner', 0)
#                 features['corner'] -= 1
#         for i, j in [(0, 1), (1, 0), (1, 2), (2, 1)]:
#             if state.pieces[i][j] == current_player:
#                 features.setdefault('edge', 0)
#                 features['edge'] += 1
#             elif state.pieces[i][j] is not None:
#                 features.setdefault('edge', 0)
#                 features['edge'] -= 1
        # for f in features:
        #     features[f] /= 10.0
        # for i in range(state.m):
        #     for j in range(state.n):
        #         features[(i, j)] = 0

        #         if state.pieces[i][j] == state.current_player:
        #             features[(i, j)] = 1
        #         elif state.pieces[i][j] is not None:
        #             features[(i, j)] = -1
        # features[action] = 1
        return features


# class CoordinateExtractor(FeatureExtractor):
#     def getFeatures(self, state, action):
#         feats = util.Counter()
#         feats[state] = 1.0
#         feats['x=%d' % state[0]] = 1.0
#         feats['y=%d' % state[0]] = 1.0
#         feats['action=%s' % action] = 1.0
#         return feats

# def closestFood(pos, food, walls):
#     """
#     closestFood -- this is similar to the function that we have
#     worked on in the search project; here its all in one place
#     """
#     fringe = [(pos[0], pos[1], 0)]
#     expanded = set()
#     while fringe:
#         pos_x, pos_y, dist = fringe.pop(0)
#         if (pos_x, pos_y) in expanded:
#             continue
#         expanded.add((pos_x, pos_y))
#         # if we find a food at this location then exit
#         if food[pos_x][pos_y]:
#             return dist
#         # otherwise spread out from the location to its neighbours
#         nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
#         for nbr_x, nbr_y in nbrs:
#             fringe.append((nbr_x, nbr_y, dist+1))
#     # no food found
#     return None

# class SimpleExtractor(FeatureExtractor):
#     """
#     Returns simple features for a basic reflex Pacman:
#     - whether food will be eaten
#     - how far away the next food is
#     - whether a ghost collision is imminent
#     - whether a ghost is one step away
#     """

#     def getFeatures(self, state, action):
#         # extract the grid of food and wall locations and get the ghost locations
#         food = state.getFood()
#         walls = state.getWalls()
#         ghosts = state.getGhostPositions()

#         features = util.Counter()

#         features["bias"] = 1.0

#         # compute the location of pacman after he takes the action
#         x, y = state.getPacmanPosition()
#         dx, dy = Actions.directionToVector(action)
#         next_x, next_y = int(x + dx), int(y + dy)

#         # count the number of ghosts 1-step away
#         features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)

#         # if there is no danger of ghosts then add the food feature
#         if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
#             features["eats-food"] = 1.0

#         dist = closestFood((next_x, next_y), food, walls)
#         if dist is not None:
#             # make the distance a number less than one otherwise the update
#             # will diverge wildly
#             features["closest-food"] = float(dist) / (walls.width * walls.height)
#         features.divideAll(10.0)
#         return features
