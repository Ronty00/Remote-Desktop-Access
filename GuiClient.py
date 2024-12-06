import socket
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
from zlib import decompress
from PIL import Image, ImageTk
import io

WIDTH = 1920
HEIGHT = 1080

class RATClient:
    def __init__(self, host, port, command_output):
        self.host = host
        self.port = port
        self.command_output = command_output
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            messagebox.showinfo("Success", "Connected to server")
            self.listen_server()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

    def listen_server(self):
        while self.connected:
            try:
                data = self.client_socket.recv(4096).decode()
                if data:
                    self.receive_data(data)
            except Exception as e:
                print("Error listening to server:", e)
                self.connected = False
                break

    def receive_data(self, data):
        if data.startswith("Server output:"):
            output = data.split(":", 1)[1]
            self.command_output.insert(tk.END, f"Server output: {output}\n")
        else:
            print("Received:", data)
            self.command_output.insert(tk.END, f"Received: {data}\n")

    def send_command(self, command):
        if self.connected:
            try:
                self.client_socket.send(command.encode())
                self.command_output.insert(tk.END, f"Command Sent: {command}\n")
            except Exception as e:
                print("Error sending command:", e)
                messagebox.showerror("Error", f"Failed to send command: {e}")
        else:
            messagebox.showwarning("Warning", "Not connected to server")

class RATGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Remote Administration Tool")
        self.master.geometry("1000x800")

        self.client = None
        self.command_output = tk.Text(self.master, wrap='word', height=30, width=70)
        self.command_output.pack()

        self.create_widgets()

    def create_widgets(self):
        self.host_label = ttk.Label(self.master, text="Server Host:")
        self.host_label.pack()

        self.host_entry = ttk.Entry(self.master)
        self.host_entry.pack()

        self.port_label = ttk.Label(self.master, text="Server Port:")
        self.port_label.pack()

        self.port_entry = ttk.Entry(self.master)
        self.port_entry.pack()

        self.connect_button = ttk.Button(self.master, text="Connect", command=self.connect_to_server)
        self.connect_button.pack()

        self.command_label = ttk.Label(self.master, text="Command:")
        self.command_label.pack()

        self.command_entry = ttk.Entry(self.master)
        self.command_entry.pack()

        self.send_button = ttk.Button(self.master, text="Send Command", command=self.send_command)
        self.send_button.pack()

        self.download_button = ttk.Button(self.master, text="Download File", command=self.download_file)
        self.download_button.pack()

        self.share_button = ttk.Button(self.master, text="Start Screen Sharing", command=self.start_screen_share)
        self.share_button.pack()

    def connect_to_server(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        self.client = RATClient(host, port, self.command_output)
        Thread(target=self.client.connect).start()

    def send_command(self):
        if self.client:
            command = self.command_entry.get()
            self.client.send_command(command)
        else:
            messagebox.showwarning("Warning", "Not connected to server")

    def download_file(self):
        pass

    def start_screen_share(self):
        if self.client:
            self.client.send_command("share")
            Thread(target=self.receive_screen_share).start()
        else:
            messagebox.showwarning("Warning", "Not connected to server")

    def receive_screen_share(self):
        while self.client.connected:
            try:
                size_bytes = self.client.client_socket.recv(4)
                size = int.from_bytes(size_bytes, byteorder='big')
                pixels_bytes = b''
                while len(pixels_bytes) < size:
                    pixels_bytes += self.client.client_socket.recv(4096)
                img = Image.frombytes('RGB', (WIDTH, HEIGHT), decompress(pixels_bytes))
                img = ImageTk.PhotoImage(img)
                self.command_output.image = img
                self.command_output.insert(tk.END, '\n')
                self.command_output.image_create(tk.END, image=img)
            except Exception as e:
                print("Error receiving screen share:", e)
                break

def main():
    root = tk.Tk()
    app = RATGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
