from mancala import Mancala
from alphabeta import *
from minimax import *
from random import randint
import time

import matplotlib.pyplot as plt

# This function mimics the logic from your provided loop:
# For each depth, it runs 100 games and tracks how many times Alpha-Beta wins
# Here we'll use mock logic, assuming your `alphabeta_vs_random(depth)` function exists
# You would replace the inside of this with your real logic

def alphabeta_vs_random_sim(depth, num_games=100):
    results = []

    for x in range(num_games):
        game = Mancala(pits_per_player = 6, stones_per_pit = 4)

        randnum = randint(0, 1)

        if randnum == 0:
            turn = 0
            while(game.winning_eval() == False):
                if turn == 0:
                    move = game.random_move_generator()
                    game.play(move)
                    turn+=1
                else:
                    move = int(minimax(game, depth, player=2))
                    game.play(move)
                    turn=0

        else:
            turn = 0
            while(game.winning_eval() == False):
                if turn == 0:
                    move = int(minimax(game, depth, player=1))
                    game.play(move)
                    turn+=1
                else:
                    move = game.random_move_generator()
                    game.play(move)
                    turn=0
        

        if(randnum == 0):
            randommancala = game.board[game.p1_mancala_index]
            alphabetamancala = game.board[game.p2_mancala_index]
            winner=""
            
            if(randommancala > alphabetamancala):
                winner="random"
            elif(alphabetamancala > randommancala):
                winner="alphabeta"
            else:
                winner="tie"
            
            num_moves = len(game.moves)
            results.append([winner, num_moves])
        
        else:
            randommancala = game.board[game.p2_mancala_index]
            alphabetamancala = game.board[game.p1_mancala_index]
            winner=""
            
            if(randommancala > alphabetamancala):
                winner="random"
            elif(alphabetamancala > randommancala):
                winner="alphabeta"
            else:
                winner="tie"
            
            num_moves = len(game.moves)
            results.append([winner, num_moves])

    # Count how many wins were 'alphabeta'
    alphabeta_wins = sum(1 for r in results if r[0] == "alphabeta")
    return alphabeta_wins

# Run simulations for depths 1 through 6
depths = list(range(1, 6))
alpha_beta_wins = [alphabeta_vs_random_sim(depth) for depth in depths]

# Plotting the results
plt.figure(figsize=(8, 5))
plt.plot(depths, alpha_beta_wins, marker='o', linestyle='-', color='#0077ff', linewidth=2)
plt.fill_between(depths, alpha_beta_wins, color='#0077ff', alpha=0.1)

plt.title('Minimax Wins vs Random Opponent at Varying Depths')
plt.xlabel('Search Depth')
plt.ylabel('Wins out of 100 Games')
plt.ylim(0, 100)
plt.xticks(depths)
plt.grid(True, linestyle='--', alpha=0.5)

# Annotate the points

plt.show()
# Save chart
final_chart_path = "/mnt/data/realistic_alphabeta_depth_results.png"
plt.tight_layout()
#plt.savefig(final_chart_path)
plt.show()

#final_chart_path
