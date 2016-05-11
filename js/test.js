var inputMove = function(callback) {
    var move;
    var readline = require('readline');
    var rl = readline.createInterface({
        input:process.stdin, output:process.stdout
    });
    rl.setPrompt('input your move:');
    rl.prompt();
    rl.on('line', function(line) {
        move = line.trim().split(',').map(function(val) {
            return parseInt(val);
        })
        console.log(move);
        callback(move);
        rl.close();
    });
    rl.on('close', function() {
        process.exit(0);
    });
    return move;
}
inputMove(function(move) {
console.log('=====');
console.log(move);
console.log('=====');
});



// const repl = require('repl');
// var connections = 0;

// repl.start({
//   prompt: 'Node.js via stdin> ',
//   input: process.stdin,
//   output: process.stdout
// });

// const readline = require('readline');

// const rl = readline.createInterface({
//   input: process.stdin, output: process.stdout
// });

// var move;
// console.log(move);

// rl.question('input your move:', function(answer) {
//     move = answer;
//     // rl.close();
//     process.exit();
// });

// console.log('===========')
// console.log(move);
//
  // var move;
  // console.log(move);
  // var prompt = require('prompt');
  // // prompt.setPrompt('input your move:')
  // prompt.start();

  // // prompt.get('move', function (err, input) {
  // //   move = input.move;
  // //   console.log('Command-line input received:');
  // //   console.log('  move: ' + input.move);
  // //   console.log(move)
  // // });
  // prompt.get('move');
  // console.log('====')
  // console.log(move)

// var testfunc = function() {
// var move;

// var readline = require('readline');
// var rl = readline.createInterface(process.stdin, process.stdout);
// rl.setPrompt('input your
// rl.prompt();

// rl.on('line', function(line) {
//     move = line;
//     rl.close();
// }).on('close',function(){
//     process.exit(0);
// });

// return move;
// }
// testmove = testfunc();
// console.log(testmove)