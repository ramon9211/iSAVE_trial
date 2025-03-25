#####imports######
import numpy as np
import scipy as sp 
import pandas as pd 
from matplotlib import pyplot as plt 
import os 
import argparse
import datetime
import seaborn as sns
import glob 


def plot_stats_strip_box(data, title, resultPath, trial, patient, width=10, height=7):
    fig, axs = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
    fig.set_dpi(100)
    sns.set(font_scale=1.75)
    plt.title(title, fontsize=22)
    fig.set_figwidth(width)
    fig.set_figheight(height)
    plt.ylabel('SPO2/%')
    #axs.set_xlabel('Session')
    axs=sns.boxplot(data=data, orient='v')
    axs=sns.stripplot(data=data, orient='v')
    #axs.set_ylim([50, 105])
    plt.savefig(os.path.join(resultPath, 'SPO2_distribution2_'+trial+'_'+patient+'.png'))
    #plt.show()

def plot_time_series(data, title, resultPath, trial, patient, fs=0.5, width=20, height=10):
    fig, axs = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)
    fig.set_dpi(150)
    fig.suptitle(title)
    fig.set_figwidth(width)
    fig.set_figheight(height)

    timeList = []
    for i in range(len(data)):
        timeList.append((1/(fs*60))*np.arange(len(data[i])))

    for i in range(len(data)):
        axs[i].plot(timeList[i], data[i], label='Session {}'.format(i+1))
        axs[i].set_ylabel('Heart rate [1/min]')
        axs[i].legend(loc='lower left')
            
    axs[-1].set_xlabel('time/min')
    
    plt.savefig(os.path.join(resultPath, 'HR_time_series_'+trial+'_'+patient+'.png'))
    #plt.clf()
    #plt.show()

if __name__ == "__main__":

    # parse arguments from command line
    parser = argparse.ArgumentParser()    
    parser.add_argument('--data_path1', type=str, required=True)
    parser.add_argument('--result_path', type=str, required=True)
    parser.add_argument('--fs', type=int, required=False, default=100)
    parser.add_argument('--trial_number', type=int, required=False, default=0)
    parser.add_argument('--patient_ID', type=str, default='0L')

    config = parser.parse_args()

    # set up identifiers to access data
    patientIDs = ['Patient_1L', 'Patient_1R', 
                  'Patient_2L', 'Patient_2R',
                  'Patient_3L', 'Patient_3R',
                  'Patient_4L', 'Patient_4R',
                  'Patient_5L', 'Patient_5R',
                  'Patient_6L', 'Patient_6R',
                  'Patient_7L', 'Patient_7R',
                  'Patient_8L', 'Patient_8R',]
    
    TrialIDs = ['Trial1', 'Trial2', 'Trial3', 'Trial4', 'Trial5', 'Trial6', 'Trial7', 'Trial8']

    monitorType = ['pmon', 'iSAVE', 'vent']

    dataType = ['graph', 'stats']

    sessionIDs = ['Session1', 'Session2', 'Session3']

    graphParameterIDs = ['P', 'V', 'F', 'CO']
    statsParameterIDs = ['SPO', 'HR']

    pathList = []
    #paths = os.walk(config.data_path1)
    for root, dirs, files in os.walk(config.data_path1, topdown=False):
        for name in files:
            if '.csv' in name and 'lock' not in name:
                path = os.path.join(root, name)
                print(path)
                pathList.append(path)

    subPathList = []
    for TrialID in TrialIDs:
        for patientID in patientIDs:
            tempList = []
            for path in pathList:
                if TrialID in path and patientID in path and 'stats' in path and 'pmon' in path: 
                    print(TrialID, patientID)
                    #print(path)
                    tempList.append(path)
            if len(tempList) > 0:
                print(tempList)
                subPathList.append(tempList)
                      

    #print(subPathList)
    print(len(subPathList))
    for i in range(len(subPathList)):
        paths = subPathList[i]
        paths.sort()
        dfList = []
        for path in paths:
            print('Current path is {}'.format(path))
            IDs = path.split('/')
            print(IDs)
            Trial = IDs[4]
            Patient = IDs[5]
            df = pd.read_csv(path)
            df.sort_values(by='TS', inplace=True)
            dfList.append(pd.read_csv(path))
            print(df)
        
        listSPO = []
        for df in dfList:
            SPO = df['SPO']
            listSPO.append(SPO)
        
        SPO2 = {
            'Session 1': listSPO[0],
            'Session 2': listSPO[1],
            'Session 3': listSPO[2]
        }
        dfSPO2 = pd.DataFrame(SPO2)
        title = Trial + ' ' + Patient
        plot_stats_strip_box(dfSPO2, title=title, resultPath=config.result_path, trial=Trial, patient=Patient)
        plot_time_series(listSPO, title=title, resultPath=config.result_path, trial=Trial, patient=Patient)
    i=0
    if i == 1:
        subPathList = []
        for path in pathList:
            if 'Trial1' in path and 'Patient_1L' in path and 'stats' in path and 'pmon' in path:
                subPathList.append(path)
                print(path)
        
        subPathList.sort() 
        print(subPathList)
        
        dfList = []
        for path in subPathList:
            dfList.append(pd.read_csv(path))
        
        #print(dfList[0]['SPO'])

        listSPO = []
        for df in dfList:
            SPO = df['SPO']
            print(SPO)
            listSPO.append(SPO)
        



    #df1 = pd.read_csv(config.data_path1)


    # print(df1)
    # print(df1['SPO'])
    # SPO1 =np.asarray(df.iloc[:,0])


        plot_stats_strip_box(listSPO)