import random
from random import randint


class Mancala:
    def __init__(self, pits_per_player=6, stones_per_pit = 4):
        self.pits_per_player = pits_per_player
        self.board = [stones_per_pit] * ((pits_per_player+1) * 2)  # Initialize each pit with stones_per_pit number of stones 
        self.players = 2
        self.current_player = 1
        self.moves = []
        self.p1_pits_index = list(range(self.pits_per_player))
        self.p1_mancala_index = self.pits_per_player
        self.p2_pits_index = list(range(self.pits_per_player + 1, len(self.board) - 1))
        self.p2_mancala_index = len(self.board)-1
        self.stones_per_pit = stones_per_pit
        
        # Zeroing the Mancala for both players
        self.board[self.p1_mancala_index] = 0
        self.board[self.p2_mancala_index] = 0

    def display_board(self):
        player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
        player_1_mancala = self.board[self.p1_mancala_index]
        player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
        player_2_mancala = self.board[self.p2_mancala_index]

        print('P1               P2')
        print('     ____{}____     '.format(player_2_mancala))
        for i in range(self.pits_per_player):
            if i == self.pits_per_player - 1:
                print('{} -> |_{}_|_{}_| <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            else:    
                print('{} -> | {} | {} | <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            
        print('         {}         '.format(player_1_mancala))
        turn = 'P1' if self.current_player == 1 else 'P2'
        print('Turn: ' + turn)
        
    def valid_move(self, pit):
        if self.current_player == 1:
            if pit-1 in self.p1_pits_index and self.board[pit-1] != 0:
                return True
            else:
                return False
        else:
            pit = pit + self.pits_per_player
            if pit in self.p2_pits_index and self.board[pit] != 0:
                return True
            else:
                return False

    def random_move_generator(self):
        temp_possible_moves = self.possible_moves()
        randnum = randint(0, len(temp_possible_moves)-1)
        return temp_possible_moves[randnum]
    
    def play(self, pit):
        
        '''
        if self.current_player == 1:
            print("Player 1 chose pit: " + str(pit))
        else:
            print("Player 2 chose pit: " + str(pit))
        
        print()
        
        if not self.valid_move(pit):
            #print("INVALID MOVE")
            return False
        
        if self.winning_eval():
            #print("GAME OVER")
            return True
        '''

        if self.current_player == 1:
            current_pit_index = pit - 1
        else:
            current_pit_index = pit + self.pits_per_player
        
        num_stones = self.board[current_pit_index]
        self.board[current_pit_index] = 0
        
        while num_stones > 0:
            current_pit_index = (current_pit_index + 1) % len(self.board)
            
            if (self.current_player == 1 and current_pit_index == self.p2_mancala_index) or (self.current_player == 2 and current_pit_index == self.p1_mancala_index):
                continue
            
            self.board[current_pit_index] += 1
            num_stones -= 1

        if self.current_player == 1 and current_pit_index in self.p1_pits_index:
            if self.board[current_pit_index] == 1:
                opposite_pit = self.p2_pits_index[0] + (self.pits_per_player - 1 - current_pit_index)
                self.board[self.p1_mancala_index] += self.board[opposite_pit] + 1
                self.board[opposite_pit] = 0
                self.board[current_pit_index] = 0
        elif self.current_player == 2 and current_pit_index in self.p2_pits_index:
            if self.board[current_pit_index] == 1:
                opposite_pit = self.pits_per_player - 1 - (current_pit_index - self.p2_pits_index[0])
                self.board[self.p2_mancala_index] += self.board[opposite_pit] + 1
                self.board[opposite_pit] = 0
                self.board[current_pit_index] = 0

        self.moves.append((self.current_player, pit))
        
        self.current_player = 3 - self.current_player

        return self.board
        
    
    def winning_eval(self):
        p1valid = False
        p2valid = False
        
        for i in self.p1_pits_index:
            if self.board[i] != 0:
                p1valid = True
            
        for i in self.p2_pits_index:
            if self.board[i] != 0:
                p2valid = True
        
        if p2valid == False or p1valid == False:
            return True
        
        return False
    
    
    
    def possible_moves(self):
        possible_moves_arr = []
        for x in range(self.pits_per_player):
            if self.valid_move(x+1):
                possible_moves_arr.append(x+1)
        return possible_moves_arr
    

    def get_stones_per_pit(self):
        return self.stones_per_pit
    
    def get_pits_per_player(self):
        return self.pits_per_player
    