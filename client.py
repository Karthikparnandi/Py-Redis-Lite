"""
Simple TCP client to test the Py-Redis-Lite server.
"""

import socket
import sys

HOST = 'localhost'
PORT = 6379


def send_command(sock, command):
    """Send a command to the server and receive the response."""
    sock.sendall(command.encode('utf-8') + b'\n')
    response = sock.recv(1024).decode('utf-8').strip()
    return response


def main():
    """Interactive client for Py-Redis-Lite server."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print(f"Connected to Py-Redis-Lite server on {HOST}:{PORT}")
        print("Commands: GET <key>, SET <key> <value>, DEL <key>, PING, INFO, EXIT\n")

        while True:
            try:
                command = input(">> ").strip()

                if not command:
                    continue

                if command.upper() == "EXIT":
                    print("Disconnecting...")
                    break

                response = send_command(sock, command)
                print(f"Response: {response}\n")

            except KeyboardInterrupt:
                print("\nDisconnecting...")
                break

    except ConnectionRefusedError:
        print(f"Error: Could not connect to server on {HOST}:{PORT}")
        print("Make sure the server is running: python server.py")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        sock.close()


if __name__ == "__main__":
    main()
