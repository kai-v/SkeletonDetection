#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: kaivelagapudi

"""

import math 
import numpy as np


class RAD:
    
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
        
        
    """ Generate the names of train files """
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
  
    """ Generate the names of test files """
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
        
        
    """Eucledian distance between 2 points """    
    def distance(self,p1, p2):
        
        distance = 0 
        d1 = (p1[0] - p2[0]) ** 2
        d2 = (p1[1] - p2[1]) ** 2
        d3 = (p1[2] - p2[2]) ** 2
        distance = math.sqrt(d1 + d2 + d3)
        return distance 

    """Compute the star skeleton distance between hip head , feet , hands """
    def compute_distances(self,points):
        distances = []
        center = points[0]
        distances.append(self.distance(center, points[1]))
        distances.append(self.distance(center, points[2]))
        distances.append(self.distance(center, points[3]))
        distances.append(self.distance(center, points[4]))
        distances.append(self.distance(center, points[5]))
        return distances 

    """ Return angle theta , given x,y,z """
    def angle(self,a, b, c): 
        angle = ""
        a_2 = a ** 2
        b_2 = b ** 2
        c_2 = c ** 2
        
        try:          
            cos_B = (a_2 - b_2 + c_2) / (2 * c * a)  
            angle = np.degrees(np.arccos(cos_B))
        except:
            cos_B = 0
            
        angle = np.degrees(np.arccos(cos_B))
        return angle 

    """Compute the angles between adjacent body extermities """
    def compute_angles(self,distances,points):
        angles = []
        angles.append(self.angle(distances[0],self.distance(points[1], points[2]),distances[1]))
        angles.append(self.angle(distances[1],self.distance(points[2], points[4]),distances[3]))
        angles.append(self.angle(distances[3],self.distance(points[4], points[5]),distances[4]))
        angles.append(self.angle(distances[4],self.distance(points[5], points[3]),distances[2]))
        angles.append(self.angle(distances[2],self.distance(points[1], points[3]),distances[0]))
        return angles 
      
    
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
                    #print("is nan")
                    
                    array[i][j] = 0.0
                    
                    
        return array
    
    
    
    def run(self,mode):
        
        
         if(mode == 1):

            input_filenames = self.train_file_names()
            output_filename = "output/rad_d1"
            
         else:
            input_filenames = self.test_file_names()
            output_filename = "output/rad_d1.t"
         
         out_file = open(output_filename, "w")
    
    
         for i in range(0,len(input_filenames)): 
            
        
            in_file = open(input_filenames[i], "r")

            # write each file into one line 
            distances_0 = []
            distances_1 = []
            distances_2 = []
            distances_3 = []
            distances_4 = []
            angles_0 = []
            angles_1 = []
            angles_2 = []
            angles_3 = []
            angles_4 = []
    
            frames = 0 
    
            # start for loop to go through frames 
            temp_points = []
            for line in in_file: 
                line = line.split()
                joint = int(line[1])
              
                #Add hip, head, hands , feet  
                if(joint == 1 or joint == 4 or joint == 8 or joint == 12 or joint == 16): 
                    point = [float(line[2]), float(line[3]), float(line[4])]
                    temp_points.append(point)
                    
                #At the end of frame , find angles and distances
                elif joint == 20: 
                    frames = frames + 1 
                    point = [float(line[2]), float(line[3]), float(line[4])]
                    temp_points.append(point)
    
                    # pairwise distances 
                    temp_points = self.nan_check(temp_points)
                    temp_distances = self.compute_distances(temp_points)  
                    distances_0.append(temp_distances[0])
                    distances_1.append(temp_distances[1])
                    distances_2.append(temp_distances[2])
                    distances_3.append(temp_distances[3])
                    distances_4.append(temp_distances[4])
    
                    # angles of adjacent extermities
                    temp_angles = self.compute_angles(temp_distances, temp_points)
                    angles_0.append(temp_angles[0])
                    angles_1.append(temp_angles[1])
                    angles_2.append(temp_angles[2])
                    angles_3.append(temp_angles[3])
                    angles_4.append(temp_angles[4])
    
                    # clear temporary vectors 
                    temp_points = []
                    temp_distances = []
    
            # make histogram for each set of angles 
            hist_angles = []      
            
            hist_angles_0 = self.make_histo(angles_0)
            hist_angles_1 = self.make_histo(angles_1)
            hist_angles_2 = self.make_histo(angles_2)
            hist_angles_3 = self.make_histo(angles_3)
            hist_angles_4 = self.make_histo(angles_4)
            
            #Normalise
            hist_angles_0 = [round(x / frames,5) for x in hist_angles_0]
            hist_angles_1 = [round(x / frames,5) for x in hist_angles_1]
            hist_angles_2 = [round(x / frames,5) for x in hist_angles_2]
            hist_angles_3 = [round(x / frames,5) for x in hist_angles_3]
            hist_angles_4 = [round(x / frames,5) for x in hist_angles_4]
            
            hist_angles.extend(hist_angles_0)
            hist_angles.extend(hist_angles_1)
            hist_angles.extend(hist_angles_2)
            hist_angles.extend(hist_angles_3)
            hist_angles.extend(hist_angles_4)
    
            #Make histogram for distances
            hist_distances = []
           
            hist_distances_0 = self.make_histo(distances_0)
            hist_distances_1 = self.make_histo(distances_1)
            hist_distances_2 = self.make_histo(distances_2)
            hist_distances_3 = self.make_histo(distances_3)
            hist_distances_4 = self.make_histo(distances_4)
            
            #Normalise
            hist_distances_0 = [round(x / frames,5) for x in hist_distances_0]
            hist_distances_1 = [round(x / frames,5) for x in hist_distances_1]
            hist_distances_2 = [round(x / frames,5) for x in hist_distances_2]
            hist_distances_3 = [round(x / frames,5) for x in hist_distances_3]
            hist_distances_4 = [round(x / frames,5) for x in hist_distances_4]
            
            hist_distances.extend(hist_distances_0)
            hist_distances.extend(hist_distances_1)
            hist_distances.extend(hist_distances_2)
            hist_distances.extend(hist_distances_3)
            hist_distances.extend(hist_distances_4)
            
            #Concatenate both the histograms 
            total_histogram = hist_angles
            total_histogram.extend(hist_distances)

            
            for i in range(0, len(total_histogram)): 
                out_file.write(str(total_histogram[i]))
                out_file.write(" ")
    
            out_file.write("\n")
            
         out_file.close()
    

