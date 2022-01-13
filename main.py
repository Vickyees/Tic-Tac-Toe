from itertools import combinations
from art import logo
import random

MAGIC_SQUARE = [8, 3, 4, 1, 5, 9, 6, 7, 2]
BEST_CPU_MOVES = [1, 3, 5, 7, 9]

game_on = True
cpu_match_on = None
player_wins = None
current_layout = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
available_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
magic_moves_p1 = []
magic_moves_p2 = []
magic_moves_human = []
magic_moves_cpu = []
turn = None


def initializeGame():
    global game_on, player_wins, available_moves, turn, current_layout
    global magic_moves_p1, magic_moves_p2, magic_moves_cpu, magic_moves_human
    game_on = True
    player_wins = False
    available_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    current_layout = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    magic_moves_p1 = []
    magic_moves_p2 = []
    magic_moves_human = []
    magic_moves_cpu = []


def printLayout(layout):
    print(f" {layout[0]}  |  {layout[1]} |  {layout[2]} ")
    print("____|____|____")
    print(f" {layout[3]}  |  {layout[4]} |  {layout[5]} ")
    print("____|____|____")
    print(f" {layout[6]}  |  {layout[7]} |  {layout[8]} ")
    print("    |    |    ")


def makePlayerMove(player, position):
    global player_wins, turn
    if player == "p1":
        symbol = "X"
    else:
        symbol = "O"
    if position in available_moves:
        current_layout[position - 1] = symbol
        available_moves.remove(position)
        if player == "p1":
            magic_moves_p1.append(MAGIC_SQUARE[position - 1])
            turn = "p2"
        else:
            magic_moves_p2.append(MAGIC_SQUARE[position - 1])
            turn = "p1"
        if checkWin(player):
            print(f"\n\nCongrats! Player-{player[1]}({symbol}) wins!")
            player_wins = True
    else:
        print("Enter the valid square number!!!")


def possWin(player):
    if player == "cpu":
        move_combs = list(combinations(magic_moves_cpu, 2))
        sum_magic_moves = [sum(map(int, comb)) for comb in move_combs]
        cpu_win_distances = [15 - i for i in sum_magic_moves]
        for distance in cpu_win_distances:
            if 0 < distance <= 9:
                if (MAGIC_SQUARE.index(distance) + 1) in available_moves:
                    return MAGIC_SQUARE.index(distance) + 1
        return 0
    else:
        move_combs = list(combinations(magic_moves_human, 2))
        sum_magic_moves = [sum(map(int, comb)) for comb in move_combs]
        human_win_distances = [15 - i for i in sum_magic_moves]
        for distance in human_win_distances:
            if 0 < distance <= 9:
                if (MAGIC_SQUARE.index(distance) + 1) in available_moves:
                    return MAGIC_SQUARE.index(distance) + 1
        return 0


def makeCpuMove(symbol):
    global player_wins, turn
    if len(available_moves) == 9:
        move = random.choice(BEST_CPU_MOVES)
    else:
        if possWin("cpu"):
            move = possWin("cpu")
        elif possWin("human"):
            move = possWin("human")
        else:
            for best_move in BEST_CPU_MOVES:
                if best_move in available_moves:
                    move = best_move
                else:
                    move = random.choice(available_moves)
    current_layout[move - 1] = symbol
    available_moves.remove(move)
    magic_moves_cpu.append(MAGIC_SQUARE[move - 1])
    turn = "human"
    print(f"\nCpu Plays-{symbol}:\n")
    printLayout(current_layout)


def makeHumanMove(symbol):
    global turn
    position = int(input(f"Enter the square number(1-9)-{symbol}: "))
    if position in available_moves:
        current_layout[position - 1] = symbol
        available_moves.remove(position)
        magic_moves_human.append(MAGIC_SQUARE[position - 1])
        turn = "cpu"
        printLayout(current_layout)
    else:
        print("Enter the valid square number!!!")
        makeHumanMove(symbol)


def checkWin(player):
    if player == "p1":
        player_magic_moves = magic_moves_p1
    elif player == "p2":
        player_magic_moves = magic_moves_p2
    elif player == 'cpu':
        player_magic_moves = magic_moves_cpu
    else:  # human
        player_magic_moves = magic_moves_human
    move_combs = list(combinations(player_magic_moves, 3))
    sum_magic_moves = [sum(map(int, comb)) for comb in move_combs]
    if 15 in sum_magic_moves:
        return True  # Player Wins
    return False


def playPrompt():
    global game_on
    play_again = input("Do you want to play again? type 'yes' or 'no':")
    if play_again.lower() in ['no', 'n']:
        game_on = False
    elif play_again.lower() in ['yes', 'y']:
        initializeGame()
    else:
        playPrompt()


def playCpuMatch():
    global turn, cpu_match_on
    user_symbol = input("\nDo you want to play as player-1(X) or player-2(O)?\nType 'X' or 'O': ").upper()
    if user_symbol == "X":
        cpu_symbol = "O"
        turn = "human"
    else:
        cpu_symbol = "X"
        turn = "cpu"
    initializeGame()
    printLayout(available_moves)
    cpu_match_on = True
    while cpu_match_on:
        if not available_moves:
            print("Match Draw!, No one wins.")
            cpu_match_on = False
        else:
            if turn == "human":
                makeHumanMove(user_symbol)
                if checkWin("human"):
                    cpu_match_on = False
                    print("Congrats! You won the match!")
            else:
                makeCpuMove(cpu_symbol)
                if checkWin("cpu"):
                    cpu_match_on = False
                    print("You lost the match!")


def playHumanMatch():
    global turn
    initializeGame()
    turn = "p1"
    printLayout(available_moves)
    while available_moves and not player_wins:
        if turn == "p1":
            n = int(input(f"Player-1(X), enter the square number(1-9): "))
            makePlayerMove("p1", n)
        else:
            n = int(input(f"Player-2(O), enter the square number(1-9): "))
            makePlayerMove("p2", n)
        printLayout(current_layout)
        print("\n")
    else:
        if not player_wins:
            print("Match Draw!, No one wins.")


while game_on:
    print(logo)
    choice = int(input("Select with whom you want to play against: \n"
                       "1. Single(play against cpu) \n2. Double(human vs human)\nType 1 or 2: "))
    if choice == 1:
        playCpuMatch()
    elif choice == 2:
        playHumanMatch()
    else:
        continue
    playPrompt()
else:
    print("Game Ended!")