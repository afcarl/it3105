import heapq

class NodePrioritySet(object):
    def __init__(self):
        self.heap = []
        self.dict = {}

    def add(self, node, priority):
        if node not in self.dict:
            heapq.heappush(self.heap, (priority, node))
            self.dict[node] = node

    def pop(self):
        priority, item = heapq.heappop(self.heap)
        del self.dict[item]
        return item

    def __getitem__(self, node):
        return self.dict[node]

    def __contains__(self, node):
        return node in self.dict

    def is_empty(self):
        return len(self.heap) == 0
