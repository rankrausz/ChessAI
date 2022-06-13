# Chess AI
A chess game with GUI made with python & pygame.



<p align="center">
  <img src="https://user-images.githubusercontent.com/103533203/169710341-fd54f2cd-38da-4a8e-95c3-7afd65e60247.gif" width="400" alt="animated" />
</p>

## How does it work?

AI uses minimax algorithm with alpha-beta optimiziation. The algorithm will look at all of the moves currently possible in the position, and then for each one look at all of the responses the rival has, and so on until a pre-defined depth is reached. when the desired depth is achieved it performs a static evaluation of the position. These are values that are then passed up the tree so that the computer can choose the best move - you can read further [here](https://en.wikipedia.org/wiki/Minimax#Minimax_algorithm_with_alternate_moves).

The maximum search depth is only 3 at the moment (not ply- meaning it searches 3 moves ahead). Any higher and it would take too much time.

The main reason for the slow speed is the board representation - it's a 2D list of 'Square' instance, each one containing 0 or 1 'Piece' instance. This makes each operation on the board take a lot of time, which is not ideal. In V2 of this AI the board will be represented as a single 1D list of integers, representing different pieces. Along with many other optimizations this will alow much greater search depth, and a better engine. However, even at depth of 3 it will still put up a decent fight, try it!

## What's Next

This version has a lot of place for improvement, but without speed it can not be a strong engine, and it has to be re-built from the ground up. so I plan on leaving it as-is, and currently working on a second version which will be much more efficient (along with other improvement)

## Wanna play?

To run the game, make sure your working directory is ChessAI and run main.py.

press r to go to main menu.

press u to undo last move

* En passant is not yet implemented

