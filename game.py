# game created by : Grzegorz Dubiel, Sebastian Znaj, Denis Łaskawiec
import os
import time
import sys
import tty
import termios
import random
import copy
from collections import Counter

LOOK = "@"

BOARD_WIDTH = 100
BOARD_HEIGHT = 35

INTRO = ("""
                     \x1b[1;30;47m.\x1b[0m
                    \x1b[1;30;47m/ \\\x1b[0m
                   \x1b[1;30;47m/ | \\\x1b[0m
                  \x1b[1;30;47m/  |  \\\x1b[0m              \x1b[6;30;42mW E L C O M E\x1b[0m
                 \x1b[1;30;47m|   |   |\x1b[0m
                 \x1b[1;30;47m|   |   |\x1b[0m                  \x1b[6;30;42mT O\x1b[0m
                 \x1b[1;30;47m|   |   |\x1b[0m
                 \x1b[1;30;47m|   |   |\x1b[0m          \x1b[6;30;42mR A B B I S W O R D\x1b[0m
                 \x1b[1;30;47m|   |   |\x1b[0m
                 \x1b[1;30;47m|   |   |\x1b[0m
                 \x1b[1;30;47m|   |   |\x1b[0m            W/S/A/D to move
                 \x1b[1;30;47m|   |   |\x1b[0m
                 \x1b[1;30;47m|   |   |\x1b[0m
                 \x1b[1;30;47m|   |   |\x1b[0m
                 \x1b[1;30;47m|   |   |\x1b[0m                      Created by:
                 \x1b[1;30;47m|   |   |\x1b[0m
                 \x1b[1;30;47m|   |   |\x1b[0m                           Sebastian Znaj
                 \x1b[1;30;47m|   |   |\x1b[0m
                 \x1b[1;30;47m|   |   |\x1b[0m                                 Grzegorz Dubiel
                 \x1b[1;30;47m|   |   |\x1b[0m
                 \x1b[1;30;47m|   |   |\x1b[0m                                        Denis Łaskawiec
                 \x1b[1;30;47m|   |   |\x1b[0m
                 \x1b[1;30;47m|   |   |\x1b[0m
 \x1b[1;30;47m________________|  / \  |_______________ \x1b[0m
\x1b[1;30;47m/  ______________|/     \|______________  \ \x1b[0m
\x1b[1;30;47m\  _____________/         \_____________  / \x1b[0m
 \x1b[1;30;47m\______________\         /______________/ \x1b[0m
                 \x1b[1;30;47m\       /\x1b[0m
                 \x1b[1;30;47m|\\    //|\x1b[0m
                 \x1b[1;30;47m|//\ ///|\x1b[0m
                 \x1b[1;30;47m|///////|\x1b[0m
                 \x1b[1;30;47m|///////|\x1b[0m
                 \x1b[1;30;47m|///////|\x1b[0m
                 \x1b[1;30;47m|///////|\x1b[0m
                 \x1b[1;30;47m|///////|\x1b[0m
                 \x1b[1;30;47m|///////|\x1b[0m
                \x1b[1;30;47m/ \/\_/\/ \\\x1b[0m
               \x1b[1;30;47m|\_/\/ \/\_/|\x1b[0m
               \x1b[1;30;47m|/ \/\ /\/ \|\x1b[0m
                \x1b[1;30;47m\_/\/_\/\_/\x1b[0m
                  \x1b[1;30;47m\_/_\_/\x1b[0m
        """)


def create_board():
    """Creates a game board with frame and obstacles"""
    game_board = [["-"] * BOARD_WIDTH for line in range(BOARD_HEIGHT)]
    game_board[0] = ["\x1b[1;30;47mX\x1b[0m"] * BOARD_WIDTH
    game_board[-1] = ["\x1b[1;30;47mX\x1b[0m"] * BOARD_WIDTH
    for i in range(16, 19):
        game_board[i][97] = "\x1b[1;36;44m|\x1b[0m"
        game_board[i][96] = "\x1b[1;36;44m|\x1b[0m"
    for x in game_board:
        x[0] = "\x1b[1;30;47mX\x1b[0m"
        x[-1] = "\x1b[1;30;47mX\x1b[0m"
    for i in range(1, 75):
        game_board[3][i] = "\x1b[1;30;47mX\x1b[0m"
        game_board[22][i] = "\x1b[1;30;47mX\x1b[0m"
    for i in range(10, 99):
        game_board[12][i] = "\x1b[1;30;47mX\x1b[0m"
        game_board[30][i] = "\x1b[1;30;47mX\x1b[0m"
    return game_board


