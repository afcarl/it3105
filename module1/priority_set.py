import heapq

class NodePrioritySet(object):
    """
    This class combines a heap (swift insertion time for new nodes while maintaining order)
    and a dictionary (quick lookup)
    """
    def __init__(self):
        self.counter = 0  # used to ensure LIFO behavior for nodes with equal priority
        self.heap = []
        self.dict = {}

    def add(self, node, priority):
        if node not in self.dict:
            heapq.heappush(self.heap, (priority, -self.counter, node))
            self.counter += 1
            self.dict[node] = node

    def pop(self):
        priority, counter, node = heapq.heappop(self.heap)
        del self.dict[node]
        return node

    def __getitem__(self, node):
        return self.dict[node]

    def __contains__(self, node):
        return node in self.dict

    def __iter__(self):
        return self.dict.__iter__()

    def is_empty(self):
        return len(self.heap) == 0
