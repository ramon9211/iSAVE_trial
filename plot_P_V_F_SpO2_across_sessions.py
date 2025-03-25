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

####
# This code is used to plot the graph data for each patient (P, V, F) along with the SPO2 levels (if needed). 
# data_p1: list of data frames that contains time series data for patient 1 with respect to different parameters (P,V,F,SPO2)
# data_p2: list of data frames that contains time series data for patient 2 with respect to different parameters (P,V,F,SPO2)
# data_params_p1: list where each element contains a letter string indicates what vital parameter was read in at what list element (P, V, F, SPO2) for patient 1
###

font = {'size'   : 20}

plt.rc('font', **font)

def plot_time_series(data=[], data_p1=[], data_p2=[], data_params=[], data_params_p1=[], data_params_p2=[], units=[], units_p1=[], units_p2=[], ylim_list=[], title=[], resultPath=[], trial=[], patient=[], fs=100, width=12, height=10, saveFileName=''):
    columns=1
    if len(data) >= 1:
        rows = len(data)

    fig, axs = plt.subplots(nrows=rows, ncols=columns, sharex=True, sharey=False)
    fig.set_dpi(300)
    fig.suptitle(title, fontsize=24)
    fig.tight_layout()
    fig.set_figwidth(width)
    fig.set_figheight(height)
    

    # timeList = []
    # print(data_p1)
    # time_p1_P = np.arange(len(data_p1[0]))*1/fs
    # timeList.append(time_p1_P)
    # time_p1_V = np.arange(len(data_p1[1]))*1/fs
    # timeList.append(time_p1_V)
    # time_p1_F = np.arange(len(data_p1[2]))*1/fs
    # timeList.append(time_p1_F)

    # print(data_p1[0].iloc[:,1])
    

    # for i in range(len(data_p1)):
    #     timeList.append((1/(fs*60))*np.arange(len(data_p1[i])))

    # print(data_p1[0].iloc[:,0])

    if len(data) >= 1: 
        for i in range(columns):
            for j in range(rows):
                    if j==2:
                        axs[j].plot((data[j].iloc[:,1]-data[j].iloc[0,1])/1000, data[j].iloc[:,0])
                    else:
                        axs[j].plot((data[j].iloc[:,1]-data[j].iloc[0,1])/1000, data[j].iloc[:,0])
                    axs[j].grid()
                    axs[j].set_xlim([5030, 5040])
                    if units != []:
                        axs[j].set_ylabel(units[j])
                        axs[j].set_title(data_params[j])
                        axs[j].set_ylim(ylim_list[j])
                    if j == rows-1:
                        axs[j].set_xlabel('time/s')
                        t_max = np.max((data[j].iloc[:,1]-data[j].iloc[0,1])/1000)
                        

    
    # if len(data_p2) >= 1: 
    #     for i in range(columns):
    #         for j in range(rows):
    #             if j<rows/2:
    #                 axs[j].plot((data_p1[j].iloc[:,1]-data_p1[j].iloc[0,1])/1000, data_p1[j].iloc[:,0])
    #                 if units_p1 != []:
    #                     axs[j].set_ylabel(units_p1[j])
    #                     axs[j].set_title(data_params_p1[j])
    #                     axs[j].set_ylim(ylim_list[j])
    #                 if j == rows-1:
    #                     axs[j].set_xlabel('time/s')
    #                     t_max = np.max((data_p1[j].iloc[:,1]-data_p1[j].iloc[0,1])/1000)
    #                     axs[j].set_xlim([0, t_max])
    #             else:
    #                 axs[j].plot((data_p2[j].iloc[:,1]-data_p2[j].iloc[0,1])/1000, data_p2[j].iloc[:,0])
    #                 if units_p1 != []:
    #                     axs[j].set_ylabel(units_p1[j])
    #                     axs[j].set_title(data_params_p1[j])
    #                     axs[j].set_ylim(ylim_list[j])
    #                 if j == rows-1:
    #                     axs[j].set_xlabel('time/s')
    #                     t_max = np.max((data_p2[j].iloc[:,1]-data_p2[j].iloc[0,1])/1000)
    #                     axs[j].set_xlim([0, t_max])
            

    # for i in range(len(data)):
    #     axs[i].plot(timeList[i], data[i], label='Session {}'.format(i+1))
    #     axs[i].set_ylabel('Heart rate [1/min]')
    #     axs[i].legend(loc='lower left')
                    
    # axs[-1].set_xlabel('time/min')
    fig.align_labels()
    fig.tight_layout()

    if saveFileName != '':
        fig.savefig(os.path.join(resultPath, saveFileName+'.png'))
        fig.savefig(os.path.join(resultPath, saveFileName+'.eps'))
        fig.savefig(os.path.join(resultPath, saveFileName+'.pdf'))
    #plt.clf()

    plt.show()

