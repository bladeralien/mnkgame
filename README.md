# mnkgame
使用 Python 以及 JavaScript 实现的 mnkgame，所谓的 mnkgame 是指在一个 m * n 的棋盘上将k个棋子连成一条线，比较常见的形式是 tic-tac-toe 以及五子棋。
详情可以参考维基。
利用如下几种技术实现了 AI。不过因为规模的原因，目前只在 tic-tac-toe 上有比较好的效果。
alpha-beta 剪枝，效果一般，因为要定义一个好的 evaluate 即估值函数，而我现在还没有想到好的估值函数。
MCTS，monte carlo tree search，效果很好，给定5s的搜索时间，在ttt上可以找到最优解，但对于大的棋盘，因为搜索量急剧增大，所以就不行了。
Q-Learning，效果很好，经过几万次对局的学习（只需要几分钟的运行时间），就可以在ttt上学到最优解了，而且AI的对手是完全随机的。
不过Q-Learning也有扩展性的问题，随着问题规模的增大，Q-Learning算法需要存储的QValue的数量也是急剧增大的，这时候就要用到Approximation Q-Learning，最简单的是定义一些feature，用一个feature的线性方程来估计QValue，当然，这需要选取好的feature。或者也可以选取其他的机器学习模型来估计QValue，比如说人工神经网络。
本项目使用了大量的来自 Artificial Intelligence: A Modern Approach 以及EDX上的Artificial Intelligence课程的代码。
