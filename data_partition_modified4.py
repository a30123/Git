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
import re

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
  
def ensure_dir(f):
#    import os
    d=os.path.abspath(f)
    if not os.path.exists(d):
        os.makedirs(d)

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
    
#########################################################################################################
#######################################   INITIALIZING        ###########################################
#########################################################################################################

#intialize "sensor variable of interest","folder to accesss", and "folder to save output to"
sensor_variables=['Heater.temp']#-------------------------------------"sensor variable of interest"
setpoint_folder='D://Heater//setpoint'
current_folder='D://Heater//setpoint'
output_folder='D://Heater//Output'
serial_number=1679

#########################################################################################################
#######################################   MAIN PROGRAM        ###########################################
#########################################################################################################

tstart = time.time()

files_in_folder = os.listdir(setpoint_folder) 

complete_dirpath_to_save_segmentlist=os.path.normpath(os.path.join(output_folder,"CSV"))    
ensure_dir(complete_dirpath_to_save_segmentlist)

serial_number_list=[]
for w in range(len(files_in_folder)):
    serial_number_list.append(extract_serial_number(files_in_folder[w]))

u=serial_number_list.index(serial_number)  
single_file_path=os.path.join(setpoint_folder, files_in_folder[u])
    
try:
    xxx=get_variable_from_csv_alternative(single_file_path, 'StepLabel')
    
    mmm=np.zeros((np.shape(xxx)[0],1))
        
    for i in range(len(mmm)):
        mmm[i]=xxx[i].split(".")[0] 

    AA=get_variable_from_csv(single_file_path, sensor_variables)
        
    modified_length=adjusted_length(single_file_path)   
        
    A=np.zeros((modified_length,1))
    m=np.zeros((modified_length,1))

    
    A=AA[-modified_length:]
    m=mmm[-modified_length:]

    A_difference = np.zeros(((modified_length-1),1))
    for i in range(0,(modified_length-1)):
        A_difference[i] = A[i+1] - A[i]
        
    uu,uuu=np.unique(m,return_counts=True)
    k=len(uuu)
        
    section=np.cumsum(uuu)
    section=np.concatenate((np.array([0]),section),axis=0)
        
    categorylist=np.zeros(modified_length+1)   
    categorylist[-1]=-1
    
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
#another test                       
    if k==1:
        intv=np.zeros((2,2))
        intv[1,0]=np.count_nonzero(categorylist==categorylist[-2])
        intv[1,1]=categorylist[-2]
        intv_n=2
    else:
        r=0
        rr=0
        intv=np.zeros((max(m),2))
        for s in range(len(categorylist)-1):
            if categorylist[s]!=categorylist[s+1]:
                intv[r,0]=np.count_nonzero(categorylist[rr:s+1]==categorylist[s])
                rr=s
                intv[r,1]=categorylist[s]
                r=r+1
        intv_n=r
        
    intv=intv[0:intv_n,:]
        
    intv[:,0]=np.cumsum(intv[:,0])
        
    intv=np.concatenate((np.zeros((1,2)),intv),axis=0)
        
    complete_path_to_save_segmentlist=os.path.normpath(os.path.join(complete_dirpath_to_save_segmentlist,files_in_folder[u]))   
    WriteListToCSV(complete_path_to_save_segmentlist,categorylist)

except ValueError:
    print('Error!!!')

print('-----------------------------------------')

print('RUN TIME: %.2f secs' % (time.time()-tstart))