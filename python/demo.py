class DemoGame(Game):

    transition = {
        'A': {'L': 'B','R': 'Q'},
        'B': {'L': 'C','R': 'J'},
        'C': {'L': 'D','R': 'G'},
        'D': {'L': 'E','R': 'F'},
        'E': {},
        'F': {},
        'G': {'L': 'H','R': 'I'},
        'H': {},
        'I': {},
        'J': {'L': 'K','R': 'N'},
        'K': {'L': 'L','R': 'M'},
        'L': {},
        'M': {},
        'N': {'L': 'O','R': 'P'},
        'O': {},
        'P': {},
        'Q': {'L': 'R','R': 'Z'},
        'R': {'L': 'S','R': 'V'},
        'S': {'L': 'T','R': 'U'},
        'T': {},
        'U': {},
        'V': {'L': 'W','R': 'X'},
        'W': {},
        'X': {},
        'Z': {'L': 'Z1','R': 'Z4'},
        'Z1': {'L': 'Z2','R': 'Z3'},
        'Z2': {},
        'Z3': {},
        'Z4': {'L': 'Z5','R': 'Z6'},
        'Z5': {},
        'Z6': {},
    }

    terminals = {
        'E': 10,
        'F': 11,
        'H': 9,
        'I': 12,
        'L': 14,
        'M': 15,
        'O': 13,
        'P': 14,
        'T': 15,
        'U': 2,
        'W': 4,
        'X': 1,
        'Z2': 3,
        'Z3': 22,
        'Z5': 24,
        'Z6': 25,
    }

    def __init__(self, id):
        self.id = id

    def legal_moves(self):
        if len(DemoGame.transition[self.id]) == 2:
            return ['L', 'R']
        return []

    def state_after_move(self, move):
        return DemoGame(DemoGame.transition[self.id][move])

    def terminal(self):
        return self.id in DemoGame.terminals

    def utility(self):
        return DemoGame.terminals[self.id]

    def evaluate(self):
        pass

    def __str__(self):
        return self.id


if __name__ == '__main__':

    game = DemoGame('A')
    print(alpha_beta_pruning(game, 4))