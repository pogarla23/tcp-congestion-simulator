from algorithms.base import BaseAlgorithm

#References for link: https://www.geeksforgeeks.org/computer-networks/tcp-congestion-control-algorithms-reno-new-reno-bic-cubic/
#Review from princeton psudocode: https://www.cs.princeton.edu/courses/archive/fall16/cos561/papers/Cubic08.pdf

#C constant for window growth --> set to 0.4
#t time elapsed since last event
#K period to grow in Wmax* beta 
#Wmax  window size since last loss event

class Cubic(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.C = 0.4  
        self.t = 0
        self.W_max = 64 #gave errors when set to 0
        self.K = 0
        
    #THREE CASES OCCUR: packet loss, slow start, congestion avoidance
    def step(self, packet_loss=False):
        
        #update Wmax, reset time, cwnd is new trhesh to meet, K use fomrula 
        if packet_loss:
            self.W_max = self.cwnd
            self.t = 0
            Beta = 0.7 
            self.ssthresh = self.cwnd * Beta
            self.cwnd = int(self.ssthresh)
    
            # K = cube_root(W_max * 0.3 / C)
            self.K = (self.W_max*0.3 / self.C) ** (1/3)
            
        #if it's a slow start 
        elif self.cwnd < self.ssthresh:
            self.cwnd *= 2
            
            if self.cwnd >= self.ssthresh:
                self.t = 0
        
        #no loss or below, increment as such and updated  
        #formula for Cubic: C * (t-K)^3 + W_max       
        else:
            self.t += 1
            self.cwnd = int(self.C * ((self.t - self.K) ** 3) + self.W_max)

        self.history.append(self.cwnd)
        return self.cwnd