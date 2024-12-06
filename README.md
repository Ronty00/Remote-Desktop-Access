# Remote-Desktop-Access
In our project enables seamless connection between a client computer and a server computer. Through this setup, the client can remotely access and control the server’s desktop environment, allowing for easy management of files, and Download files. 
Project Overview
This project provides a Remote Desktop Access solution, enabling a client computer to connect to and control a server computer remotely. The system supports executing commands, transferring files, and initiating screen-sharing sessions. It is implemented using Python with a GUI for user interaction and a server-side application to handle incoming connections.

Features
Remote Command Execution: Execute commands on the server from the client.
Directory Management: Navigate the server’s filesystem using commands like cd.
File Transfer: Download files from the server to the client.
Screen Sharing: View the server's desktop screen in real time (feature in progress).
How to Use
1. Prerequisites
Install Python (3.6 or later).
Install required dependencies:
Dependencies include tkinter, pillow, and mss.
2. Setup
Run the Server:

Navigate to the directory containing GuiServer.py.
Run the server:
bash
Copy code
python GuiServer.py
The server will start listening on the specified host ip and port.
Run the Client:

Navigate to the directory containing GuiClient.py.
Run the client:
bash
Copy code
python GuiClient.py
Enter the server's IP address and port to establish the connection.
3. Functionalities
Command Execution:
Enter commands in the client interface to execute them on the server. For example:
ls: List server directory contents.
cd <directory>: Change the directory on the server.
(Will work with all windows command related with file directory change or create, delete directory etc.)
File Transfer:
Use get <filename> to download files from the server.
Screen Sharing:
Start a screen-sharing session by clicking "Start Screen Sharing" on the client interface.
Future Updates
Enhanced Screen Sharing: Adding real-time screen updates for smoother visual interaction.
Multi-Platform Support: Optimizing for macOS and Linux clients.
File Uploads: Implementing a feature to send files from the client to the server.
If you would like to contribute, especially to enhance the screen-sharing feature, your efforts would be greatly appreciated! Feel free to submit pull requests or suggest improvements.

Credits
This project was developed as a part of hands-on learning in Python and networking. It leverages libraries like socket, tkinter, Pillow, and mss to create a functional remote desktop application.

