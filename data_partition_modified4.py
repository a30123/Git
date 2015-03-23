# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 10:00:54 2015

@author: A30330
"""
#########################################################################################################
###      #####  #####        #####       ###############    #   ###  ###       ###       ################
###  #########  ########  ########  ####################  #  #  ###  ###  ###  ###  ###  ################
###  #########  ########  ########  ####################  ####  ###  ###  ###  ###  ###  ################
###      #####  ########  ########       ###############  ####  ###  ###       ###       ################
#########################################################################################################

#########################################################################################################
#######################################   IMPORT LIBRARIES    ###########################################
#########################################################################################################
import os
import time
import csv
import numpy as np
<<<<<<< HEAD
import re
=======
#import math
import re
#import pandas as pd
import matplotlib.pyplot as plt

>>>>>>> parent of 923b3ca... add serial number input
#########################################################################################################
#######################################   FUNCTIONS           ###########################################
#########################################################################################################

def get_variable_from_csv(csvpathfilename, listofvariablename):
    reader = csv.reader(open(csvpathfilename, 'r'), delimiter=',')
    tempArr = np.array(list(reader))
    tags = tempArr[0,:]
        
    variablearrays=np.zeros((np.shape(tempArr)[0] - 1, np.shape(np.array(listofvariablename))[0]))
    for j in range(0, np.shape(np.array(listofvariablename))[0]):
        for i in range(0,np.shape(tempArr)[1]):
            if tags[i] == np.array(listofvariablename)[j]:
                variablearrays[0:, j] = tempArr[1:, i].astype('float')
        
    return variablearrays    

def get_variable_from_csv_alternative(csvpathfilename, listofvariablename):       
    notfirst=1
    thelist=[]
    
    with open(csvpathfilename,'rU') as csvfile:
        contents=csv.reader(csvfile)
        for row in contents:
            if notfirst==1:
               whichcolumn=row.index(listofvariablename)
               notfirst+=1
            else:
               thelist.append(row[(whichcolumn)])
        
    return np.array(thelist)
    
def WriteListToCSV(filename_path,listname):
#    import csv
	
    runnumberfile=open(filename_path,'w',newline='')
    wr=csv.writer(runnumberfile,quoting=csv.QUOTE_ALL)
    for item in listname:
        wr.writerow([item])
		
    runnumberfile.close()

#reference:    http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary     
def ensure_dir(f):
#    import os
    d=os.path.abspath(f)
    if not os.path.exists(d):
        os.makedirs(d)

<<<<<<< HEAD
def extract_serial_number(filename):
#    import re
    extract_regular_expression=re.search('(_\d+-)',filename)
    serial_number_string=extract_regular_expression.group(0)
    serial_number_string=serial_number_string.replace('-','')
    serial_number_string=serial_number_string.replace('_','') 
    value_of_number=int(serial_number_string)
    return value_of_number

def adjusted_length(step_steplabel_file_path):
#    import numpy as np
    
    mm=get_variable_from_csv(step_steplabel_file_path, ['Step'])
    
    nonzero_step=np.zeros((1,1))
    if min(mm)==0:
        zero_step=np.count_nonzero(mm==0)
        if zero_step==len(mm):
            zero_step=0
    else:
        nonzero_step=np.count_nonzero(mm==min(mm))
        for i in range(len(mm)):
            if mm[i]==min(mm):
                zero_step=(i+1)-nonzero_step
                
    return((len(mm)-int(zero_step)))
    
=======
>>>>>>> parent of 923b3ca... add serial number input
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################

sensor_variables=['Heater.temp']#-------------------------------------"sensor variable of interest"
setpoint_folder='D://Heater//setpoint'
current_folder='D://Heater//setpoint'
output_folder='D://Heater//Output'

#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################
tstart = time.time()

files_in_folder = os.listdir(setpoint_folder) 

complete_dirpath_to_save_segmentlist=os.path.normpath(os.path.join(output_folder,"CSV"))    
ensure_dir(complete_dirpath_to_save_segmentlist)

doesnotwork=[]

<<<<<<< HEAD
serial_number_list=[]
for w in range(len(files_in_folder)):
    serial_number_list.append(extract_serial_number(files_in_folder[w]))
    
=======
for u in range(len(files_in_folder)):
    print(u)
    single_file_path=os.path.join(setpoint_folder, files_in_folder[u])
>>>>>>> parent of 923b3ca... add serial number input

u=serial_number_list.index(serial_number)    

<<<<<<< HEAD
single_file_path=os.path.join(setpoint_folder, files_in_folder[u])

mm=get_variable_from_csv(single_file_path, ['Step'])
=======
    justnumbertemp=runnumberbylogfile.group(0)
    mm=get_variable_from_csv(single_file_path, ['Step'])
>>>>>>> parent of 923b3ca... add serial number input
 
ultimate_length=np.shape(mm)[0]
    
AA=get_variable_from_csv(single_file_path, sensor_variables)
    
try:
    xxx=get_variable_from_csv_alternative(single_file_path, 'StepLabel')
    mmm=np.zeros((np.shape(xxx)[0],1))
        
    for i in range(len(mmm)):
        mmm[i]=xxx[i].split(".")[0] 

    AA=get_variable_from_csv(single_file_path, sensor_variables)
      
    modified_length=adjusted_length(single_file_path)   

<<<<<<< HEAD
    A=AA[-modified_length:]
    m=mmm[-modified_length:]

    A_difference = np.zeros(((modified_length-1),1))
    for i in range(0,(modified_length-1)):
        A_difference[i] = A[i+1] - A[i]
        
    uu,uuu=np.unique(m,return_counts=True)
    k=len(uuu)
=======
    
        A=AA[int(zero_step):]
        m=mm[int(zero_step):]

        A_difference = np.zeros(((modified_length-1),1))
        for i in range(0,(modified_length-1)):
            A_difference[i] = A[i+1] - A[i]
        # preprocessing for partition
#        n=int(max(m))
#        for k in range(0, (modified_length-1)):
#            for i in range(1, n):
#                if math.fabs(A[k+1] - A[k]) <= 0.01:
#                    m[k+1] = m[k]
                
        uu,uuu=np.unique(m,return_counts=True)
        uuu[-1]=uuu[-1]
        k=len(uuu)
        nnn=uuu
        # partition completed
>>>>>>> parent of 923b3ca... add serial number input
        
    section=np.cumsum(uuu)
    section=np.concatenate((np.array([0]),section),axis=0)
        
    categorylist=np.zeros(modified_length)   
    
<<<<<<< HEAD
    for j in range(0, k):
        if k==1:
            categorylist[0:section[1]]=4*np.ones((section[1]))
        elif k>1 and section[j+1]-section[j]>3:
            if max(A_difference[section[j]+1:section[j+1]-1])*min(A_difference[section[j]+1:section[j+1]-1]) < 0:#fluctuation
                categorylist[section[j]:(section[j+1])]=1*np.ones((section[j+1]-section[j]))
            elif max(A_difference[section[j]+1:section[j+1]-1]) < -0.1:# decrease fast
                categorylist[section[j]:(section[j+1])]=2*np.ones((section[j+1]-section[j]))
            elif min(A_difference[section[j]+1:section[j+1]-1]) > 0.1:# increase fast
                categorylist[section[j]:(section[j+1])]=3*np.ones((section[j+1]-section[j]))
            elif max(A_difference[section[j]+1:section[j+1]-1]) < 0.01 and min(A_difference[section[j]+1:section[j+1]-1]) >= -0.01: # stable
                categorylist[section[j]:(section[j+1])]=4*np.ones((section[j+1]-section[j]))
            elif max(A_difference[section[j]+1:section[j+1]-1]) <= 0.1 and max(A_difference[section[j]+1:section[j+1]-1]) >= 0.01 and min(A_difference[section[j]+1:section[j+1]-1]) >= 0: # increase slowly
                categorylist[section[j]:(section[j+1])]=5*np.ones((section[j+1]-section[j]))
            elif min(A_difference[section[j]+1:section[j+1]-1]) >= -0.1 and max(A_difference[section[j]+1:section[j+1]-1]) <= -0.01 and min(A_difference[section[j]+1:section[j+1]-1]) <= 0: # decrease slowly
                categorylist[section[j]:(section[j+1])]=6*np.ones((section[j+1]-section[j]))            
            else: 
                categorylist[section[j]:(section[j+1])]=6*np.ones((section[j+1]-section[j]))
        
    complete_path_to_save_segmentlist=os.path.normpath(os.path.join(complete_dirpath_to_save_segmentlist,files_in_folder[u]))
        
    WriteListToCSV(complete_path_to_save_segmentlist,categorylist)
=======
        for j in range(0, k):
            if k==1:
                categorylist[0:section[1]]=1*np.ones((section[1]))
                plt.axvspan(0, section[1]-1, facecolor='c', alpha=0.5)
            elif k>1 and section[j+1]-section[j]>3:
                if max(A_difference[section[j]+1:section[j+1]-1])*min(A_difference[section[j]+1:section[j+1]-1]) < 0:#fluctuation
                    categorylist[section[j]:(section[j+1])]=1*np.ones((section[j+1]-section[j]))
                    plt.axvspan(section[j], section[j+1], facecolor='g', alpha=0.8)
                elif max(A_difference[section[j]+1:int(section[j+1])-1]) < -0.1:# decrease fast:red
                    categorylist[section[j]:(section[j+1])]=2*np.ones((section[j+1]-section[j]))
                    plt.axvspan(section[j], section[j+1], facecolor='r', alpha=1)
                elif min(A_difference[section[j]+1:section[j+1]-1]) > 0.1:# increase fast:yellow
                    categorylist[section[j]:(section[j+1])]=3*np.ones((section[j+1]-section[j]))
                    plt.axvspan(section[j], section[j+1], facecolor='y', alpha=1)
                elif max(A_difference[section[j]+1:section[j+1]-1]) < 0.01 and min(A_difference[section[j]+1:section[j+1]-1]) >= -0.01: # stable:cyan
                    categorylist[section[j]:(section[j+1])]=4*np.ones((section[j+1]-section[j]))
                    plt.axvspan(section[j], section[j+1], facecolor='c', alpha=0.5)
                elif max(A_difference[section[j]+1:section[j+1]-1]) <= 0.1 and max(A_difference[section[j]+1:section[j+1]-1]) >= 0.01 and min(A_difference[section[j]+1:section[j+1]-1]) >= 0: # increase slowly:magenta
                    categorylist[section[j]:(section[j+1])]=5*np.ones((section[j+1]-section[j]))
                    plt.axvspan(section[j], section[j+1], facecolor='m', alpha=0.5)
                elif min(A_difference[section[j]+1:section[j+1]-1]) >= -0.1 and max(A_difference[section[j]+1:section[j+1]-1]) <= -0.01 and min(A_difference[section[j]+1:section[j+1]-1]) <= 0: # decrease slowly:gray
                    categorylist[section[j]:(section[j+1])]=6*np.ones((section[j+1]-section[j]))
                    plt.axvspan(section[j], section[j+1], facecolor='k', alpha=0.2)                
                else: 
                    categorylist[section[j]:(section[j+1])]=6*np.ones((section[j+1]-section[j]))
                    plt.axvspan(section[j], section[j+1], facecolor='w', alpha=1)

                    
#                    for i in range(section[j], section[j+1]):
#                        if math.fabs(A_difference[i])<=0.01:
#                            categorydifferencelist[i]=4
#                        elif A_difference[i]>0.1:
#                            categorydifferencelist[i]=3
#                        elif A_difference[i]<=0.1 and A_difference[i]>0.01:
#                            categorydifferencelist[i]=5
#                        elif A_difference[i]<-0.1:
#                            categorydifferencelist[i]=2
#                        elif A_difference[i]<=-0.01 and A_difference>=-0.1:
#                            categorydifferencelist[i]=6
   
        categorylist=np.concatenate((np.zeros(zero_step),categorylist),axis=0)
    

    
        complete_path_to_save_segmentlist=os.path.normpath(os.path.join(complete_dirpath_to_save_segmentlist,files_in_folder[u]))
        figure_filename2=files_in_folder[u].replace('.csv','.png')
        complete_path_to_save_figure=os.path.normpath(os.path.join(complete_dirpath_to_save_figure,figure_filename2))
        
        WriteListToCSV(complete_path_to_save_segmentlist,categorylist)
>>>>>>> parent of 923b3ca... add serial number input

except ValueError:
    print('Error') 

print('RUN TIME: %.2f secs' % (time.time()-tstart))