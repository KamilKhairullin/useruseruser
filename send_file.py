import sys, os
import socket
from threading import Thread


def send_file(filename, address, port):
    """
    param: filename: name of file in current directory to sendall
    param: address: address to send to
    param: portn: port to send to
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((address, port))
    if os.path.isfile(filename):
        sock.sendall(len(filename).to_bytes(1, 'big')) #sending filename
        sock.sendall(str(filename).encode())
        file_size = os.path.getsize(filename)  #size of file
        sent = 0
        file = open(filename, "rb")
        while True:
            print(f"{sent} of {file_size} bytes sent - {sent * 100 / file_size :.2f}% done")
            buf = file.read(1024) #send data of file
            if not buf:
                break
            sock.sendall(buf)
            sent += len(buf)
        print("Finished!")
    else:
        print("Failed.")

if __name__ == "__main__":
    args = sys.argv[1:4]
    filename, address, port = args
    send_file(filename, address, int(port))
