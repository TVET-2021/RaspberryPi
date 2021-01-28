import os
import time
import socket
import threading
import random
import configparser

class BingoServer:
    def __init__(self, port, max_people):
        self.port = port
        self.user_list = {}
        self.max_people = max_people

    def start(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(('', self.port))

        sock.listen(10)

        while True:
            try:
                client_socket, addr = sock.accept()

                user_name = client_socket.recv(1024)
                user_name = user_name.decode()

            except Exception as e:
                # print("! Error : ", e)
                continue

            self.user_list.setdefault(user_name, client_socket)
            print("> '", user_name, f"' participated | Total {len(self.user_list)}/{self.max_people}")

            client_thread = threading.Thread(target=self.handler_client, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()

    def handler_client(self, client_sock):

        try:
            while 1:
                pass
        except Exception as e:
            pass

        client_sock.close()

    def broadcast(self, value):
        for user_name, client_socket in self.user_list.items():
            client_socket.send(str(value).encode())

    def get_participated_people(self):
        return len(self.user_list)


def main():

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "bingo_server.cfg"))
    time.sleep(0.2)
    print("======" * 5)
    print("> Bingo server start")
    print("======" * 5)
    print()
    print("> Please wait for people to get in...")
    print()
    time.sleep(1)
    game_counter = 1
    number_list = []

    bingo_server = BingoServer(port=int(config["server"]["port"]), max_people=int(config["server"]["max_people"]))

    threading.Thread(target=bingo_server.start).start()

    while True:
        if bingo_server.get_participated_people() == bingo_server.max_people:

            if game_counter == 1:
                print()
                print("======" * 5)
                print("Start bingo game!!!")
                print("======" * 5)
                print()

                input(f"> 1st step | Next Number ")
            elif game_counter == 2:
                input(f"> 2nd step | Next Number ")
            elif game_counter == 3:
                input(f"> 3rd step | Next Number ")
            else:
                input(f"> {game_counter}nd step | Next Number ")

            while True:
                random_value = random.randint(0, 100)

                if len(number_list) == 101:
                    yes_or_no = input("! All of the number is used!!! Do you want to fresh history of number? (Y/N)")

                    if yes_or_no.upper() == 'N':
                        print("> Okay, bye~!!")
                        return
                    else:
                        number_list = []

                if not random_value in number_list:
                    number_list.append(random_value)
                    break

            print(">> Generated random number : ", random_value)
            print()
            bingo_server.broadcast(value=random_value)

            game_counter += 1
    # except Exception as e:
    #     print(e)

if __name__ == "__main__":
    main()

