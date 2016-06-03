var MNKGame = function(m, n, k, pieces, currentPlayer) {
    this.m = m;
    this.n = n;
    this.k = k;
    if (pieces == undefined) {
        this.pieces = [];
        for (var i = 0; i < this.m; i++) {
            this.pieces.push([]);
            for (var j = 0; j < this.n; j++) {
                this.pieces[i].push(null);
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
            if (this.pieces[i][j] == null) {
                moves.push([i, j]);
            };
        };
    };
    return moves;
};

MNKGame.prototype.stateAfterMove = function(move) {
    var i = move[0], j = move[1];
    var pieces = JSON.parse(JSON.stringify(this.pieces));
    var currentPlayer = this.currentPlayer;
    pieces[i][j] = currentPlayer;
    currentPlayer = currentPlayer == 'X' ? 'O' : 'X';
    var newobj = new MNKGame(this.m, this.n, this.k, pieces, currentPlayer)
    return newobj;
};

MNKGame.prototype.terminal = function() {
    var that = this;
    var pattern = MNKGame.players.map(function(player) {
        return player.repeat(that.k);
    });
    for (var i = 0; i < this.m; i++) {
        for (var j = 0; j < this.n + 1 - this.k; j++) {
            var temp = this.pieces[i].slice(j, j + this.k);
            temp = temp.map(function(p) {
                return p != null ? p : '-';
            });
            if (pattern.indexOf(temp.join('')) != -1) {
                return true;
            };
        };
    };
    for (var j = 0; j < this.n; j++) {
        for (var i = 0; i < this.m + 1 - this.k; i++) {
            var temp = range(this.k).map(function(c) {
                return that.pieces[i + c][j]
            });
            temp = temp.map(function(p) {
                return p != null ? p : '-';
            });
            if (pattern.indexOf(temp.join('')) != -1) {
                return true;
            };
        };
    };
    for (var i = 0; i < this.m + 1 - this.k; i++) {
        for (var j = 0; j < this.n + 1 - this.k; j++) {
            var temp = range(this.k).map(function(c) {
                return that.pieces[i + c][j + c]
            });
            temp = temp.map(function(p) {
                return p != null ? p : '-';
            });
            if (pattern.indexOf(temp.join('')) != -1) {
                return true;
            };
        };
    };
    for (var i = this.k - 1; i < this.m; i++) {
        for (var j = 0; j < this.n + 1 - this.k; j++) {
            var temp = range(this.k).map(function(c) {
                return that.pieces[i - c][j + c]
            });
            temp = temp.map(function(p) {
                return p != null ? p : '-';
            });
            if (pattern.indexOf(temp.join('')) != -1) {
                return true;
            };
        };
    };
};

MNKGame.prototype.utility = function() {
    if (this.terminal()) {
        return this.currentPlayer == 'X' ? 1 : 0;
    }
};

MNKGame.prototype.evaluate = function() {
    if (!this.terminal()) {
        var score = 0;
        var that = this;
        for (var i = 0; i < this.m; i++) {
            for (var j = 0; j < this.n + 1 - this.k; j++) {
                var temp = this.pieces[i].slice(j, j + this.k);
                score += temp.count('O') - temp.count('X');
            };
        };
        for (var j = 0; j < this.n; j++) {
            for (var i = 0; i < this.m + 1 - this.k; i++) {
                var temp = range(this.k).map(function(c) {
                    return that.pieces[i + c][j]
                });
                score += temp.count('O') - temp.count('X');
            };
        };
        for (var i = 0; i < this.m + 1 - this.k; i++) {
            for (var j = 0; j < this.n + 1 - this.k; j++) {
                var temp = range(this.k).map(function(c) {
                    return that.pieces[i + c][j + c]
                });
                score += temp.count('O') - temp.count('X');
            };
        };
        for (var i = this.k - 1; i < this.m; i++) {
            for (var j = 0; j < this.n + 1 - this.k; j++) {
                var temp = range(this.k).map(function(c) {
                    return that.pieces[i - c][j + c]
                });
                score += temp.count('O') - temp.count('X');
            };
        };
        score = 1 / (1 + Math.pow(Math.E, score));
        console.log('evaluate');
        console.log(this.toString());
        console.log(score);
        return score;
    };
};

MNKGame.prototype.toString = function() {
    var lines = [];
    lines.push(this.currentPlayer + '\'s turn to move.');
    for (var i = 0; i < this.m; i++) {
        var line = this.pieces[i].map(function(p) {
            return p != null? p: '-'
        });
        line = line.join('')
        lines.push(line);
    };
    return lines.join('\n');
};

MNKGame.prototype.inspect = MNKGame.prototype.toString;
