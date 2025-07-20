import serial
import time

# --- Game Configuration ---
SERIAL_PORT = 'COM6'  # *** IMPORTANT: Change this to your Arduino's serial port ***
                      # On Linux/macOS, it might be '/dev/ttyACM0' or '/dev/ttyUSB0'
BAUD_RATE = 9600

# --- Tic-Tac-Toe Game Logic ---
board = [' ' for _ in range(9)]  # Represents the 3x3 board (indices 0-8)
player_turn = 'X'
game_over = False

def print_board():
    print("\n--- Tic-Tac-Toe Board ---")
    print(f" {board[0]} | {board[1]} | {board[2]}    1 | 2 | 3")
    print("---+---+---  ---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]}    4 | 5 | 6")
    print("---+---+---  ---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]}    7 | 8 | 9")
    print("------------------------")

def check_win(player):
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

def check_draw():
    return ' ' not in board and not check_win('X') and not check_win('O')

def reset_game():
    global board, player_turn, game_over
    board = [' ' for _ in range(9)]
    player_turn = 'X'
    game_over = False
    print("\n--- Game Reset! ---")
    print_board()

# --- Serial Communication and Game Loop ---
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to Arduino on {SERIAL_PORT} at {BAUD_RATE} baud.")
    time.sleep(2) # Give some time for the serial connection to establish
    print_board()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Received from Arduino: {line}")

            if line.isdigit():
                cell_number = int(line)
                if 1 <= cell_number <= 9:
                    cell_index = cell_number - 1 # Convert 1-9 to 0-8 index

                    if not game_over:
                        if board[cell_index] == ' ':
                            board[cell_index] = player_turn
                            print_board()

                            if check_win(player_turn):
                                print(f"\n!!! Player {player_turn} wins! !!!")
                                game_over = True
                            elif check_draw():
                                print("\n!!! It's a draw! !!!")
                                game_over = True
                            else:
                                player_turn = 'O' if player_turn == 'X' else 'X'
                                print(f"Next turn: Player {player_turn}")
                        else:
                            print(f"Cell {cell_number} is already taken. Try again.")
                    else:
                        print("Game is over. Press a number to start a new game.")
                        # If a key is pressed after game over, treat it as a reset
                        reset_game()
                else:
                    print(f"Invalid input from keypad: {line}. Please press 1-9.")
            else:
                print(f"Non-numeric input ignored: {line}")

        time.sleep(0.1) # Small delay to prevent busy-waiting

except serial.SerialException as e:
    print(f"Error: Could not open serial port {SERIAL_PORT}. {e}")
    print("Please check:")
    print("1. If the Arduino is connected.")
    print("2. If the correct COM port is selected in the script.")
    print("3. If the Arduino IDE Serial Monitor is closed (it can block the port).")
except KeyboardInterrupt:
    print("\nExiting game.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")