if __name__ == "__main__":

    # parse arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('--ventilation_data_patient_1', type=str, required=False)
    parser.add_argument('--ventilation_data_patient_2', type=str, required=False, default='')
    parser.add_argument('--data_path_P_patient_1', type=str, required=False)
    parser.add_argument('--data_path_V_patient_1', type=str, required=False)
    parser.add_argument('--data_path_F_patient_1', type=str, required=False)
    parser.add_argument('--data_path_SPO2_patient_1', type=str, default='', required=False)

    parser.add_argument('--data_path_P_patient_2', type=str, default='', required=False)
    parser.add_argument('--data_path_V_patient_2', type=str, default='', required=False)
    parser.add_argument('--data_path_F_patient_2', type=str, default='', required=False)
    parser.add_argument('--data_path_SPO2_patient_2', type=str, default='', required=False)
    
    parser.add_argument('--result_path', type=str, required=False)
    parser.add_argument('--fs', type=int, required=False, default=100)
    parser.add_argument('--trial_number', type=int, required=False, default=0)
    parser.add_argument('--patient_ID', type=str, default='0L', required=False)
    parser.add_argument('--title', type=str, default='Ventilation parameters and SPO2, Patient 1R, Session 1', required=False)
    parser.add_argument('--save_file_name', type=str, default='')

    config = parser.parse_args()

    files = [f for f in os.listdir(config.ventilation_data_patient_1) if os.path.isfile(os.path.join(config.ventilation_data_patient_1, f))]
    print(files)
    for file in files:
        if '_P_' in file:
            config.data_path_P_patient_1 = os.path.join(config.ventilation_data_patient_1, file)
        elif '_V_' in file:
            config.data_path_V_patient_1 = os.path.join(config.ventilation_data_patient_1, file) 
        elif '_F_' in file:
            config.data_path_F_patient_1 = os.path.join(config.ventilation_data_patient_1, file)
        
        print(config.data_path_P_patient_1)

    # reading data for all patients
    df_list_data = []
    df_list_parameters = []
    df_list_units = []
    df_list_y_lim_all = []

    # reading in data for patient 1
    df_list_p1 = []
    df_list_parameter_p1 = []
    df_list_units_p1 = []
    df_list_y_lim = []

    df_P_p1 = pd.read_csv(config.data_path_P_patient_1)
    df_list_data.append(df_P_p1)
    df_list_p1.append(df_P_p1)
    df_list_parameters.append('Pressure')
    df_list_parameter_p1.append('Pressure')
    df_list_units.append('mmhg')
    df_list_units_p1.append('mmhg')
    df_list_y_lim.append([0, 40])
    df_V_p1 = pd.read_csv(config.data_path_V_patient_1)
    df_list_p1.append(df_V_p1)
    df_list_data.append(df_V_p1)
    df_list_parameters.append('Volume')
    df_list_parameter_p1.append('Volume')
    df_list_units.append('ml')
    df_list_units_p1.append('ml')
    df_list_y_lim.append([-50, 500])
    df_F_p1 = pd.read_csv(config.data_path_F_patient_1)
    df_list_data.append(df_F_p1)
    df_list_p1.append(df_F_p1)
    df_list_parameters.append('Flow')
    df_list_parameter_p1.append('Flow')
    df_list_units.append('l/min')
    df_list_units_p1.append('l/min')
    df_list_y_lim.append([-40, 80])
    
    
    if config.data_path_SPO2_patient_1 != '':
        df_stats_p1 = pd.read_csv(config.data_path_SPO2_patient_1)
        df_SPO2_p1 = df_stats_p1[['SPO','TS']]
        df_HR_p1 = df_stats_p1[['HR', 'TS']]
        df_list_p1.append(df_SPO2_p1)
        df_list_data.append(df_SPO2_p1)
        print(df_SPO2_p1.head())
        df_list_parameter_p1.append('Oxygen saturation')
        df_list_parameters.append('Oxygen saturation')
        df_list_units_p1.append('% saturation')
        df_list_units.append('% saturation')
        df_list_y_lim.append([50, 110])


    print(df_list_p1)
    print(df_list_p1[0])

    # reading in data for patient 2 if data is given
    df_list_p2 = []
    df_list_parameter_p2 = []
    df_list_units_p2 = []

    # #timestamp comparison because not every measurement starts at exact the same moment
    # TS_list = []
    # for i in range(len(df_list_p1)):
    #     TS = df_list_p1[i].iloc[0,1]
    #     TS_list.append(TS)
    # maxTS = max(TS_list)
    # print(TS_list)
    # print('Latest measurement starts at time stamp {}'.format(maxTS))
    # #slice dataframes so they start with the same TS and are aligned
    # df_P_p1[(df_P_p1.TS==maxTS).idmax():]
    # df_V_p1[(df_V_p1.TS==maxTS).idmax():]
    # df_F_p1[(df_F_p1.TS==maxTS).idmax():]
    # print(df_P_p1, df_V_p1, df_F_p1)

    if config.ventilation_data_patient_2 != '':
        print('hi')

        files = [f for f in os.listdir(config.ventilation_data_patient_2) if os.path.isfile(os.path.join(config.ventilation_data_patient_2, f))]
        print(files)
        for file in files:
            if '_P_' in file:
                config.data_path_P_patient_2 = os.path.join(config.ventilation_data_patient_2, file)
            elif '_V_' in file:
                config.data_path_V_patient_2 = os.path.join(config.ventilation_data_patient_2, file) 
            elif '_F_' in file:
                config.data_path_F_patient_2 = os.path.join(config.ventilation_data_patient_2, file)
            print(config.data_path_P_patient_2)

        if config.data_path_P_patient_2 != '':
            df_P_p2 = pd.read_csv(config.data_path_P_patient_2)
            df_list_data.append(df_P_p2)
            df_list_p2.append(df_P_p2)
            df_list_parameters.append('Pressure')
            df_list_parameter_p2.append('Pressure')
            df_list_units_p2.append('mmHg')
            df_list_units.append('mmHg')

        if config.data_path_V_patient_2 != '':
            df_V_p2 = pd.read_csv(config.data_path_V_patient_2)
            df_list_p2.append(df_V_p2)
            df_list_data.append(df_V_p2)
            df_list_parameters.append('Volume')
            df_list_parameter_p2.append('Volume')
            df_list_units_p2.append('ml')
            df_list_units.append('ml')

        if config.data_path_F_patient_2 != '':
            df_F_p2 = pd.read_csv(config.data_path_F_patient_2)
            df_list_data.append(df_F_p2)
            df_list_p2.append(df_F_p2)
            df_list_parameter_p2.append('Flow')
            df_list_parameters.append('Flow')
            df_list_units_p2.append('l/min')
            df_list_units.append('l/min')

        if config.data_path_SPO2_patient_2 != '':
            df_SPO2_p2 = pd.read_csv(config.data_path_P_patient_2)
            df_list_p2.append(df_SPO2_p2)
            df_list_data.append(df_SPO2_p2)
            df_list_parameter_p2.append('Oxygen saturation')
            df_list_units_p2.append('% saturation')

    plot_time_series(data=df_list_data, data_params=df_list_parameters, units=df_list_units, title=config.title, ylim_list=df_list_y_lim, saveFileName=config.save_file_name, resultPath=config.result_path)
    
    
    
    
