#!/usr/bin/env python created by Sebastian Znaj
data_file_name = 'game_stat.txt'
year = "2000"
genre = "First-person shooter"
title = "Counter-Strike"


def file_convert_to_list():
    """Convertinge file to nested lists in list"""
    with open(data_file_name, 'r') as games:
        games_list = []
        for line in games:
            row = line[:-1].split("\t")
            games_list.append(row)
        return games_list


def count_games(data_file_name):
    """Count how many games is in data_file_name"""
    games_list = file_convert_to_list()
    count = 0
    for line in games_list:
        count += 1
    return count


def decide(data_file_name, year):
    """Looking for year in data_file_name"""
    games_list = file_convert_to_list()
    ans = False
    for line in games_list:
        year = str(year)
        if year in line[2]:
            ans = True
    return ans


def get_latest(data_file_name):
    """Check which game is released latest"""
    games_list = file_convert_to_list()
    last = []
    for line in games_list:
        last.append(line[2])
    index = last.index(max(last))
    game = games_list[index][0]
    return game


def count_by_genre(data_file_name, genre):
    """Counts how many games are in specified games category"""
    games_list = file_convert_to_list()
    genre_list = []
    count = 0
    for line in games_list:
        genre_list.append(line[3])
    for i in genre_list:
        if i == genre:
            count += 1
    return(count)


def get_line_number_by_title(data_file_name, title):
    """"Display the line number of given title"""
    games_list = file_convert_to_list()
    titles_list = []
    for line in games_list:
        titles_list.append(line[0])
    for i in titles_list:
        if i == title:
            index = titles_list.index(i)
            index += 1
    if title not in titles_list:
        raise ValueError("Title is not in data base!")
    return index


def sort_abc(data_file_name):
    """Give alphabetic order of titles_listt"""
    games_list = file_convert_to_list()
    titles_list = []
    for line in games_list:
        titles_list.append(line[0])
    sorted_list = tuple(sorted(titles_list))
    return sorted_list


def get_genres(data_file_name):
    """Gives a list of not duplicated genres"""
    games_list = file_convert_to_list()
    genres = []
    for line in games_list:
        genres.append(line[3])
    genres = list(sorted(set(genres)))
    return genres


def when_was_top_sold_fps(data_file_name):
    """Gives the year of top sold FPS game"""
    games_list = file_convert_to_list()
    FPS_list = []
    FPS_list_nested = []
    for i in games_list:
        if i[3] == "First-person shooter":
            FPS_list_nested.append([i[0], i[1], i[2]])
            FPS_list.append(float(i[1]))
            best = max(FPS_list)
    if not "First-person shooter"in i[3]:
        raise ValueError("There's no First-person shooter game!")
    index = FPS_list.index(best)
    year_of_best = int(FPS_list_nested[index][2])
    return year_of_best


def main():
    """Main function of this program"""
    games_list = file_convert_to_list()
    decide(data_file_name, year)
    count_games(data_file_name)
    get_latest(data_file_name)
    count_by_genre(data_file_name, genre)
    get_line_number_by_title(data_file_name, title)
    sort_abc(data_file_name)
    get_genres(data_file_name)
    when_was_top_sold_fps(data_file_name)
if __name__ == '__main__':
    main()
