class BaseAlgorithm:
    
    #what do all the algorithms share: window size, threshold, and history for calculating the graph 
    def __init__(self):
        self.cwnd = 1
        self.ssthresh = 1
        self.history = []
 
    def step(self, packet_loss=False):
        raise NotImplementedError
 