# nim-move
Generates the best move possible given a game state in the game of nim

##Introduction
This program was written for a Data Structures II course's final team project. The goal was to design and implement an algorithm that plays a version of the game of [Nim] (https://en.wikipedia.org/wiki/Nim) optimally. The program generates the best possible move. It takes as inputs two files: one that contains the game state and one that contains the game constraints. In this instance the game state input file is called game_state.txt and the game constraints file is called lose_patterns.txt.

##Setup
If not already installed, install [Python] (https://www.python.org/downloads/) on your computer. Save the source code with the two input files in the same directory on your computer. 

##Usage
On your CLI run the following command ``` bash python nim_move.py game_state.txt lose_patterns.txt ```
Note that while game_state.txt will be modified througout the progression of the game, lose_patterns.txt should only be changed before the game starts and should conform to the game constraints. Here is how the two files are structured.

###game_state.txt
The game state.txt file is formatted as a list with h lines, where h is the number of
unique pile heights in the game state. Each line in the file is of the form ”X pY ” where
X is the number of piles that have Y objects in them (ex. 5p3 means 5 piles with 3
objects each).

###lose_patterns.txt
The lose patterns.txt file is formatted as a list with p lines, where p is the number of
”lose patterns” we need to avoid. Each line is a series of number pairs of the form
”X pY ” where X is the number of piles that have Y objects in them (ex. 2p1 means
2 piles with 1 object each).

##Contributors
Michael Lane and Liam O'Brien are the other two contributors on this project.

##Contributing
Contributions are welcome. For major changes, please open an issue first to discuss the ideas you would like to implement.

##License
[MIT](https://choosealicense.com/licenses/mit/)




