from algorithms.base import BaseAlgorithm

#code references: https://tcpcc.systemsapproach.org/avoidance.html

class Vegas(BaseAlgorithm):
    # reacts to rising RTT before packets drop

    def __init__(self):
        super().__init__()
        self.initial_rtt = None  # minimum RTT seen
        self.rtt = 1.0
        self.alpha = 2
        self.beta = 4

    # THREE CASEs
    #packet loss --> divide sshtresh window by half, decrease window by 1
    
    #slow start --> if its slower than sstrhes increment by 1
    
    # if the window size is greater there
        #difference = expected - actual * initial_rtt
            #if difference < alpha --> cwnd++
            #if difference > beta --> cwnd--
    def step(self, packet_loss=False, rtt=None):
        
        if rtt is not None:
            self.rtt = rtt
            if self.initial_rtt is None or rtt < self.initial_rtt:
                self.initial_rtt = rtt

        
        if packet_loss:
            self.ssthresh = self.cwnd // 2
            self.cwnd -= 1

        elif self.cwnd < self.ssthresh:
            self.cwnd += 1

        elif self.initial_rtt:
            
            #expected = cwnd / initial_rtt
            #actual = cwnd / rtt 
            diff = ((self.cwnd/self.initial_rtt)- ( self.cwnd/self.rtt))*self.initial_rtt
            
            
            if diff < self.alpha:
                self.cwnd += 1
            elif diff > self.beta:
                self.cwnd -= 1
                

        self.history.append(self.cwnd)
        return self.cwnd