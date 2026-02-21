"""
TCP Server for Py-Redis-Lite - An in-memory, Redis-like data store.

Listens on port 6379 and handles GET, SET, and DEL commands.
Uses an LRU Cache as the core data storage engine.
"""

import socket
import threading
import logging
from lru_cache import LRUCache

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Server configuration
HOST = 'localhost'
PORT = 6379
BUFFER_SIZE = 1024
CACHE_CAPACITY = 100


class RedisLiteServer:
    """
    A lightweight, Redis-like TCP server with an LRU Cache backend.
    """

    def __init__(self, host=HOST, port=PORT, capacity=CACHE_CAPACITY):
        self.host = host
        self.port = port
        self.cache = LRUCache(capacity)
        self.server_socket = None
        self.running = False

    def start(self):
        """Start the TCP server."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True

            logger.info(f"Py-Redis-Lite server started on {self.host}:{self.port}")
            logger.info(f"LRU Cache capacity: {self.cache.capacity}")

            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    logger.info(f"Client connected: {client_address}")

                    # Handle client in a separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()

                except KeyboardInterrupt:
                    logger.info("Server shutting down...")
                    break
                except Exception as e:
                    logger.error(f"Error accepting client connection: {e}")

        except socket.error as e:
            logger.error(f"Socket error: {e}")
        finally:
            self.stop()

    def handle_client(self, client_socket, client_address):
        """
        Handle commands from a connected client.

        Supported commands:
        - GET <key>
        - SET <key> <value>
        - DEL <key>
        - PING
        - INFO
        """
        try:
            while self.running:
                data = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()

                if not data:
                    break

                logger.info(f"Received from {client_address}: {data}")
                response = self.process_command(data)

                client_socket.sendall(response.encode('utf-8') + b'\n')

        except Exception as e:
            logger.error(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
            logger.info(f"Client disconnected: {client_address}")

    def process_command(self, command):
        """
        Parse and execute a command.

        Returns the response as a string.
        """
        parts = command.split(None, 2)  # Split on whitespace, max 3 parts

        if not parts:
            return "ERROR: Empty command"

        cmd = parts[0].upper()

        try:
            if cmd == "GET":
                if len(parts) < 2:
                    return "ERROR: GET requires a key"
                key = parts[1]
                value = self.cache.get(key)
                return f"OK: {value}" if value is not None else "NULL"

            elif cmd == "SET":
                if len(parts) < 3:
                    return "ERROR: SET requires a key and value"
                key, value = parts[1], parts[2]
                self.cache.set(key, value)
                return "OK"

            elif cmd == "DEL":
                if len(parts) < 2:
                    return "ERROR: DEL requires a key"
                key = parts[1]
                success = self.cache.delete(key)
                return "OK" if success else "NULL"

            elif cmd == "PING":
                return "PONG"

            elif cmd == "INFO":
                size = self.cache.size()
                capacity = self.cache.capacity
                return f"Cache size: {size}/{capacity}"

            else:
                return "ERROR: Unknown command"

        except Exception as e:
            logger.error(f"Error processing command '{command}': {e}")
            return f"ERROR: {str(e)}"

    def stop(self):
        """Stop the server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        logger.info("Server stopped")


if __name__ == "__main__":
    server = RedisLiteServer()
    server.start()
