import socket
from threading import Thread
import sys, os


def generate_copy_filename(filename, number):
    """
    param: filename: name of file
    param: address: number of copy to write
    return : edited filename with copy number (filename_copy_number.format)
    """
    firstname = ""
    for char in filename:
        if not char == ".":
            firstname += char
        else:
            firstname += "_copy_" + str(number) + "."
    return firstname


def check_collision(filename):
    """
    param: filename: name of file
    return : if filename is already exists, return changed name, else return param: filename
    """
    copy_number = 0
    new_name = filename
    while True:
        if os.path.isfile(new_name):
            copy_number += 1
            new_name = generate_copy_filename(filename, copy_number)
        else:
            return new_name


def receive_file(connection, address):
    """
    param: connection: socket connection
    param: adress: adress of connection
    """

    print("Receiving a file from adress:", address)
    filename_size = int.from_bytes(connection.recv(1), 'big') #receive filename size
    filename = (connection.recv(filename_size)).decode() #receive filename
    filename = check_collision(filename)

    ### write data to file ###
    file = open(filename, "wb")
    while True:
        data = connection.recv(1024)
        if not data:
            break
        file.write(data)
    print("Received file with name:", filename)


if __name__ == "__main__":
    port = int(sys.argv[1])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))
    sock.listen()
    while True:
        connection, address = sock.accept()
        #when someone connects to socket, create Thread and run recieve_file function
        #Thread closes automatically after function returns
        thread = Thread(target=receive_file, args=(connection, address))
        thread.start()
