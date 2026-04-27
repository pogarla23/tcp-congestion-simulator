import random

#simulating random packets 
class Network:
    def __init__(self, capacity=50, loss_rate=5):
        self.capacity = capacity
        self.loss_rate = loss_rate
        self.total_sent = 0

    #for vegas
    def get_rtt(self, cwnd):
        queue_depth = cwnd - self.capacity
        return 1.0 + queue_depth * 0.1

    
    def should_lose(self, cwnd):
        base = self.loss_rate / 100.0
        overflow =  ((cwnd - self.capacity) / self.capacity) 
        
        return random.random() < min(base + overflow, 0.95)