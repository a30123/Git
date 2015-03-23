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

#reference:    http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary     
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

doesnotwork=[]

serial_number_list=[]
for w in range(len(files_in_folder)):
    serial_number_list.append(extract_serial_number(files_in_folder[w]))
    
for ww in range(1):
    u=serial_number_list.index(serial_number)    

    single_file_path=os.path.join(setpoint_folder, files_in_folder[u])

    mm=get_variable_from_csv(single_file_path, ['Step'])
 
    ultimate_length=np.shape(mm)[0]
    
    AA=get_variable_from_csv(single_file_path, sensor_variables)
    
    try:
        xxx=get_variable_from_csv_alternative(single_file_path, 'StepLabel')
        mmm=np.zeros((np.shape(xxx)[0],1))
        
        for i in range(len(mmm)):
            mmm[i]=xxx[i].split(".")[0] 

        AA=get_variable_from_csv(single_file_path, sensor_variables)
      
#        if min(mm)==0:
#            zero_step=np.count_nonzero(mm==0)
#        elif min(mm)!=0:
#            nonzero_step=np.count_nonzero(mm==min(mm))
#            for i in range(len(mm)):
#                if mm[i]==min(mm):
#                    zero_step=(i+1)-nonzero_step
        
        modified_length=adjusted_length(single_file_path)   
#        modified_length=ultimate_length-int(zero_step)
        
        A=np.zeros((modified_length,1))
        m=np.zeros((modified_length,1))

    
        A=AA[-modified_length:]
        m=mmm[-modified_length:]
#        A=AA[int(zero_step):]
#        m=mmm[int(zero_step):]

        A_difference = np.zeros(((modified_length-1),1))
        for i in range(0,(modified_length-1)):
            A_difference[i] = A[i+1] - A[i]
        
        uu,uuu=np.unique(m,return_counts=True)
        k=len(uuu)
        
        section=np.cumsum(uuu)
        section=np.concatenate((np.array([0]),section),axis=0)
        
        categorylist=np.zeros(modified_length)   
    
        for j in range(0, k):
            if k==1:
                categorylist[0:section[1]]=4*np.ones((section[1]))
            elif k>1 and section[j+1]-section[j]>3:
                if max(A_difference[section[j]+1:section[j+1]-1])*min(A_difference[section[j]+1:section[j+1]-1]) < 0:#fluctuation
                    categorylist[section[j]:(section[j+1])]=1*np.ones((section[j+1]-section[j]))
#                    plt.axvspan(section[j], section[j+1], facecolor='g', alpha=0.8)
                elif max(A_difference[section[j]+1:section[j+1]-1]) < -0.1:# decrease fast:red
                    categorylist[section[j]:(section[j+1])]=2*np.ones((section[j+1]-section[j]))
#                    plt.axvspan(section[j], section[j+1], facecolor='r', alpha=1)
                elif min(A_difference[section[j]+1:section[j+1]-1]) > 0.1:# increase fast:yellow
                    categorylist[section[j]:(section[j+1])]=3*np.ones((section[j+1]-section[j]))
#                    plt.axvspan(section[j], section[j+1], facecolor='y', alpha=1)
                elif max(A_difference[section[j]+1:section[j+1]-1]) < 0.01 and min(A_difference[section[j]+1:section[j+1]-1]) >= -0.01: # stable:cyan
                    categorylist[section[j]:(section[j+1])]=4*np.ones((section[j+1]-section[j]))
#                    plt.axvspan(section[j], section[j+1], facecolor='c', alpha=0.5)
                elif max(A_difference[section[j]+1:section[j+1]-1]) <= 0.1 and max(A_difference[section[j]+1:section[j+1]-1]) >= 0.01 and min(A_difference[section[j]+1:section[j+1]-1]) >= 0: # increase slowly:magenta
                    categorylist[section[j]:(section[j+1])]=5*np.ones((section[j+1]-section[j]))
#                    plt.axvspan(section[j], section[j+1], facecolor='m', alpha=0.5)
                elif min(A_difference[section[j]+1:section[j+1]-1]) >= -0.1 and max(A_difference[section[j]+1:section[j+1]-1]) <= -0.01 and min(A_difference[section[j]+1:section[j+1]-1]) <= 0: # decrease slowly:gray
                    categorylist[section[j]:(section[j+1])]=6*np.ones((section[j+1]-section[j]))
#                    plt.axvspan(section[j], section[j+1], facecolor='k', alpha=0.2)                
                else: 
                    categorylist[section[j]:(section[j+1])]=6*np.ones((section[j+1]-section[j]))
#                    plt.axvspan(section[j], section[j+1], facecolor='w', alpha=1)
                
        
        intv=np.zeros((max(m),2))
        r=0
        rr=0
        if k==1:
            intv[1,0]=np.count_nonzero(categorylist==categorylist[-1])
            intv[1,1]=categorylist[-1]
        else:
            for s in range(len(categorylist)-1):
                if categorylist[s]!=categorylist[s+1]:
                    intv[r,0]=np.count_nonzero(categorylist[rr:s]==categorylist[s])
                    rr=s
                    intv[r,1]=categorylist[s]
                    r=r+1
    
        intv_n=len(intv)-np.count_nonzero(intv[r,0]==0)
        intv=intv[0:intv_n,:]
        
        intv[:,0]=np.cumsum(intv[:,0])
        
        intv=np.concatenate((np.zeros((1,2)),intv),axis=0)
        
#        for v in range(len(intv)-1):
#            if intv[v+1,1]==1:
#                plt.axvspan(intv[v,0], intv[v+1,0]-1, facecolor='g', alpha=0.8)
#            if intv[v+1,1]==2:
#                plt.axvspan(intv[v,0], intv[v+1,0]-1, facecolor='r', alpha=1)
#            if intv[v+1,1]==3:
#                plt.axvspan(intv[v,0], intv[v+1,0]-1, facecolor='y', alpha=1)
#            if intv[v+1,1]==4:
#                plt.axvspan(intv[v,0], intv[v+1,0]-1, facecolor='c', alpha=0.5)
#            if intv[v+1,1]==5:
#                plt.axvspan(intv[v,0], intv[v+1,0]-1, facecolor='m', alpha=0.5)
#            if intv[v+1,1]==6:
#                plt.axvspan(intv[v,0], intv[v+1,0]-1, facecolor='k', alpha=0.2)
        
        complete_path_to_save_segmentlist=os.path.normpath(os.path.join(complete_dirpath_to_save_segmentlist,files_in_folder[u]))
#        figure_filename=files_in_folder[u].replace('.csv','.png')
#        complete_path_to_save_figure=os.path.normpath(os.path.join(complete_dirpath_to_save_figure,figure_filename))
        
        WriteListToCSV(complete_path_to_save_segmentlist,categorylist)

#        plt.xlim(section[0], section[k]-1)
#        plt.grid()
#        plt.xlabel("Time(s)",fontsize=16)
#        plt.ylabel("Setpoint",fontsize=16) 
#        for tick in plt.gca().xaxis.get_major_ticks():
#            tick.label1.set_fontsize(12) 
#        for tick in plt.gca().yaxis.get_major_ticks():
#            tick.label1.set_fontsize(12) 
#        plt.savefig(complete_path_to_save_figure)
#        plt.clf()
    
    
    except ValueError:
#        print('Reading CSV file:',justnumbertemp)
#        print('run',u)
        print('No valid StepLabel in this run!!!')
        doesnotwork.append(u)
#    print('Reading CSV file:',justnumbertemp) 
    
    print('-----------------------------------------')

print('RUN TIME: %.2f secs' % (time.time()-tstart))