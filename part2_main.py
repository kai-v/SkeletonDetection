#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: kaivelagapudi
"""
from reformat_data import reformat
from learning import svm_learn
import sys
 
if __name__ == "__main__": 
    
    
    """ Reformats the output train data ( mode = 1) and test data ( mode = 2 ) 
   fro all 3 representations created in Part 1 """

    r = reformat() 
    r.run(1)
    r.run(2)
    
        
    """ 
    Mode 1 = Rad
    Mode 2 = HJPD 
    Mode 3 = HOD   """
    
    name = sys.argv[1]
    
    if name == 'rad':
        mode = 1
    elif name == 'hjpd':
        mode = 2
    elif name == 'hod':
        mode = 3
    else:
           raise ValueError("Choices are rad, hjpd or hod")

    l = svm_learn()
    l.train_svm(mode)