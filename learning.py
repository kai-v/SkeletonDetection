#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: kaivelagapudi
"""

import sys
import os
import numpy as np

from libsvm.svmutil import *
from commonutil import *
from sklearn.metrics import confusion_matrix

class svm_learn:
    
    def __init__(self):
        pass
    
    """Get the formatted train and test files for RAD """
    def rad_train_and_test_files(self):
        
         train = "formatted/rad_d1"
         test = "formatted/rad_d1.t"
        
         return (train,test)
     
    """Get the formatted train and test files for HJPD """
     
    def hjpd_train_and_test_files(self):
        
         train = "formatted/hjpd_d1"
         test = "formatted/hjpd_d1.t"
        
         return (train,test)
     
    """Get the formatted train and test files for HOD """
     
    def hod_train_and_test_files(self):
        
         train = "formatted/hod_d1"
         test = "formatted/hod_d1.t"
        
         return (train,test)
     
        
    """Save to an external file """
     
    def save_to_file(self,file_name,p_label):
        
        name = file_name + '.predict'       
        output_file = open(name, 'w')

        for i in p_label:
            output_file.write(str(int(i))+'\n')

        
    def train_svm(self,mode):
        
        #RAD 
       if mode == 1:    
           print("RAD")
           train,test = self.rad_train_and_test_files()
           params = '-c 0.03125 -g 1.0' #Values given by grid search
           
        #HJPD
       elif mode == 2:   
           print("HJPD")
           train,test = self.hjpd_train_and_test_files()
           params = '-c 2.0 -g 0.125' #Values given by grid search
           
        #HOD 
       elif mode == 3:   
           print("HOD")
           train,test = self.hod_train_and_test_files()
           params = '-c 8.0 -g 0.125' #Values given by grid search
           
       else:
           raise ValueError("Valid entries are 1 , 2 or 3")
                     
               
       train_labels, train_data = svm_read_problem(train, return_scipy=True)
       test_labels, test_data = svm_read_problem(test, return_scipy=True)
       print("Read the files")
       
       if mode == 3:           
           """Scale data for HOD which uses 8 bins vs 10"""
       
           scale_param_train = csr_find_scale_param(train_data, lower=0,upper=0.4)
           scale_param_test = csr_find_scale_param(test_data, lower=0,upper=0.4)   
           train_data_scaled = csr_scale(train_data, scale_param_train)
           test_data_scaled = csr_scale(test_data, scale_param_test)      
           print("Scaled the data")
          
           model = svm_train(train_labels,train_data_scaled, params)
           p_label, p_acc, p_val = svm_predict(test_labels,test_data_scaled, model)
           
           
       else:
       
           model = svm_train(train_labels,train_data, params)
           p_label, p_acc, p_val = svm_predict(test_labels,test_data, model)

       c_matrix = confusion_matrix(test_labels,p_label)     
       print("Confusion matrix")
       print(c_matrix)
       
       self.save_to_file(test,p_label)
       
