import pandas as pd 
import argparse
import os
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme()
import numpy as np
from scipy import stats 
import statannot
from statannotations.Annotator import Annotator



#############################################################################
# This code is used to plot the wave forms for each inspiratory hold that was 
# conducted and safe it.
#############################################################################

if __name__ == "__main__":

    # parse arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, required=True)
    parser.add_argument('--pressure_recording_path', type=str, required=False)
    parser.add_argument('--save_folder', type=str, required=False, default='.')
    parser.add_argument('--patient', type=str, required=True)
    parser.add_argument('--session', type=int, required=True)
    config = parser.parse_args()

    dataDF=pd.read_csv(config.data_path)
    recordingDF = pd.read_csv(config.pressure_recording_path)

    patientList = ['1L', '1R', '2L', '2R', '3L', '3R', '4L', '4R', '5L', '5R', '6L', '6R', '7L', '7R', '8L', '8R']
    sessionList = [1, 2, 3]
    
    save_path=os.path.join(config.save_folder, config.patient, 'session_'+str(config.session))
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
        print('{} folder created.'.format(save_path))
    else:
        print('{} already exists.'.format(save_path))


    dataDF=pd.read_csv(config.data_path)

    dfTemp = dataDF[dataDF['Patient']==config.patient]
    df=dfTemp[dfTemp['Session']==config.session]
    NRows = len(df.index)

    startTimeList = []
    endTimeList = []

    for i in range(NRows):
        startTimeList.append(df.loc[df.index[i], 'start time'])
        endTimeList.append(df.loc[df.index[i], 'end time'])
    print(startTimeList, endTimeList)

    time=recordingDF['TS'].to_numpy()
    pressure = recordingDF['P'].to_numpy()
    time = (time-time[0])/60000
    print(time)

    plateaouWaveList=[]
    for i in range(len(startTimeList)):
        indices = np.where(time>=startTimeList[i])
        startIndex=indices[0][0]
        indices= np.where(time<endTimeList[i])
        endIndex=indices[0][-1]
        plateaouWaveList.append(pressure[startIndex:endIndex])
        plt.plot(plateaouWaveList[i])

    plateaouWaveDF=pd.DataFrame(data=plateaouWaveList).T
    print(plateaouWaveDF)

    save_name = 'patient_{}_session_{}_plateaou_pressure_waveforms.csv'.format(config.patient, config.session)
    print(save_name)
    plateaouWaveDF.to_csv(os.path.join(save_path, save_name))
    #print(plateaouWaveList)
    


    plt.show()

    
    #print(indices)
    #print(df)


