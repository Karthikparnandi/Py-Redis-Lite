"""
LRU Cache implementation from scratch using a Doubly Linked List and Hash Map.
Guarantees O(1) time complexity for get, set, and delete operations.
"""


class Node:
    """Node for the Doubly Linked List."""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    Least Recently Used (LRU) Cache implementation.

    Uses a Doubly Linked List to maintain the order of access and a Hash Map
    to store pointers to nodes, guaranteeing O(1) time complexity for all operations.

    Args:
        capacity (int): Maximum number of items the cache can hold.
    """

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")

        self.capacity = capacity
        self.cache = {}  # Hash Map: key -> Node

        # Sentinel nodes to avoid edge case handling
        self.head = Node(None, None)  # Most recently used end
        self.tail = Node(None, None)  # Least recently used end

        # Connect sentinels
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove_node(self, node):
        """Remove a node from the doubly linked list. O(1) operation."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node):
        """Add a node right after the head (most recently used position). O(1) operation."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        """
        Get the value associated with the key.

        Marks the accessed node as most recently used.

        Args:
            key: The key to retrieve.

        Returns:
            The value associated with the key, or None if not found.

        Time Complexity: O(1)
        """
        if key not in self.cache:
            return None

        node = self.cache[key]
        # Move the accessed node to the head (most recently used)
        self._remove_node(node)
        self._add_to_head(node)

        return node.value

    def set(self, key, value):
        """
        Set a key-value pair in the cache.

        If the key already exists, update its value.
        If the cache is at capacity, evict the least recently used item.

        Args:
            key: The key to set.
            value: The value to associate with the key.

        Time Complexity: O(1)
        """
        if key in self.cache:
            # Update existing node
            node = self.cache[key]
            node.value = value
            # Move to head (most recently used)
            self._remove_node(node)
            self._add_to_head(node)
        else:
            # Create new node
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)

            # Check if we exceeded capacity
            if len(self.cache) > self.capacity:
                # Remove the least recently used node (before tail)
                lru_node = self.tail.prev
                self._remove_node(lru_node)
                del self.cache[lru_node.key]

    def delete(self, key):
        """
        Delete a key-value pair from the cache.

        Args:
            key: The key to delete.

        Returns:
            True if the key was found and deleted, False otherwise.

        Time Complexity: O(1)
        """
        if key not in self.cache:
            return False

        node = self.cache[key]
        self._remove_node(node)
        del self.cache[key]
        return True

    def size(self):
        """Get the current number of items in the cache. O(1) operation."""
        return len(self.cache)

    def is_empty(self):
        """Check if the cache is empty. O(1) operation."""
        return len(self.cache) == 0

    def clear(self):
        """Clear all items from the cache. O(1) operation."""
        self.cache.clear()
        self.head.next = self.tail
        self.tail.prev = self.head
