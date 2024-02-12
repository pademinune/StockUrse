# StockUrse
My own chess bot in python from scratch (no chess libraries or anything). After every move, it will print the current board to the console (although it's recommended to follow on your own board for better graphics)

If you want to play as black, set 'youAreWhite' to 'False'.

In order to make your move, you need to input the current coordinate of the piece (in algebraic notation) followed by the destination seperated by a space.

Sample Input:

e2 e4

This moves the piece on e2 to e4. In the original starting position, this would move a pawn to e4.

After the bot finishes thinking, this is what it outputs:

![image](https://github.com/pademinune/StockUrse/assets/86390271/fa2faa3a-fb04-4450-829a-f770f813c24a)


You can also run it in this replit, however it will take much longer to think (around 10 seconds): https://replit.com/join/awunerszee-justinnitoi1

It works by calculating every possible move it can make, followed by every possible move the opponent can make to create a tree and output the best move. Unfortunately it must run on very low depth because the amount of lines it must calculate grows exponentially. In the future, I want to improve this by finding ways to ignore certain moves that are likely to be bad so I can then increase the depth.
