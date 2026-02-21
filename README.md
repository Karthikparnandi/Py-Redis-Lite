# Py-Redis-Lite: An Educational In-Memory Data Store

A lightweight, Redis-like in-memory key-value data store built from scratch in Python to demonstrate **Data Structures and Algorithms (DSA)** applied to **System Design**.

## Overview

Py-Redis-Lite is an educational project that implements a TCP-based server with an **LRU Cache** (Least Recently Used Cache) as the core data storage engine. The entire LRU Cache is built from scratch without using Python's built-in `OrderedDict` or `functools.lru_cache`, showcasing a deep understanding of fundamental data structures and their time complexity guarantees.

## Architecture

### Core Components

#### 1. LRU Cache (`lru_cache.py`)
The heart of this system, built with:
- **Doubly Linked List**: Maintains the order of access (most recently used at head, least recently used at tail)
- **Hash Map (Python Dictionary)**: Provides O(1) lookups to nodes in the linked list
- **Sentinel Nodes**: Eliminates edge case handling for cleaner code

**Time Complexity Guarantees:**
- `get(key)`: O(1)
- `set(key, value)`: O(1)
- `delete(key)`: O(1)

**Key Features:**
- Automatic eviction of least recently used items when capacity is exceeded
- Updates to existing keys re-position them as most recently used
- No dependencies on Python's built-in data structure implementations

#### 2. TCP Server (`server.py`)
A multi-threaded socket-based server that:
- Listens on port 6379 (standard Redis port)
- Handles concurrent client connections
- Parses and executes client commands
- Returns immediate responses to clients

**Supported Commands:**
- `GET <key>`: Retrieve value, returns "OK: <value>" or "NULL"
- `SET <key> <value>`: Store key-value pair, returns "OK"
- `DEL <key>`: Delete key, returns "OK" or "NULL"
- `PING`: Server health check, returns "PONG"
- `INFO`: Display cache statistics (size/capacity)

#### 3. Test Client (`client.py`)
A simple interactive client for testing server functionality.

## Why This Project Matters

### DSA Application
This project demonstrates:
1. **Doubly Linked List** - Efficient insertion/deletion at both ends (O(1))
2. **Hash Map** - Constant time lookups and insertions
3. **Combined Data Structure Design** - Solving the LRU problem optimally

### System Design Lessons
1. **Separation of Concerns** - Core cache logic isolated from networking
2. **Concurrency** - Multi-threaded server handling simultaneous clients
3. **Protocol Design** - Simple, text-based command protocol
4. **Capacity Management** - Automatic eviction policies

## Installation

### Prerequisites
- Python 3.7+
- No external dependencies

### Setup
```bash
git clone https://github.com/Karthikparnandi/Py-Redis-Lite.git
cd Py-Redis-Lite
```

## Usage

### Start the Server
```bash
python server.py
```

Expected output:
```
2024-XX-XX XX:XX:XX,XXX - INFO - Py-Redis-Lite server started on localhost:6379
2024-XX-XX XX:XX:XX,XXX - INFO - LRU Cache capacity: 100
```

### Connect with the Test Client
In another terminal:
```bash
python client.py
```

### Example Session
```
Connected to Py-Redis-Lite server on localhost:6379
Commands: GET <key>, SET <key> <value>, DEL <key>, PING, INFO, EXIT

>> SET user:1 "John Doe"
Response: OK

>> GET user:1
Response: OK: John Doe

>> SET user:2 "Jane Smith"
Response: OK

>> INFO
Response: Cache size: 2/100

>> DEL user:1
Response: OK

>> GET user:1
Response: NULL

>> EXIT
Disconnecting...
```

## Technical Specifications

### LRU Cache Implementation Details

**Node Structure:**
```python
class Node:
    key: str
    value: Any
    prev: Node  # Previous node in linked list
    next: Node  # Next node in linked list
```

**Cache Structure:**
```
Head (Sentinel) <-> [Most Recent] <-> ... <-> [Least Recent] <-> Tail (Sentinel)
     |
Hash Map: {key -> Node pointer}
```

### Server Configuration
- **Host**: localhost
- **Port**: 6379
- **Buffer Size**: 1024 bytes
- **Cache Capacity**: 100 items
- **Threading**: One thread per client connection

## Algorithm Complexity Analysis

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| GET       | O(1)            | O(1)             |
| SET       | O(1)            | O(1)             |
| DELETE    | O(1)            | O(1)             |
| Overall   | -               | O(capacity)      |

The O(1) guarantees are achieved by:
1. Hash Map provides O(1) node lookup
2. Doubly Linked List provides O(1) insertion/deletion at any position given the node pointer
3. No array resizing or complex operations needed

## Educational Value

This project is ideal for:
- **Interview Preparation**: LRU Cache is a classic system design interview question
- **Data Structure Mastery**: Hands-on implementation of advanced combined data structures
- **Networking Fundamentals**: Socket programming and multi-threaded servers
- **System Design**: Building scalable, efficient systems from first principles

## Future Enhancements (Educational)

- Persistence (RDB/AOF snapshots)
- Additional data structures (Lists, Sets, Hashes)
- Pub/Sub messaging
- Transaction support (MULTI/EXEC)
- Cluster support
- Authentication and ACLs

## File Structure

```
Py-Redis-Lite/
├── lru_cache.py     # LRU Cache implementation
├── server.py        # TCP server
├── client.py        # Test client
└── README.md        # This file
```

## Testing

To test the implementation:

1. **Start the server**: `python server.py`
2. **Run the client**: `python client.py`
3. **Test basic operations**:
   ```
   SET key1 value1
   GET key1
   SET key2 value2
   INFO
   DEL key1
   ```
4. **Verify capacity eviction**: Set more than 100 items and observe the least recently used items being evicted

## About the Author

This project was created to demonstrate a deep understanding of:
- Core data structures and algorithms
- System design principles
- Practical networking with Python
- Production-grade code quality and documentation

## License

This project is open source and available for educational purposes.

## References

- **LRU Cache Pattern**: Common system design interview question
- **Doubly Linked List**: Foundation for efficient caching strategies
- **Hash Map**: Essential for O(1) access patterns
- **Redis**: The production system this project emulates

---

**Note**: This is an educational implementation optimized for learning and clarity, not production use. For production caching, use actual Redis or similar mature systems.
