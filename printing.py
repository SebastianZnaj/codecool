#!/usr/bin/env python created by Sebastian Znaj
from reports import *


def games_count_print():
    print("1.How many games are in the file?")
    print("Games count is: " + str(count_games(data_file_name))+"\n")


def decide_print(data_file_name, year):
    print("2. Is there a game from a given year?")
    if decide(data_file_name, year) is True:
        print("Yes")
    else:
        print("No")


def get_latest_print():
    print("3. Is there a game from a given year?")




def main():
    games_count_print()
    decide_print(data_file_name, year)
if __name__ == '__main__':
    main()
