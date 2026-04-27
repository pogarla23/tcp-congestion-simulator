#RENO

# slow start, slow growth within congestion window size
# or ater period of state of no activity
#readon it allows probing available bandwith in controlled way
# start to congestion avoidance segment after accomplishing a thrshold   
# fast retransmit
# fast recovery 

from algorithms.base import BaseAlgorithm
 
class Reno(BaseAlgorithm):
    def __init__(self):
        super().__init__()
 
    #if cwnd < thresh --> double window
    #if cwnd >= thresh --> increase by 1 window
    #if packet loss --> cut window in half. restart size of window
    
    def step(self, packet_loss=False):
        
        if packet_loss:
            self.ssthresh = self.cwnd//2
            self.cwnd = 1
            
        elif self.cwnd < self.ssthresh:
            self.cwnd *= 2
            
        else:
            self.cwnd += 1
 
        self.history.append(self.cwnd)
        return self.cwnd