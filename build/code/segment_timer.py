# -*- coding: utf-8 -*-

import time

def timer(start, tStart=None):
    
    """
    Timer function.
    start: True=start timer (Boolean), False=end timer.
    tStart: start time (float)<time.time(), default None.
    Start timer with timer(True), returns current time.
    End timer with timer(False,t0), returns time elapsed since t0.
    """
    
    assert isinstance(start, bool), 'start must be Boolean'

    if tStart != None:
        assert isinstance(tStart, float), 'tStart must be a float'
    
    if start:  
        
        return time.time()
        
    else:
        
        tEnd = time.time()
        
        assert tStart <= tEnd,'tStart should be <= current time'
        
        return tEnd - tStart
