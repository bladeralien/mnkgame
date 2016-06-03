var range = function(k) {
    return Array.apply(null, Array(k)).map(function(_, i) {
        return i;
    });
};


String.prototype.repeat = function(count) {
    if (count < 1) return '';
    var result = '', pattern = this.valueOf();
    while (count > 1) {
        if (count & 1) result += pattern;
        count >>= 1, pattern += pattern;
    }
    return result + pattern;
};


Array.prototype.count = function(element) {
    return this.filter(function(x){return x == element}).length
};
