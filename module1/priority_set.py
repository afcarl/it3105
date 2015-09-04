import heapq

class PrioritySet(object):
    def __init__(self):
        self.my_heap = []
        self.my_set = set()

    def add(self, item, priority):
        if item not in self.my_set:
            heapq.heappush(self.my_heap, (priority, item))
            self.my_set.add(item)

    def pop(self):
        priority, item = heapq.heappop(self.my_heap)
        self.my_set.remove(item)
        return item

    def exists(self, item):
        return item in self.my_set
