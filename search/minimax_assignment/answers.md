## Answers

### Q1
*All possible states:* The state of the game is defined by

1. The positions of the fish in the water,
2. the positions of the boats,
3. the positions of the boats' hooks,
4. the scores of the two players,
5. the current player,
6. and the fishes caught by each player.

All possible states will thus be all possible variations of these different variables.

*Initial state:* In the initial state, each player has 0 points and no caught fish, meaning that all the fish are left in the water. The boats, hooks, and fishes are in their starting positions, and the current player will be the green boat.

*Transition function:* a player makes a move from {LEFT, RIGHT, UP, DOWN, STAY}, and a player's score may increase or decrease if a fish was caught. The player's position is updated (the hook or the boat). The position of the fish will also be updated, as the fish move in the 9 basic directions.

### Q2
Either all the fish (that do not give negative points) are caught or the timer has run out. If all the fish are caught, the terminal state is the boats' positions and the score of each player. If the timer has run out, the terminal state could be any state reachable through a series of legal moves.

### Q3
It is very simple and fast to compute, something that can be done using only the game state.

### Q4
The terminal state, where $Score(Green\ boat) - Score(Red\ boat)$ exactly determines the final winner of the game. Since this is equivalent to the evaluation function, there will be no approximation errors in a terminal state.

### Q5
If it is A's turn, this can happen if A picks up a fish that gives negative points, and the game ends up in a terminal state. If it is B's turn, they could pick up an additional fish that leads to a state where $v(A, s) < 0$.

### Q6
The problem would then be that we are in a state where $η(A, s) > 0$ and B wins in next turn. This could for example happen when there is one fish left and A is currently in the lead. If B gets the final fish, B wins the game. But since the fish can only be reached through one out of 4 available moves to B, the heuristic will say that A is more likely to win. Then when B takes the fish in the next turn, B wins the game despite $η(A, s) > 0$ being true in the previous turn.

