import os
import time
import socket
import random
import configparser

def bingo_board_print():
    print()
    print()

    for i in range(5):
        for j in range(5):
            print(bingo_board[i][j], end='\t')

        print()

def check_matched_line():
    total_matching_counter = 0

    # Vertical
    for i in range(5):
        matching_counter = 0
        for j in range(5):
            if "*" in bingo_board[i][j]:
                matching_counter += 1

        if check_is_matched(matching_counter):
            total_matching_counter += 1

    # Horizontal
    for i in range(5):
        matching_counter = 0
        for j in range(5):
            if "*" in bingo_board[j][i]:
                matching_counter += 1

        if check_is_matched(matching_counter):
            total_matching_counter += 1

    # diagonal top left to bottom right
    matching_counter = 0
    for i in range(5):
        if "*" in bingo_board[i][i]:
            matching_counter += 1

    if check_is_matched(matching_counter):
        total_matching_counter += 1

    # diagonal top right to bottom left
    matching_counter = 0
    for i in range(5):
        if "*" in bingo_board[i][4 - i]:
            matching_counter += 1

    if check_is_matched(matching_counter):
        total_matching_counter += 1

    if total_matching_counter >= 3:
        pprint_total_matching_count(total_matching_counter)
        print()
        print("======" * 5)
        print("# Congratulations !!! You are winner !!!")
        print("======" * 5)

        return True
    else:
        pprint_total_matching_count(total_matching_counter)
        return False


def check_is_matched(matched_num):
    if matched_num == 5:
        return True

    return False


def pprint_total_matching_count(total_count):
    if total_count == 1:
        print("> One line is matched")

    elif total_count == 2:
        print("> Two lines are matched")
    elif total_count == 3:
        print("> Three lines are matched")

try:
    print()
    print("======" * 5)
    print("> Bingo client start")
    print("======" * 5)


    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "bingo_client.cfg"))
    time.sleep(1)

    ip = config["server"]["ip"]
    port = int(config["server"]["port"])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    print(f">> Success to connect bingo server\t Server ip : {ip}, port : {port}")
    print()

    name = input("> Enter the your name : ")
    sock.send(str(name).encode())

    while True:
        # Create bingo board
        bingo_item_buffer = [] # For checking duplicated item
        bingo_board = []

        for _ in range(5):
            bingo_board_line = []

            for _ in range(5):
                item = str(random.randint(0, 100))

                while True:
                    if not item in bingo_item_buffer:
                        break
                    else:
                        item = str(random.randint(0, 100))

                bingo_board_line.append(item)
                bingo_item_buffer.append(item)

            bingo_board.append(bingo_board_line)

        while True:
            bingo_board_print()
            if check_matched_line():
                break

            number = sock.recv(1024) #input("Insert number : ")

            try:
                number = int(number.decode())
                print("> Received number : ", number)
            except ValueError:
                print("! Please insert only number")
                continue

            for i in range(5):
                for j in range(5):
                    if bingo_board[i][j] == str(number):
                        bingo_board[i][j] += "*"



        yes_or_no = input("Next (Y/N) ?")

        if yes_or_no.upper() == 'N':
            break

    sock.close()
except Exception as e:
    print("Error : ", e)
    input()