def print_board(game_board):
    """displays a game board with hero character, etc."""
    for x in game_board:
        print(''.join(x))


def getch():
    """Allows a smooth introduction of moving keys"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def insert_hero(board, x=1, y=1):
    """ Displays a hero on the board """
    board[x][y] = LOOK
    return x, y


def insert_boss(board):
    """inserts boss in a static location on the map"""
    board[31][94:-1] = ("\x1b[1;33;40m(\_/)\x1b[0m")
    board[32][94:-1] = ("\x1b[1;33;40m(o.0)\x1b[0m")
    board[33][93:-1] = ("\x1b[1;33;40m(\")(\")\x1b[0m")
    return board


def item_spawn(board, a, b, c, d, e, f, g, h):
    """Spawns items in a random locations with special colors"""
    board[a][b] = '\x1b[1;33;41m1\x1b[0m'
    board[c][d] = '\x1b[1;36;40m2\x1b[0m'
    board[e][f] = '\x1b[1;30;47m3\x1b[0m'
    board[g][h] = '\x1b[1;36;45m4\x1b[0m'
    return board


def item_location():
    """Choose random item locations"""
    a = random.randint(3, BOARD_HEIGHT - 3)
    while a == 3 or a == 12 or a == 22 or a == 30:
        a = random.randint(3, BOARD_HEIGHT - 3)
    b = random.randint(3, BOARD_WIDTH - 3)
    c = random.randint(3, BOARD_HEIGHT - 3)
    while c == a or c == 3 or c == 12 or c == 22 or c == 30:
        c = random.randint(3, BOARD_HEIGHT - 3)
    d = random.randint(3, BOARD_WIDTH - 3)
    while d == b:
        d = random.randint(3, BOARD_WIDTH - 3)
    e = random.randint(3, BOARD_HEIGHT - 3)
    while e == a or e == c or e == 3 or e == 12 or e == 22 or e == 30:
        e = random.randint(3, BOARD_HEIGHT - 3)
    f = random.randint(3, BOARD_WIDTH - 3)
    while f == b or f == d:
        f = random.randint(3, BOARD_WIDTH - 3)
    g = random.randint(3, BOARD_HEIGHT - 3)
    while g == a or g == c or g == e or g == 3 or g == 12 or g == 22 or g == 30:
        g = random.randint(3, BOARD_HEIGHT - 3)
    h = random.randint(3, BOARD_WIDTH - 3)
    while h == b or h == d or h == f:
        h = random.randint(3, BOARD_WIDTH - 3)
    return a, b, c, d, e, f, g, h


def move(key_press, x, y, board):
    """
    Allows hero to move up, down,left, right, collect items and
    limits the movement to the dimensions of game board
    """
    global LOOK

    limit_x = x
    limit_y = y
    board[x][y] = "-"

    if key_press == 'w':
        x -= 1
        if x == 0:
            x = 1
    elif key_press == 's':
        x += 1
        if x == BOARD_HEIGHT - 1:
            x = BOARD_HEIGHT - 2
    elif key_press == 'd':
        y += 1
        if y == BOARD_WIDTH - 1:
            y = BOARD_WIDTH - 2
    elif key_press == 'a':
        y -= 1
        if y == 0:
            y = 1
    elif key_press == 'q':
        exit()

    if board[x][y] == "\x1b[1;30;47mX\x1b[0m":
        x = limit_x
        y = limit_y

    if x in range(31, 34) and y == 92:
        x = limit_x
        y = limit_y
        main2()

    if board[x][y] == '\x1b[1;33;41m1\x1b[0m':
        LOOK = '#'

    if board[x][y] == '\x1b[1;36;40m2\x1b[0m':
        LOOK += "/"

    if board[x][y] == '\x1b[1;30;47m3\x1b[0m':
        LOOK = ">" + LOOK

    if board[x][y] == '\x1b[1;36;45m4\x1b[0m':
        main3()

    x, y = insert_hero(board, x, y)

    return x, y

# BOSS GAME


def pick_number():
    """Chooses a random number"""
    number0 = random.randint(0, 9)
    number1 = random.randint(0, 9)
    number2 = random.randint(0, 9)
    numbers = (number0, number1, number2)
    return numbers


def check_duplicate(number):
    """Checks if digits of randomly selected number are repeated"""
    while True:
        if number[0] != number[1] and number[0] != number[2] and number[1] != number[2]:
            return number
            break
        else:
            number = pick_number()


def guess_number(number):
    """Takes correct imput from player"""
    print(number)
    information = ("""I am thinking of a 3-digit number. Try to guess what it is.

                    Here are some clues:

                    When I say:    That means:

                    Cold       No digit is correct.

                    Warm       One digit is correct but in the wrong position.

                    Hot        One digit is correct and in the right position.

                    I have thought up a number. You have 10 guesses to get it. """)
    print(information)
    i = 0
    while i < 5:
        i += 1
        print("Guess #", i)
        while True:
            try:
                user_input = tuple(input(">> "))
                while len(user_input) != 3:
                    print("Choose 3 digit number")
                    user_input = tuple(input(">> "))
                cnt = 0
                while cnt < 3:
                    if int(user_input[cnt]) not in number:
                        print("Cold")
                    elif int(user_input[cnt]) == number[cnt]:
                        print("Hot")
                    elif int(user_input[cnt]) in number:
                        print("Warm")
                    cnt += 1
                if user_input == number:
                    print("You've got it!")
                    break
            except ValueError:
                print("Choose 3 digit number")
    print("You loose !")


def main2():
    """Main function of inner game Hot-Worm"""
    number = pick_number()
    check_duplicate(number)
    guess_number(number)

# INVENTORY


def add_to_inventory(board, x, y, a, b, c, d, e, f, g, h, inventory):
    """adds descriptions of the items to inventory"""
    if board[x][y] == board[a][b]:
        inventory.update({"zbroja": 1})
    if board[x][y] == board[c][d]:
        inventory.update({"miecz": 1})
    if board[x][y] == board[e][f]:
        inventory.update({"peleryna": 1})
    if board[x][y] == board[g][h]:
        inventory.update({"oko maga": 1})

    return inventory


def print_table(inventory, order=None):
    """displays inventory"""
    print("Inventory:")
    print("{:>7} {:>13}".format('count', 'item name'))
    print("-" * 21)

    if order == "count,desc":
        for key, value in sorted(inventory.items(), key=lambda x: x[1], reverse=True):
            print("{:>7} {:>13}".format(value, key))

    if order == "count,asc":
        for key, value in sorted(inventory.items(), key=lambda x: x[1]):
            print("{:>7} {:>13}".format(value, key))

    if order == None:
        for key, value in inventory.items():
            print("{:>7} {:>13}".format(value, key))

    print("-" * 21)
    print("Total number of items: %s" % sum(inventory.values()))

# GUESS A number

list = sys.argv


def start():
    """Initializes the guess number game"""
    print("Welcome in ***Guess the Number*** game!")
    name = input("What is your name? ")
    print("Well ", name, ", I am thinking of a number between 1 and 30.")


def answer():
    """
    Checks if the answer is a digit, if the number is correct,
     tells whether the answer is  too high or too low.
    """
    number = random.randint(1, 30)
    while True:
        try:
            guess = int(input("What is your guess? "))
            if guess < number:
                print(guess, " is too low")
            if guess > number:
                print(guess, " is too high")
            if guess == number:
                print("YES!!! ", guess, " is my secret number! Congratulations!!!")
                exit()
        except ValueError:
            print("Number please!")
        continue


def exit():
    """Exit the guess number game"""
    repeat = input("Do you want to play again? Y/N ")
    if repeat == "y" or "Y":
        answer()
    else:
        quit()


def main3():
    """Main function of guess number game"""
    start()
    answer()


# MAIN


def main():
    """Main function of whole game"""
    print(INTRO)
    time.sleep(3)
    a, b, c, d, e, f, g, h = item_location()
    board = create_board()
    board = item_spawn(board, a, b, c, d, e, f, g, h)
    x, y = insert_hero(board)
    board = insert_boss(board)
    inventory = {}
    while True:
        os.system("clear")
        print_board(board)
        inventory = add_to_inventory(board, x, y, a, b, c, d, e, f, g, h, inventory)
        print_table(inventory, order=None)
        key_press = getch()
        x, y = move(key_press, x, y, board)
main()
