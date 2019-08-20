Client-Server Simulation
========================

Introduction
------------

This first version consists of four new modules:

- ClientServerSimul.py
- ClientConnection.py
- ServerConnection.py
- ClientThread.py
- SchcConfig.py
- ClientSend.py

This second version implements the Socket library to perform the communication between a client and a server, using the localhost
address 127.0.0.1, port 1234, TCP protocol and threads on the server to allow communication **from several clients to a server**.

At the end of a successful communication, the simulation records the time in seconds at that instant in the text file
client_server_simulation.txt, and restarts sending the same message from the client to the server.

How to run this simulation
--------------------------

- Run Server

    ```
    python3 ClientServerSimul.py --r server
    ```

- Run Client

    ```
    python3 ClientServerSimul.py --r client
    ```

Rulemanager Test
=====================

## Example with the simulator

- First Rulemanager test

    ```
    python3 test_frag_new.py
    ```
## Example without the simulator

- First Rulemanager test

    ```
    python3 test_compress.py
    ```
