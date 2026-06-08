import tkinter as tk
from tkinter import messagebox, ttk
import threading
from mancala import Mancala
from alphabeta import alphabeta
from minimax import minimax


class MancalaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mancala Solver - Interactive Game")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2c3e50")
        
        self.game = None
        self.human_player = 1
        self.ai_player = 2
        self.ai_algorithm = "alphabeta"
        self.ai_depth = 5
        self.game_over = False
        self.ai_thinking = False
        
        self.setup_ui()
        self.new_game()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Top control panel
        control_frame = tk.Frame(self.root, bg="#34495e", height=100)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        title = tk.Label(control_frame, text="MANCALA SOLVER", font=("Arial", 24, "bold"), 
                        bg="#34495e", fg="#ecf0f1")
        title.pack(pady=5)
        
        # Settings frame
        settings_frame = tk.Frame(control_frame, bg="#34495e")
        settings_frame.pack(pady=5)
        
        # Algorithm selection
        tk.Label(settings_frame, text="AI Algorithm:", font=("Arial", 10), 
                bg="#34495e", fg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        
        self.algorithm_var = tk.StringVar(value="alphabeta")
        algo_combo = ttk.Combobox(settings_frame, textvariable=self.algorithm_var, 
                                 values=["alphabeta", "minimax"], state="readonly", width=12)
        algo_combo.pack(side=tk.LEFT, padx=5)
        algo_combo.bind("<<ComboboxSelected>>", lambda e: self.change_algorithm())
        
        # Depth selection
        tk.Label(settings_frame, text="Search Depth:", font=("Arial", 10), 
                bg="#34495e", fg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        
        self.depth_var = tk.IntVar(value=5)
        depth_spin = tk.Spinbox(settings_frame, from_=1, to=8, textvariable=self.depth_var, 
                               width=5, font=("Arial", 10))
        depth_spin.pack(side=tk.LEFT, padx=5)
        
        # New game button
        new_game_btn = tk.Button(control_frame, text="New Game", command=self.new_game,
                                font=("Arial", 11, "bold"), bg="#27ae60", fg="white",
                                padx=20, pady=5)
        new_game_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Main game area
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Board canvas
        self.canvas = tk.Canvas(main_frame, bg="#1a252f", width=900, height=300,
                               highlightbackground="#34495e", highlightthickness=2)
        self.canvas.pack(pady=20)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Status and info frame
        info_frame = tk.Frame(main_frame, bg="#34495e")
        info_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = tk.Label(info_frame, text="", font=("Arial", 12), 
                                    bg="#34495e", fg="#ecf0f1")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.score_label = tk.Label(info_frame, text="", font=("Arial", 12, "bold"), 
                                   bg="#34495e", fg="#f39c12")
        self.score_label.pack(side=tk.RIGHT, padx=10)
        
        # Message log
        log_frame = tk.Frame(main_frame, bg="#34495e", height=100)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(log_frame, text="Game Log:", font=("Arial", 10, "bold"), 
                bg="#34495e", fg="#ecf0f1").pack(anchor=tk.W, padx=5, pady=5)
        
        self.log_text = tk.Text(log_frame, height=6, font=("Arial", 9), 
                               bg="#1a252f", fg="#ecf0f1", state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Instructions
        instr_label = tk.Label(self.root, 
            text="Click on your pits (numbered 1-6) to make a move • You are Player 1 • AI is Player 2",
            font=("Arial", 9), bg="#2c3e50", fg="#bdc3c7")
        instr_label.pack(pady=5)
        
    def change_algorithm(self):
        """Change the AI algorithm"""
        self.ai_algorithm = self.algorithm_var.get()
        self.log_message(f"AI algorithm changed to: {self.ai_algorithm}")
        
    def new_game(self):
        """Start a new game"""
        self.ai_depth = self.depth_var.get()
        self.game = Mancala(pits_per_player=6, stones_per_pit=4)
        self.game_over = False
        self.ai_thinking = False
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log_message("New game started! You are Player 1. Make your move.")
        self.update_display()
        
    def log_message(self, msg):
        """Add a message to the game log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def update_display(self):
        """Update the board display and status"""
        self.draw_board()
        self.update_status()
        
    def draw_board(self):
        """Draw the mancala board"""
        self.canvas.delete("all")
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 900
        if canvas_height <= 1:
            canvas_height = 300
        
        # Board dimensions
        pit_radius = 25
        mancala_width = 60
        mancala_height = 100
        pit_spacing = 65
        
        # Starting positions
        left_mancala_x = 40
        right_mancala_x = canvas_width - 40
        p1_y = canvas_height * 2 // 3
        p2_y = canvas_height // 3
        pit_start_x = 100
        
        # Draw mancalas (scoring bins)
        # P1 Mancala (left side)
        p1_mancala_score = self.game.board[self.game.p1_mancala_index]
        self.canvas.create_rectangle(left_mancala_x - mancala_width//2, p1_y - mancala_height//2,
                                     left_mancala_x + mancala_width//2, p1_y + mancala_height//2,
                                     fill="#e74c3c", outline="#c0392b", width=2)
        self.canvas.create_text(left_mancala_x, p1_y - 30, text="P1 Mancala", 
                               font=("Arial", 9, "bold"), fill="white")
        self.canvas.create_text(left_mancala_x, p1_y, text=str(p1_mancala_score), 
                               font=("Arial", 20, "bold"), fill="white")
        
        # P2 Mancala (right side)
        p2_mancala_score = self.game.board[self.game.p2_mancala_index]
        self.canvas.create_rectangle(right_mancala_x - mancala_width//2, p2_y - mancala_height//2,
                                     right_mancala_x + mancala_width//2, p2_y + mancala_height//2,
                                     fill="#3498db", outline="#2980b9", width=2)
        self.canvas.create_text(right_mancala_x, p2_y - 30, text="P2 Mancala", 
                               font=("Arial", 9, "bold"), fill="white")
        self.canvas.create_text(right_mancala_x, p2_y, text=str(p2_mancala_score), 
                               font=("Arial", 20, "bold"), fill="white")
        
        # Draw Player 1 pits (bottom row, left to right, numbered 1-6)
        for i in range(6):
            pit_index = i
            stones = self.game.board[pit_index]
            x = pit_start_x + i * pit_spacing
            y = p1_y
            
            # Determine pit color
            is_valid = self.game.valid_move(i + 1)
            pit_color = "#2ecc71" if is_valid else "#95a5a6"
            
            self.canvas.create_oval(x - pit_radius, y - pit_radius,
                                   x + pit_radius, y + pit_radius,
                                   fill=pit_color, outline="#27ae60", width=2)
            self.canvas.create_text(x, y - pit_radius - 15, text=str(i + 1), 
                                   font=("Arial", 8, "bold"), fill="white")
            self.canvas.create_text(x, y, text=str(stones), 
                                   font=("Arial", 16, "bold"), fill="white")
            
            # Store pit info for clicking
            self.canvas.create_text(x, y + pit_radius + 10, text=f"Pit {i+1}", 
                                   font=("Arial", 7), fill="#bdc3c7")
        
        # Draw Player 2 pits (top row, right to left for visualization - opposite to P1)
        for i in range(6):
            pit_index = self.game.pits_per_player + 1 + (5 - i)  # P2 pits in reverse (12,11,10,9,8,7)
            stones = self.game.board[pit_index]
            x = pit_start_x + (5 - i) * pit_spacing  # Position from right to left
            y = p2_y
            
            pit_color = "#9b59b6"
            
            self.canvas.create_oval(x - pit_radius, y - pit_radius,
                                   x + pit_radius, y + pit_radius,
                                   fill=pit_color, outline="#8e44ad", width=2)
            self.canvas.create_text(x, y - pit_radius - 15, text=str(i + 1), 
                                   font=("Arial", 8, "bold"), fill="white")
            self.canvas.create_text(x, y, text=str(stones), 
                                   font=("Arial", 16, "bold"), fill="white")
        
        # Draw center line
        center_y = (p1_y + p2_y) // 2
        self.canvas.create_line(pit_start_x - 20, center_y, canvas_width - pit_start_x + 20, 
                               center_y, fill="#34495e", width=2, dash=(5, 5))
        
        self.canvas.create_text(canvas_width // 2, center_y - 20, text="Player 2 (AI)", 
                               font=("Arial", 10, "bold"), fill="#3498db")
        self.canvas.create_text(canvas_width // 2, center_y + 20, text="Player 1 (You)", 
                               font=("Arial", 10, "bold"), fill="#2ecc71")
    
    def update_status(self):
        """Update status labels"""
        p1_score = self.game.board[self.game.p1_mancala_index]
        p2_score = self.game.board[self.game.p2_mancala_index]
        
        self.score_label.config(text=f"Score: You {p1_score} - {p2_score} AI")
        
        if self.game_over:
            if p1_score > p2_score:
                status = "🎉 You Won! 🎉"
            elif p2_score > p1_score:
                status = "AI Won! Better luck next time."
            else:
                status = "It's a Tie!"
            self.status_label.config(text=status, fg="#f39c12")
        else:
            if self.game.current_player == 1:
                status = "Your turn - Click on a pit"
                color = "#2ecc71"
            else:
                status = "AI is thinking..."
                color = "#3498db"
            self.status_label.config(text=status, fg=color)
    
    def on_canvas_click(self, event):
        """Handle canvas clicks for pit selection"""
        if self.game_over or self.game.current_player != 1 or self.ai_thinking:
            return
        
        # Calculate which pit was clicked
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        pit_radius = 25
        pit_spacing = 65
        pit_start_x = 100
        p1_y = canvas_height * 2 // 3
        
        # Check each pit
        for i in range(6):
            x = pit_start_x + i * pit_spacing
            y = p1_y
            
            distance = ((event.x - x)**2 + (event.y - y)**2)**0.5
            
            if distance < pit_radius:
                # Pit clicked
                pit_num = i + 1
                if self.make_human_move(pit_num):
                    self.root.after(500, self.ai_move)
                return
    
    def make_human_move(self, pit):
        """Make a move for the human player"""
        if not self.game.valid_move(pit):
            messagebox.showwarning("Invalid Move", f"Pit {pit} is empty or invalid!")
            return False
        
        self.game.play(pit)
        self.log_message(f"You played pit {pit}")
        self.update_display()
        
        # Check for game over
        if self.game.winning_eval():
            self.end_game()
            return False
        
        return True
    
    def ai_move(self):
        """Make a move for the AI"""
        if self.game_over or self.game.current_player != 2:
            return
        
        self.ai_thinking = True
        self.update_status()
        self.root.update()
        
        try:
            # Get AI move
            if self.ai_algorithm == "alphabeta":
                move = alphabeta(self.game, self.ai_depth, player=2)
            else:  # minimax
                move = minimax(self.game, self.ai_depth, player=2)
            
            move = int(move)
            
            # Make the move
            self.game.play(move)
            self.log_message(f"AI played pit {move}")
            self.update_display()
            
            # Check for game over
            if self.game.winning_eval():
                self.end_game()
                self.ai_thinking = False
                return
            
            # If current player is still AI, make another move
            if self.game.current_player == 2:
                self.ai_thinking = False
                self.root.after(300, self.ai_move)
            else:
                self.ai_thinking = False
                self.update_display()
                
        except Exception as e:
            messagebox.showerror("AI Error", f"An error occurred: {str(e)}")
            self.ai_thinking = False
    
    def end_game(self):
        """Handle game end"""
        self.game_over = True
        
        p1_score = self.game.board[self.game.p1_mancala_index]
        p2_score = self.game.board[self.game.p2_mancala_index]
        
        if p1_score > p2_score:
            result = f"You won {p1_score} to {p2_score}!"
            self.log_message("🎉 " + result + " 🎉")
        elif p2_score > p1_score:
            result = f"AI won {p2_score} to {p1_score}. Try again!"
            self.log_message(result)
        else:
            result = f"It's a tie {p1_score} to {p2_score}!"
            self.log_message(result)
        
        self.update_status()
        messagebox.showinfo("Game Over", result + "\n\nClick 'New Game' to play again.")


def main():
    root = tk.Tk()
    gui = MancalaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
