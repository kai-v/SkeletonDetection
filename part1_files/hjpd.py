#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

@author: kaivelagapudi

"""

import math 
import numpy as np


class HJPD:
    
    def __init__(self):       
        pass
        
    """ Write to external file """        
    def train_file_names(self):

      filenames = []
      fileaname = ""
      a_names = [8,10,12,13,15,16]
    
      for a in range(0,len(a_names)):
        for s in range(1,7):
          for t in range(1,3):
    
            action = a_names[a]
    
            if action == 8:
    
              fileaname = "dataset/train/a0" + str(action) + "_" + "s0" + str(s) + "_" + "e0" +str(t) + "_skeleton_proj.txt"
    
            else:
    
              fileaname = "dataset/train/a" + str(action) + "_" + "s0" + str(s) + "_" + "e0" + str(t) + "_skeleton_proj.txt"
    
            filenames.append(fileaname)

      return filenames
  
    
    """ Generate the names of train files """
    def test_file_names(self):

      filenames = []
      fileaname = ""
      a_names = [8,10,12,13,15,16]
    
      for a in range(0,len(a_names)):
        for s in range(7,11):
          for t in range(1,3):
    
            action = "a" + str(a_names[a])
            subject = "s0" + str(s)
    
            if a == 0:
                
              action = "a0" + str(a_names[a])
              
            if s == 10:
                
              subject = "s" + str(s)
    
            
    
            fileaname = "dataset/test/" + action + "_" + subject + "_" + "e0" + str(t) + "_skeleton_proj.txt"
    
            filenames.append(fileaname)

      return filenames

    
    def save_to_file(self,histogram,filename):
        
        out_file = open(filename, "w")
        for i in range(0, len(histogram)): 
                out_file.write(str(histogram[i]))
                out_file.write(" ")
    
        out_file.write("\n")
    
        out_file.close()
        
    
    """Get the displacemnet between two points"""
    def get_displacement(self,p1,p2):
        
        dx = abs(p1[0] - p2[0])
        dy = abs(p1[1] - p2[1])
        dz = abs(p1[2] - p2[2])
    
        vec = [dx, dy, dz]
        return vec
    
    """Make histogram of 10 bins"""
    def make_histo(self,data_set):
        
        numBins = 10       
        hist,bins = np.histogram(data_set,bins=numBins)
        return hist

   
    """ Helper method to make sure there are no Nan values before we make
        the histogram """
    
    def nan_check(self,array):
        
        for i in range(0,len(array)):
            for j in range(0,3):
                
                val = array[i][j]
                
                if math.isnan(val):                    
                    array[i][j] = 0.0
                    
                    
        return array
                    
                    
      
    def run(self,mode):
         
        #Train mode
        if(mode == 1):
            input_filenames = self.train_file_names()
            output_filename = "output/hjpd_d1"
         
        #Test mode 
        else:
            input_filenames = self.test_file_names()
            output_filename = "output/hjpd_d1.t"
            
            
        out_file = open(output_filename, "w")
          
        #Go through eaach file
        for i in range(0,len(input_filenames)): 
            
            
            in_file_name = input_filenames[i]
            in_file = open(in_file_name, "r")
            

            distances_0 = []
            distances_1 = []
            distances_2 = []
            distances_3 = []
            distances_4 = []
            distances_5 = []
            distances_6 = []
            distances_7 = []
            distances_8 = []
            distances_9 = []
            distances_10 = []
            distances_11 = []
            distances_12 = []
            distances_13 = []
            distances_14 = []
            distances_15 = []
            distances_16 = []
            distances_17 = []
            distances_18 = []
       
            temp_points = []
            temp_distances = []
            frames = 0
            
            #Read each line in a file
            for line in in_file: 
                    
                
                line = line.split()
                joint = int(line[1])
                x = float(line[2])
                y = float(line[3])
                z = float(line[4])
             
                #If joint number is between 2 and 19 
                #save the center joint (hip) and append
                if joint >= 1 and joint < 20:
                   
                    point = [x,y,z]
   
                    
                    if(joint == 1):
                        center_point = point
                       
                        
                    else:
                        temp_points.append(point)
                 
                #At the end of the frame , joint 20 , append all the displacemets
                elif joint == 20: 
                    
                    frames = frames + 1 
                    point = [x,y,z]
                    temp_points.append(point)
                 
                    #Check for Nan values
                    temp_points = self.nan_check(temp_points)

          
                    #Find the displacemnet for each joint and the center - hip
                    for i in range(0,len(temp_points)):
                        temp_distance = self.get_displacement(temp_points[i],center_point)
                        temp_distances.append(temp_distance)
                        

                        
                    #Check to make sure no nan values    
                    temp_distances = self.nan_check(temp_distances)
                        

                    distances_0.append(temp_distances[0])
                    distances_1.append(temp_distances[1])
                    distances_2.append(temp_distances[2])
                    distances_3.append(temp_distances[3])
                    distances_4.append(temp_distances[4])
                    distances_5.append(temp_distances[5])
                    distances_6.append(temp_distances[6])
                    distances_7.append(temp_distances[7])
                    distances_8.append(temp_distances[8])
                    distances_9.append(temp_distances[9])
                    distances_10.append(temp_distances[10])
                    distances_11.append(temp_distances[11])
                    distances_12.append(temp_distances[12])
                    distances_13.append(temp_distances[13])
                    distances_14.append(temp_distances[14])
                    distances_15.append(temp_distances[15])
                    distances_16.append(temp_distances[16])
                    distances_17.append(temp_distances[17])
                    distances_18.append(temp_distances[18])
                   

                    # clear temporary vectors 
                    temp_points = []
                    temp_distances = []
    
    
            #Create histograms
            hist_distances = []

            hist_dist_0 = self.make_histo(distances_0)
            hist_dist_1 = self.make_histo(distances_1)
            hist_dist_2 = self.make_histo(distances_2)
            hist_dist_3 = self.make_histo(distances_3)
            hist_dist_4 = self.make_histo(distances_4)
            hist_dist_5 = self.make_histo(distances_5)
            hist_dist_6 = self.make_histo(distances_6)
            hist_dist_7 = self.make_histo(distances_7)
            hist_dist_8 = self.make_histo(distances_8)
            hist_dist_9 = self.make_histo(distances_9)
            hist_dist_10 = self.make_histo(distances_10) 
            hist_dist_11 = self.make_histo(distances_11)
            hist_dist_12 = self.make_histo(distances_12)
            hist_dist_13 = self.make_histo(distances_13)
            hist_dist_14 = self.make_histo(distances_14)
            hist_dist_15 = self.make_histo(distances_15)
            hist_dist_16 = self.make_histo(distances_16)
            hist_dist_17 = self.make_histo(distances_17)
            hist_dist_18 = self.make_histo(distances_18)
            
            #Normalise
            hist_dist_0 = [round(x / frames,5) for x in hist_dist_0]
            hist_dist_1 = [round(x / frames,5) for x in hist_dist_1]
            hist_dist_2 = [round(x / frames,5) for x in hist_dist_2]
            hist_dist_3 = [round(x / frames,5) for x in hist_dist_3]
            hist_dist_4 = [round(x / frames,5) for x in hist_dist_4]
            hist_dist_5 = [round(x / frames,5) for x in hist_dist_5]
            hist_dist_6 = [round(x / frames,5) for x in hist_dist_6]
            hist_dist_7 = [round(x / frames,5) for x in hist_dist_7]
            hist_dist_8 = [round(x / frames,5) for x in hist_dist_8]
            hist_dist_9 = [round(x / frames,5) for x in hist_dist_9]
            hist_dist_10 = [round(x / frames,5) for x in hist_dist_10]
            hist_dist_11 = [round(x / frames,5) for x in hist_dist_11]
            hist_dist_12 = [round(x / frames,5) for x in hist_dist_12]
            hist_dist_13 = [round(x / frames,5) for x in hist_dist_13]
            hist_dist_14 = [round(x / frames,5) for x in hist_dist_14]
            hist_dist_15 = [round(x / frames,5) for x in hist_dist_15]
            hist_dist_16 = [round(x / frames,5) for x in hist_dist_16]
            hist_dist_17 = [round(x / frames,5) for x in hist_dist_17]
            hist_dist_18 = [round(x / frames,5) for x in hist_dist_18]
           
            #Concatenete all the histograms into one         
            hist_distances.extend(hist_dist_0)
            hist_distances.extend(hist_dist_1)
            hist_distances.extend(hist_dist_2)
            hist_distances.extend(hist_dist_3)
            hist_distances.extend(hist_dist_4)
            hist_distances.extend(hist_dist_5)
            hist_distances.extend(hist_dist_6)
            hist_distances.extend(hist_dist_7)
            hist_distances.extend(hist_dist_8)
            hist_distances.extend(hist_dist_9)
            hist_distances.extend(hist_dist_10)
            hist_distances.extend(hist_dist_11)
            hist_distances.extend(hist_dist_12)
            hist_distances.extend(hist_dist_13)
            hist_distances.extend(hist_dist_14)
            hist_distances.extend(hist_dist_15)
            hist_distances.extend(hist_dist_16)
            hist_distances.extend(hist_dist_17)
            hist_distances.extend(hist_dist_18)

              
            #Write to file
    
            for i in range(0,len(hist_distances)): 
                out_file.write(str(hist_distances[i]))
                out_file.write(" ")
    
            out_file.write("\n")
            
        out_file.close()
    
    
    

