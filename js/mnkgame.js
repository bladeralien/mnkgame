function alphaBetaPruning(state, depth) {
    return maxValue(state, -Infinity, Infinity, depth)[1];
}


function maxValue(state, alpha, beta, depth) {
    if (state.terminal()) {
        return [state.utility(), undefined];
    }
    if (depth != undefined) {
        if (depth == 0) {
            return [state.evaluate(), undefined];
        }
        depth -= 1;
    }
    var maxminValue = -Infinity, maxminMove = undefined;
    var legalMoves = state.legalMoves();
    for (var i = 0; i < legalMoves.length; i++) {
        var move = legalMoves[i];
        temp = minValue(state.stateAfterMove(move), alpha, beta, depth)[0];
        if (temp > maxminValue) {
            maxminValue = temp;
            maxminMove = move;
        }
        if (maxminValue >= beta) {
            return [maxminValue, maxminMove];
        }
        alpha = Math.max(alpha, maxminValue);
    }
    return [maxminValue, maxminMove];
}


function minValue(state, alpha, beta, depth) {
    console.log(state);
    if (state.terminal()) {
        return [state.utility(), undefined];
    }
    if (depth != undefined) {
        if (depth == 0) {
            return [state.evaluate(), undefined];
        }
        depth -= 1;
    }
    var minmaxValue = Infinity, minmaxMove = undefined;
    var legalMoves = state.legalMoves();
    for (var i = 0; i < legalMoves.length; i++) {
        var move = legalMoves[i];
        temp = maxValue(state.stateAfterMove(move), alpha, beta, depth)[0]
        if (temp < minmaxValue) {
            minmaxValue = temp;
            minmaxMove = move;
        }
        if (minmaxValue <= alpha) {
            return [minmaxValue, minmaxMove];
        }
        beta = Math.min(beta, minmaxValue);
    }
    return [minmaxValue, minmaxMove];
}


var Game = function() {

};
Game.prototype.legalMoves = function() {
    // body...
};
Game.prototype.stateAfterMove = function(move) {
    // body...
};
Game.prototype.terminal = function() {
    // body...
};
Game.prototype.utility = function() {
    // body...
};
Game.prototype.evaluate = function() {
    // body...
};
Game.inputMove = function() {
    // body...
    var move;
    var prompt = require('prompt');

    prompt.start();

    prompt.get(['move'], function(err, result) {
        if (err) {
            return onErr(err); }
        move = result.move;
        move = move.trim().split(',').map(function(val) {
            return parseInt(val);
        })
        console.log(move);
        return move;
    });

    function onErr(err) {
        console.log(err);
        return 1;
    }
    // var readline = require('readline');
    // var rl = readline.createInterface(process.stdin, process.stdout);
    // rl.setPrompt('input your move:');
    // rl.prompt();
    // rl.on('line', function(line) {
    //     move = line;
    //     rl.close();
    // });
    // move

    // return move;
};
Game.play = function(game, depth) {

    console.log(game);

    var readline = require('readline');
    var rl = readline.createInterface({
        input:process.stdin, output:process.stdout
    });
    rl.setPrompt('input your move:');
    rl.prompt();

    rl.on('line', function(line) {
        var move = line.trim().split(',').map(function(val) {
            return parseInt(val);
        })
        console.log(move);
        legalMovesStr = game.legalMoves().map(function(arr) {
            return arr.toString();
        });

        if (legalMovesStr.indexOf(move.toString()) != -1) {

            game = game.stateAfterMove(move)
            console.log(game)

            if (game.terminal()) {
                rl.close();
            }

            game = game.stateAfterMove(alphaBetaPruning(game, depth));
            console.log(game)

            if (game.terminal()) {
                rl.close();
            }
        } else {
            console.log('invalid move.')
        }
        rl.prompt();
    });
    rl.on('close', function() {
        process.exit(0);
    });



    // while (true) {
    //     console.log(game)
    //     move = Game.inputMove()
    //     console.log('move from input');
    //     console.log(move);
    //     if (move in game.legalMoves()) {
    //         game = game.stateAfterMove(move)
    //     }
    //     console.log(game)
    //     if (game.terminal()) {
    //         break;
    //     }

    //     game = game.stateAfterMove(alphaBetaPruning(game, depth))
    //     if (game.terminal()) {
    //         break;
    //     } else {
    //         console.log('invalid move.');
    //     }

    // }

};

var range = function(k) {
    return Array.apply(null, Array(k)).map(function(_, i) {
        return i; });
}

String.prototype.repeat = function(count) {
    if (count < 1) return '';
    var result = '',
        pattern = this.valueOf();
    while (count > 1) {
        if (count & 1) result += pattern;
        count >>= 1, pattern += pattern;
    }
    return result + pattern;
};

