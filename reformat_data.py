#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: kaivelagapudi

"""

import math 
import numpy as np

class reformat:
    
    def __init__(self):       
        pass


    """ Write to external file """
    def save_to_file(self,histogram,filename):
        
        out_file = open(filename, "w")
        for i in range(0, len(histogram)): 
                out_file.write(str(histogram[i]))
                out_file.write(" ")
    
        out_file.write("\n")   
        out_file.close()
        
        
    def get_train_filenames(self):
        
        names = ["output/rad_d1","output/hjpd_d1","output/hod_d1"]        
        return names
    
    
    def get_test_filenames(self):
        
        names = ["output/rad_d1.t","output/hjpd_d1.t","output/hod_d1.t"]       
        return names
    
    def get_output_filenames(self,input_file):
        
        names = input_file[7:]        
        return "formatted/" + names
        
    
    def run(self,mode):
        
        labels = [8,10,12,13,15,16]
        
        if mode == 1:
        
            input_filenames = self.get_train_filenames()
            switch_counter = 72/len(labels)
            
        else:
            
            input_filenames = self.get_test_filenames()
            switch_counter = 48/len(labels)
        
        
        for i in range(0,len(input_filenames)): 
                        
            count = 0
            index = 0
                 
            in_file = open(input_filenames[i], "r")
            output_filename = self.get_output_filenames(input_filenames[i])
            out_file = open(output_filename, "w")

            
            for line in in_file: 
                
                if count > 0 and count % switch_counter == 0:
                    index = index + 1

                label = labels[index]               
                points = line.split()

            #Write to output file
                temp_index = 0
                for i in range(0, len(points)): 
                    out_file.write(str(label))
                    out_file.write(" ")
                    out_file.write(str(temp_index))
                    out_file.write(":")
                    out_file.write(str(points[i]))
                    temp_index = temp_index + 1
                
                
                count = count + 1   
                out_file.write("\n")                
            
        out_file.close()
        