function alphaBetaPruning(state, depth) {
    return maxValue(state, -Infinity, Infinity, depth)[1];
}

function maxValue(state, alpha, beta, depth) {
    if (state.terminal()) {
        return [state.utility(), null];
    }
    if (depth != undefined) {
        if (depth == 0) {
            return [state.evaluate(), null];
        }
        depth -= 1;
    }
    var maxminValue = -Infinity, maxminMove = null;
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
    if (state.terminal()) {
        return [state.utility(), null];
    }
    if (depth != undefined) {
        if (depth == 0) {
            return [state.evaluate(), null];
        }
        depth -= 1;
    }
    var minmaxValue = Infinity, minmaxMove = null;
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
    // body...
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
                console.log('you win');
                rl.close();
            }

            game = game.stateAfterMove(alphaBetaPruning(game, depth));
            console.log(game)

            if (game.terminal()) {
                console.log('you lose')
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
};