var jQuery = require('jQuery');

var MNKGame = function(m, n, k, pieces, currentPlayer) {
    this.m = m;
    this.n = n;
    this.k = k;
    if (pieces == undefined) {
        this.pieces = [];
        for (var i = 0; i < this.m; i++) {
            this.pieces.push([]);
            for (var j = 0; j < this.n; j++) {
                this.pieces[i].push(undefined);
            };
        };
    } else {
        this.pieces = pieces;
    }
    if (currentPlayer == undefined) {
        this.currentPlayer = 'X';
    } else {
        this.currentPlayer = currentPlayer;
    }
}
MNKGame.prototype.__proto__ = Game.prototype;

MNKGame.players = ['X', 'O'];

MNKGame.prototype.legalMoves = function() {
    var moves = [];
    for (var i = 0; i < this.m; i++) {
        for (var j = 0; j < this.n; j++) {
            if (this.pieces[i][j] == undefined) {
                moves.push([i, j]);
            };
        };
    };
    return moves;
};

MNKGame.prototype.stateAfterMove = function(move) {
    console.log('enter stateAfterMove');
    var i = move[0], j = move[1];
    // var pieces = this.pieces;
    var pieces = jQuery.extend(true, {}, this.pieces);
    var currentPlayer = this.currentPlayer;
    console.log(move);
    console.log(pieces);
    console.log(currentPlayer);
    pieces[i][j] = currentPlayer;
    currentPlayer = currentPlayer == 'X' ? 'O' : 'X';
    console.log(pieces);
    console.log(currentPlayer);
    var newobj = new MNKGame(this.m, this.n, this.k, pieces, currentPlayer)
    console.log('leave stateAfterMove');
    return newobj;
};

MNKGame.prototype.terminal = function() {
    var pattern = MNKGame.players.map(function(player) {
        return player.repeat(this.k);
    });
    for (var i = 0; i < this.m; i++) {
        for (var j = 0; j < this.n + 1 - this.k; j++) {
            var temp = this.pieces[i].slice(j, j + this.k);
            temp = temp.map(function(p) {
                return p != undefined ? p : '-';
            });
            if (pattern.indexOf(temp.join('')) != -1) {
                return true;
            };
        };
    };
    for (var j = 0; j < this.n; j++) {
        for (var i = 0; i < this.m + 1 - this.k; i++) {
            var that = this;
            var temp = range(this.k).map(function(c) {
                return that.pieces[i + c][j]
            });
            temp = temp.map(function(p) {
                return p != undefined ? p : '-';
            });
            if (pattern.indexOf(temp.join('')) != -1) {
                return true;
            };
        };
    };
    for (var i = 0; i < this.m + 1 - this.k; i++) {
        for (var j = 0; j < this.n + 1 - this.k; j++) {
            var that = this;
            var temp = range(this.k).map(function(c) {
                return that.pieces[i + c][j + c]
            });
            temp = temp.map(function(p) {
                return p != undefined ? p : '-';
            });
            if (pattern.indexOf(temp.join('')) != -1) {
                return true;
            };
        };
    };
    for (var i = this.k - 1; i < this.m; i++) {
        for (var j = 0; j < this.n + 1 - this.k; j++) {
            var that = this;
            var temp = range(this.k).map(function(c) {
                return that.pieces[i - c][j + c]
            });
            temp = temp.map(function(p) {
                return p != undefined ? p : '-';
            });
            if (pattern.indexOf(temp.join('')) != -1) {
                return true;
            };
        };
    };
};

MNKGame.prototype.utility = function() {
    if (this.terminal()) {
        return this.current_player == 'X' ? 1 : 0;
    }
};

MNKGame.prototype.evaluate = function() {
    if (!this.terminal()) {
        return 0.5;
    }
};


// Game.inputMove();
var game = new MNKGame(3, 3, 3);
Game.play(game, 3)

// def __str__(self):
//     lines = []
//     lines.append(self.current_player + '\'s turn to move.')
//     for i in range(self.m):
//         line = [p if p is not None else '-' for p in self.pieces[i]]
//         lines.append(''.join(line))
//     return '\n'.join(lines)

// def __eq__(self, other):
//     """
//     Overloads '==' such that two game with the same configuration
//     are equal.
//     """
//     return self.__str__() == other.__str__()

// def __hash__(self):
//     return hash(self.__str__())


// if __name__ == '__main__':

//     # TicTacToe
//     # game = MNKGame(3, 3, 3)
//     # Gomoku
//     game = MNKGame(19, 19, 5)
//     MNKGame.play(game, 3)