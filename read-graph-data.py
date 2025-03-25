#author rajib mondal
#reading graph data from iSAVE and ventilator
#graph data is highly sampled P,V, or F data
#each graph data file is a csv file containing two columns
#column 1: measurement (P, or V, or F)
#column 2: timestamp in unix format

#####imports######
import numpy as np
import scipy as sp 
import pandas as pd 
from matplotlib import pyplot as plt 
import os 
import argparse
import datetime
import seaborn as sns


##############################################################################
# This was mainly used to read the graph data and extract pressure, volume, and flow volumes at specific time points
############################################################################## 


# plot data
def plot_time_series_spotty_regions(data, time, savePath, fileName, title, xIndices, width=20, height=10, timeRange=20):
    for i in range(xIndices.shape[1]):
        fig, axs = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
        fig.set_dpi(150)
        fig.suptitle(title+' {}/{}'.format(i, xIndices.shape[1]), fontsize=14)
        fig.set_figwidth(width)
        fig.set_figheight(height)

        axs.plot(time, data, label='Graph data')

        axs.plot([time[xIndices[0,i]], time[xIndices[0,i]]], [-500,750], label='Timestamp jump')

        axs.set_ylabel('Amplitude')
        axs.set_xlabel('time/s')

        xlim = [time[xIndices[0,i]]-timeRange/2, time[xIndices[0,i]]+timeRange/2]
        axs.set_xlim(xlim)

        #minValue= np.min(data[xIndices[0,i]])
        #maxValue= np.max(data[xIndices[0,i]])
        #peakToPeak = maxValue-minValue
        #axs.set_ylim([minValue-peakToPeak/2, maxValue+peakToPeak/2])

        if not os.path.exists(savePath):
            os.makedirs(savePath)
        
        plt.legend()
        plt.savefig(os.path.join(savePath, fileName+ str(xlim[0]) + '_' + str(xlim[1]) +'.png'))
        plt.savefig(os.path.join(savePath, fileName+ str(xlim[0]) + '_' + str(xlim[1]) +'.pdf'))

        plt.close(fig)
        plt.close('all')
        print('Figure {}/{} saved.'.format(i, xIndices.shape[1]))
    print('######### Plots for all spotty regions in current file generated ##############')
        
        # plt.show()

def plot_whole_time_series(data, time, title='Pressure', width=20, height=10):
    fig, axs = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=False)
    fig.set_dpi(150)
    fig.suptitle(title, fontsize=14)
    fig.set_figwidth(width)
    fig.set_figheight(height)

    axs.plot(time/60, data, label='Graph data')
    axs.set_xlabel('time/min')
    axs.set_ylabel('mmHg')

    #plt.legend()
    plt.show()


def plot_stats_strip_box(data, label_x, label_y):
    sns.boxplot(x='size', y='tip', data=data)
    sns.stripplot(x='size', y='tip', data=data)
    plt.show()

