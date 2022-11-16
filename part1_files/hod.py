#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

@author: kaivelagapudi

"""

import math 
import numpy as np


class HOD:
    
    def __init__(self):        
        pass
    
    
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
        
    """ Write to external file """
    def save_to_file(self,histogram,filename):
        
        out_file = open(filename, "w")
        for i in range(0, len(histogram)): 
                out_file.write(str(histogram[i]))
                out_file.write(" ")
    
        out_file.write("\n")
    
        out_file.close()
        
    
    """Make distogram of n bins"""
    
    def make_histo(self,data_set,bins):
        
        numBins = bins   
        hist,bins = np.histogram(data_set,bins=numBins)    
        return hist
    
    
        """ Helper method to make sure there are no Nan values before we make
        the histogram """
    
    def nan_check(self,array):
        
        for i in range(0,len(array)):
            for j in range(0,5):
                
                if math.isnan(array[i][j]):                    
                    array[i][j] = 0.0
                    
                    
        return array
    
    
    """Helper method to help read the file data into an array"""
    def get_data(self,filename):
        
        in_file = open(filename, "r")
        data = []
        for line in in_file: 
                    
                
            line = line.split()
            frame = int(line[0])
            joint = int(line[1])
            x = float(line[2])
            y = float(line[3])
            z = float(line[4])
            temp = [frame,joint,x,y,z]
            data.append(temp)
            
        return data
    
    """Get the slope of a trajectory, given a tuple of points """
    def get_slope(self,p):
        
        p1 = p[0]
        p2 = p[1]
        
        try:
            
            slope = (p2[1]-p1[1])/(p2[0]-p1[0])
            
        except:
            
            slope = 0
            
        return slope
    
    """Get the angle of the trajectory"""
    def get_angle(self,slope):
        
        angle = math.degrees(math.atan(slope))
        
        #If angle is negative , make it positive 
        
        while angle < 0:
            
            angle = angle + 360
            
        return abs(angle)
    
    
    """Helper method to create the temporal pyramid """
    def get_temporal_pyramid(self,points):
        
         points = np.array(points)
         
        
         """Level 1 """
         temp = np.array_split(points,2)
         points1 = temp[0]
         points2 = temp[1] 
         
         """Level 2 """
         temp = np.array_split(points1,2)
         points3 = temp[0]
         points4 = temp[1]
         
         """Level 3"""
         temp = np.array_split(points2,2)
         points5 = temp[0]
         points6 = temp[1]
          
         
         """Create 7 histograms"""
         
         hist_0 = self.make_histo(points,8)
         hist_1 = self.make_histo(points1,8)
         hist_2 = self.make_histo(points2,8)
         hist_3 = self.make_histo(points3,8)
         hist_4 = self.make_histo(points4,8)
         hist_5 = self.make_histo(points5,8)
         hist_6 = self.make_histo(points6,8)
         
         """ Concatenate the individual histograms bottom up int
         
         one final histogram """

         
         hist = np.concatenate((hist_0,hist_1,hist_2,hist_3,hist_4,hist_5,hist_6))
         return hist
     
     
    """ Get the displacemnet for each pair of angles and distances """
    def get_angle_distances(self,angles,distances):
        
        output = []
        
        for i in range(0,len(angles)):
            
            value = angles[i]*distances[i]
            output.append(value)
            
        return output
    
    
    
    """Eucledian distance"""
    def get_distance(self,p1,p2):
        
        dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)          
        return dist
    

    

    def run(self,mode):
         
         #Train mode     
        if(mode == 1):

            input_filenames = self.train_file_names()
            output_filename = "output/hod_d1"
            
        else: #Test mode 
            input_filenames = self.test_file_names()
            output_filename = "output/hod_d1.t"
            
            
        out_file = open(output_filename, "w")

        #Loop through all the files 
        for i in range(0,len(input_filenames)): 
            
            
             in_file_name = input_filenames[i]
             #Read file data into arry for easy access
             file_data = self.get_data(in_file_name)
             
             #Make sure there are no Nan values         
             file_data = self.nan_check(file_data)
             num_frames = int(len(file_data)/20)

                        
             angles_xy = []
             angles_yz = []
             angles_xz = []
             
             distances_xy = []
             distances_yz = []
             distances_xz = []
             
             final_hist = []
            
           
            #Loop through every line in the file
             for i in range(0,len(file_data)-20):
                                
                if not i == num_frames:
                   
                    #P_t
                    p1 = (file_data[i][2],file_data[i][3],file_data[i][4])
                    next_i = i + 20
                    #P_t+1 , trajectory of the joint in the next frame
                    p2 = (file_data[next_i][2],file_data[next_i][3],file_data[next_i][4])

                    
                    #Calculate the slope , angle and distances of the 3 2d projections
                    xy = ((p1[0],p1[1]),(p2[0],p2[1]))
                    slope_xy = self.get_slope(xy)
                    angle_xy = self.get_angle(slope_xy)
                    dist_xy = self.get_distance(xy[0],xy[1])
                    
                    yz = ((p1[1],p1[2]),(p2[1],p2[2]))
                    slope_yz = self.get_slope(yz)
                    angle_yz = self.get_angle(slope_yz)
                    dist_yz = self.get_distance(yz[0],yz[1])
                    
                    xz = ((p1[0],p1[2]),(p2[0],p2[2]))
                    slope_xz = self.get_slope(xz)
                    angle_xz = self.get_angle(slope_xz)
                    dist_xz = self.get_distance(xz[0],xz[1])
    
    
                    #Save angles and distances to an array
                     
                    angles_xy.append(angle_xy)
                    angles_yz.append(angle_yz)
                    angles_xz.append(angle_xz)
                     
                    distances_xy.append(dist_xy)
                    distances_yz.append(dist_yz)
                    distances_xz.append(dist_xz)
                    

            #Get the HOD for each 2D projection 
                    
             hist_xy = self.get_angle_distances(angles_xy,distances_xy)
             hist_yz = self.get_angle_distances(angles_yz,distances_yz)
             hist_xz = self.get_angle_distances(angles_xz,distances_xz)
               
             
            #Create the temporal pyramid 
             hist_xy = self.get_temporal_pyramid(hist_xy)
             hist_yz = self.get_temporal_pyramid(hist_yz)
             hist_xz = self.get_temporal_pyramid(hist_xz)
                    
             
            #Concatenate into 1 final histogram and normalise
             final_hist = np.concatenate((hist_xy,hist_yz,hist_xz))                   
             final_hist = [round(x /num_frames,5) for x in final_hist]
                    
              
                    
            #Write to out file        
             for i in range(0,len(final_hist)): 
                out_file.write(str(final_hist[i]))
                out_file.write(" ")
        
             out_file.write("\n")

                 
           
    
        out_file.close()
    
    


