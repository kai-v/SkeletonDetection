#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: kaivelagapudi
"""
from rad import RAD
from hjpd import HJPD
from hod import HOD


if __name__ == "__main__": 
    
    """ Generate train and test files for all 3 techniques """

    r = RAD() 
    r.run(1)
    r.run(2)
    
    hj = HJPD() 
    hj.run(1)
    hj.run(2)
    
    hd = HOD() 
    hd.run(1)
    hd.run(2)