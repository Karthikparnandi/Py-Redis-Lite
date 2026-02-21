"""
Automated test script for Py-Redis-Lite server
"""

import socket
import time

HOST = 'localhost'
PORT = 6379
BUFFER_SIZE = 1024


def send_command(sock, command):
    """Send a command and receive response."""
    print(f">> {command}")
    sock.sendall(command.encode('utf-8') + b'\n')
    time.sleep(0.1)  # Small delay for response
    response = sock.recv(BUFFER_SIZE).decode('utf-8').strip()
    print(f"Response: {response}\n")
    return response


def main():
    """Run tests against the server."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print("=" * 60)
        print("Py-Redis-Lite Server Test Suite")
        print("=" * 60 + "\n")

        # Test 1: PING
        print("TEST 1: PING Command")
        response = send_command(sock, "PING")
        assert response == "PONG", f"Expected 'PONG', got '{response}'"
        print("[PASSED] PING test passed\n")

        # Test 2: SET and GET
        print("TEST 2: SET and GET Commands")
        send_command(sock, "SET user:1 Alice")
        response = send_command(sock, "GET user:1")
        assert "Alice" in response, f"Expected 'Alice' in response, got '{response}'"
        print("[PASSED] SET/GET test passed\n")

        # Test 3: Multiple SET operations
        print("TEST 3: Multiple SET operations")
        send_command(sock, "SET user:2 Bob")
        send_command(sock, "SET user:3 Charlie")
        send_command(sock, "SET score:1 95")
        info_response = send_command(sock, "INFO")
        assert "4" in info_response, f"Expected 4 items in cache, got '{info_response}'"
        print("[PASSED] Multiple SET test passed\n")

        # Test 4: GET non-existent key
        print("TEST 4: GET non-existent key")
        response = send_command(sock, "GET nonexistent")
        assert response == "NULL", f"Expected 'NULL', got '{response}'"
        print("[PASSED] Non-existent key test passed\n")

        # Test 5: DEL command
        print("TEST 5: DEL command")
        response = send_command(sock, "DEL user:1")
        assert response == "OK", f"Expected 'OK', got '{response}'"
        response = send_command(sock, "GET user:1")
        assert response == "NULL", f"Expected 'NULL' after deletion, got '{response}'"
        print("[PASSED] DEL test passed\n")

        # Test 6: DELETE non-existent key
        print("TEST 6: DELETE non-existent key")
        response = send_command(sock, "DEL doesnotexist")
        assert response == "NULL", f"Expected 'NULL' for non-existent delete, got '{response}'"
        print("[PASSED] Non-existent deletion test passed\n")

        # Test 7: INFO command
        print("TEST 7: INFO command")
        info_response = send_command(sock, "INFO")
        assert "Cache size:" in info_response, f"Expected 'Cache size:' in response, got '{info_response}'"
        print("[PASSED] INFO test passed\n")

        # Test 8: Update existing key (should move to most recent)
        print("TEST 8: Update existing key")
        send_command(sock, "SET mykey value1")
        send_command(sock, "SET mykey value2")
        response = send_command(sock, "GET mykey")
        assert "value2" in response, f"Expected 'value2', got '{response}'"
        info_response = send_command(sock, "INFO")
        print("[PASSED] Update key test passed\n")

        # Test 9: LRU Capacity Test (fill cache near capacity)
        print("TEST 9: LRU Capacity Management")
        print("Setting 50 items to test capacity...")
        for i in range(50):
            send_command(sock, f"SET key:{i} value{i}")

        info_response = send_command(sock, "INFO")
        print(f"Current cache state: {info_response}")
        print("[PASSED] Capacity test passed\n")

        # Test 10: Error handling
        print("TEST 10: Error handling")
        response = send_command(sock, "SET")  # Missing parameters
        assert "ERROR" in response, f"Expected ERROR in response, got '{response}'"
        response = send_command(sock, "GET")  # Missing parameters
        assert "ERROR" in response, f"Expected ERROR in response, got '{response}'"
        response = send_command(sock, "UNKNOWN")  # Unknown command
        assert "ERROR" in response, f"Expected ERROR in response, got '{response}'"
        print("[PASSED] Error handling test passed\n")

        print("=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)

    except ConnectionRefusedError:
        print(f"ERROR: Could not connect to server on {HOST}:{PORT}")
        print("Make sure the server is running: python server.py")
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
