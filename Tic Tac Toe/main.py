def create_board():
    """Create an empty 3x3 board."""
    return [" " for _ in range(9)]

def display_board(board):
    """Display the current state of the board."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def is_winner(board, player):
    """Check if the specified player has won."""
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] == player:
            return True
    
    # Check columns
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] == player:
            return True
    
    # Check diagonals
    if board[0] == board[4] == board[8] == player:
        return True
    if board[2] == board[4] == board[6] == player:
        return True
    
    return False

def is_board_full(board):
    """Check if the board is full (tie game)."""
    return " " not in board

def get_player_move(board, player):
    """Get and validate player move."""
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-9): ")) - 1
            if 0 <= move <= 8:
                if board[move] == " ":
                    return move
                else:
                    print("That position is already taken!")
            else:
                print("Please enter a number between 1 and 9!")
        except ValueError:
            print("Please enter a valid number!")

def display_game_instructions():
    """Display the game instructions and board positions."""
    print("\nWelcome to Tic Tac Toe!")
    print("\nBoard positions are numbered as follows:")
    print("\n 1 | 2 | 3 ")
    print("---+---+---")
    print(" 4 | 5 | 6 ")
    print("---+---+---")
    print(" 7 | 8 | 9 ")
    print("\nPlayers will take turns placing their mark (X or O) on the board.")
    print("First player to get 3 in a row (horizontally, vertically, or diagonally) wins!")
    print("\nLet's begin!\n")

def play_game():
    """Main game loop."""
    while True:
        # Initialize the game
        board = create_board()
        current_player = "X"
        display_game_instructions()
        
        # Game loop
        while True:
            display_board(board)
            
            # Get player move
            move = get_player_move(board, current_player)
            board[move] = current_player
            
            # Check for win
            if is_winner(board, current_player):
                display_board(board)
                print(f"\nCongratulations! Player {current_player} wins!")
                break
            
            # Check for tie
            if is_board_full(board):
                display_board(board)
                print("\nIt's a tie!")
                break
            
            # Switch players
            current_player = "O" if current_player == "X" else "X"
        
        # Ask to play again
        play_again = input("\nWould you like to play again? (yes/no): ").lower()
        if play_again != 'yes' and play_again != 'y':
            print("\nThanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    play_game()