if __name__ == "__main__":

    # parse arguments from command line
    parser = argparse.ArgumentParser()    
    parser.add_argument('--data_path', type=str, required=True)
    parser.add_argument('--save_folder_path', type=str, required=False, default='./')
    parser.add_argument('--fs', type=int, required=False, default=100)
    parser.add_argument('--trial_number', type=int, required=False, default=0)
    parser.add_argument('--patient_ID', type=str, default='0L')

    spotty=False
    config = parser.parse_args() 
    fs = config.fs

    # paths = [f for f in os.listdir(config.data_path) if os.path.isfile(os.path.join(config.data_path, f))]
    fs=100
    df = pd.read_csv(config.data_path)
    print(df)
    P=np.asarray(df.iloc[:,0])
    print(P)
    N=P.size

    dateTime0 = datetime.datetime.fromtimestamp(df.loc[0,'TS']/1000)
    dateTime1 = datetime.datetime.fromtimestamp(df.loc[1,'TS']/1000)
    dateTime2 = datetime.datetime.fromtimestamp(df.loc[2,'TS']/1000)
    dateTime3 = datetime.datetime.fromtimestamp(df.loc[N-1,'TS']/1000)
    diff=(dateTime1-dateTime0).total_seconds()
    fs = 1/diff
    print('fs is {}'.format(fs))

    # print(dateTime1)
    # print(dateTime2)
    # print(dateTime3)
    # print(dateTime2-dateTime1)
    # #print(dateTime3-dateTime2)
    # print(dateTime3)

    time = (df.loc[:,'TS']-df.loc[0,'TS'])/1000

    #time = np.arange(P.size)*diff

    #fs=1/diff
    
    plot_whole_time_series(P, time)

    ###########################################################
    #### Code added by Leen ##################################

    PEEPextraction = find_PEEPs() 



    ###########################################################
    if spotty:
        rootList = [] # list of root folders
        fileNameList = [] # list of files inside current root
        dirList = [] # list of directories inside current root

        for (root,dirs,files) in os.walk(config.data_path, topdown=True):
            rootList.append(root)
            fileNameList.append(files)
            dirList.append(dirs)


        filePathList = []
        for i in range(len(rootList)):
            for j in range(len(fileNameList[i])):
                filePath = os.path.join(rootList[i], fileNameList[i][j])
                filePathList.append(filePath)
        # print(filePathList)        


        #filter paths of interest
        filteredFilePaths = []
        for i in range(len(filePathList)):
            if '_graph' in filePathList[i]:
                filteredFilePaths.append(filePathList[i])

        print(len(filteredFilePaths))

        indexList=[]
        for i in range(len(filteredFilePaths)):
            if 'CO' in filteredFilePaths[i] or 'IMP' in filteredFilePaths[i]: 
                indexList.append(i)

        for index in sorted(indexList, reverse=True):
            del filteredFilePaths[index]


        print(len(filteredFilePaths))
        print(filteredFilePaths[0])

        #files = ['grp_V_vent401_T5.csv']


        for filePath in filteredFilePaths:

            filePathStringList = filePath.split('/')
            print(filePathStringList)
            Session = filePathStringList[6]
            Patient = filePathStringList[5]
            Trial = filePathStringList[4]
            fileName = filePathStringList[-1].replace('.csv', '')

            savePath = os.path.join(config.save_folder_path, Trial, Patient, Session)


            # df = pd.read_csv(os.path.join(config.data_path, file))
            df = pd.read_csv(filePath)
            print(df)

            V=np.asarray(df.iloc[:,0])
            print(V)
            
            rows = df.shape[0]
            columns = df.shape[1]

            # absTime: absolute time in yyy-mm-dd hh:mm:sssssssss
            absTime=[]

            # relTime: time passed since recording started
            relTime=[]

            # time difference between two subsequent time stamps 
            # ideally should always be 1/fs if the recording is stable and uninterrupted
            timeDifference=[]

            for i in range(rows):
                # time stamp is stored in miliseconds resolution
                # therefore timestamp needs to be divided by 1000
                dateTime = datetime.datetime.fromtimestamp(df.loc[i,'TS']/1000)
                # print('Converted date time: {}'.format(dateTime))
                absTime.append(dateTime)

                ################################
                #use code below if absTime.sort() is NOT used
                ################################
                if i==0:
                    relTime.append(0)
                    #timeDifference.append(1/fs)                
                elif i>0:
                    relTime.append((absTime[i]-absTime[0]).total_seconds())
                    timeDifference.append((absTime[i]-absTime[i-1]).total_seconds())
                # print('Time difference between current samples: {} s'.format(timeDifference[i]))
                
                # if timeDifference[i] != 1/fs:
                #     print('!!!!!!!!! Time stamp error detected. !!!!!!!!!!')

                # if timeDifference[i] <0:
                #     print('negative time difference detected')

                #################################
                #################################
            
            fs = int(1/timeDifference[0])
            print('Sampling frequency is {}'.format(fs))
            Ts = 1/fs
            print('Time step is {}'.format(Ts))
            # absTime.sort()

            ###################################################    
            # use code below only if absTime.sort() is used
            # #############################################         
            

            # for i in range(len(absTime)):
            #     if i ==0:
            #         relTime.append(0)
            #         timeDifference.append(1/fs)
            #     elif i>0:
            #         relTime.append((absTime[i]-absTime[0]).total_seconds())
            #         timeDifference.append((absTime[i]-absTime[i-1]).total_seconds())
            #     if timeDifference[i] != 1/fs:
            #         print('!!!!!!!!! Time stamp error detected. !!!!!!!!!!')
            #     if timeDifference[i]==0:
            #         print('0 time diff detected')



            ##################################################
            ##################################################
            
            relTime = np.asarray(relTime)
            timeDifference = np.asarray(timeDifference)
            # check for missed measurements (spotty samples)
            checkIndices = np.asarray(np.where(timeDifference != 1/fs))
            checkNegIndices = np.asarray(np.where(timeDifference < 0))
            checkValues = np.asarray(timeDifference[checkIndices])
            print('Number of potentially spotty regions: {}'.format(checkIndices.size))
            minValueIndice = np.asarray(np.where(timeDifference==np.min(timeDifference)))
            
            # print(minValueIndice)
            # print(checkIndices)
            # print(checkValues)
            # print(np.min(checkValues))
            # print(np.max(checkValues))
            # print('In total {} spotty regions were found'.format(checkValues.size))
            # print('Resulting in {} undersampled time in seconds.'.format(np.sum(checkValues[0])))
            # print(checkValues)
            # print(relTime[checkIndices])
            # print(relTime[checkIndices-1])
            # print(checkNegIndices)
            # print(checkIndices.shape)

            plot_time_series_spotty_regions(data=V, time=relTime, savePath=savePath, fileName=fileName, title=fileName, xIndices=checkIndices, width=20, height=10, timeRange=20)
