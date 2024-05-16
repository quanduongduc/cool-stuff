# Copy a file to a network socket without loading it into memory
# This is a zero-copy operation, meaning that the data is sent directly from the file to the network socket
# without passing through the application's memory space.
# As a result, This is a very efficient way to send large files over a network.
# The sendfile() system call is used to perform this operation.
# Tested on Linux.
# Usage: zero_copy_send_to_socket(destination_ip="localhost", destination_port=9999, source_file="hehe.txt") with nc -l 9999 > destination.txt on the destination machine.
# read more about zero copy: https://en.wikipedia.org/wiki/Zero-copy

import os
import socket


def zero_copy_send_to_socket(source_file, destination_ip, destination_port):
    source = os.open(source_file, os.O_RDONLY)
    source_size = os.fstat(source).st_size

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((destination_ip, destination_port))

        destination = s.fileno()

        os.sendfile(destination, source, 0, source_size)

FILE_SIZE = 5 * 10**9  # 5GB
FILE_NAME = "temp.txt"

if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w") as f:
        for _ in range(5 * 10**6):
            f.write("A" * 1024)  # Write a 1KB string

zero_copy_send_to_socket(
    destination_ip="localhost", destination_port=9999, source_file=FILE_NAME
)
