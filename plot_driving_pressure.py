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
# This code is used to plot the extracted driving pressure values and peak 
# inspiratory pressures across patient pairs for iSAVE clinical trial. The code 
# allows to either plot the data across the three Sessions OR across the three 
# Sessions for each patient It also allows to statistically test for a 
# difference between sessions. 
#############################################################################


if __name__ == "__main__":

    # parse arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, required=False)
    parser.add_argument('--save_folder', type=str, required=False, default='.')
    parser.add_argument('--data_path_P_patient_1', type=str, required=False)
    parser.add_argument('--data_path_V_patient_1', type=str, required=False)
    parser.add_argument('--data_path_F_patient_1', type=str, required=False)
    parser.add_argument('--data_path_SPO2_patient_1', type=str, default='', required=False)
    config = parser.parse_args()

    dataDF=pd.read_csv(config.data_path)

    patientList = ['1L', '1R', '2L', '2R', '3L', '3R', '4L', '4R', '5L', '5R', '6L', '6R', '7L', '7R', '8L', '8R']
    sessionList = [1, 2, 3]

    sessionDFList = []
    for session in sessionList:
        df = dataDF[dataDF['Session']==session]
        sessionDFList.append(df)

    patientDFList = []
    for patient in patientList:
        df = dataDF[dataDF['Patient']==patient]
        patientDFList.append(df)

    

    patientSessionDFList = []
    for patient in patientList:
        tempSessionList = []
        df = dataDF[dataDF['Patient']==patient]
        for session in sessionList:
            dfSession = df[df['Session']==session]
            tempSessionList.append(dfSession)
        patientSessionDFList.append(tempSessionList)   
    
    print(patientSessionDFList[0][0])
    print(patientSessionDFList[1])
    print(len(patientSessionDFList))
    print(len(patientSessionDFList[0]))

    statstest=True
    
    if statstest:
        #pairs to compare
        pairs = [(1,2),(1,3),(2,3)]

        DPlist = []
        tStatList = []
        pValueList = []
        for session in sessionList:
            DPlist.append(dataDF[dataDF['Session']==session]['DP'])
 
        t_stat, p_value = stats.ttest_ind(DPlist[0], DPlist[1])
        tStatList.append(t_stat)
        pValueList.append(p_value)
        t_stat, p_value = stats.ttest_ind(DPlist[0], DPlist[2])
        tStatList.append(t_stat)
        pValueList.append(p_value)
        t_stat, p_value = stats.ttest_ind(DPlist[1], DPlist[2])
        tStatList.append(t_stat)
        pValueList.append(p_value)
        print(tStatList)
        print(pValueList)

    fig1, axs = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
    fig1.set_dpi(100)
    fig1.suptitle('Driving pressure across sessions', fontsize=18)
    fig1.set_figwidth(12)
    fig1.set_figheight(7)
    sns.violinplot(ax=axs, data=dataDF, x='Session', y='DP', kind='violin', color='.9', inner=None)
    sns.swarmplot(ax=axs, data=dataDF, x='Session', y='DP', size=3)
    axs.set_ylabel('Driving pressure [mmHg]')
    axs.set_ylim([0,30])

    annotator=Annotator(axs, pairs, dataDF, x='Session', y='DP')
    annotator.set_custom_annotations(pValueList)
    annotator.annotate()


    fig1Name = 'driving_pressure_sessions.pdf'
    fig1.savefig(os.path.join(config.save_folder, fig1Name))

    computethis=True
    if computethis:
        nRows=4
        nCols=4
        fig2, axs = plt.subplots(nrows=nRows, ncols=nCols, sharex=True, sharey=False)
        fig2.set_dpi(100)
        fig2.suptitle('Driving pressure across patients and sessions', fontsize=18)
        #fig2.tight_layout()
        print('i like big butts and i cannot lie')
        fig2.set_figwidth(7)
        fig2.set_figheight(10)
        print(len(axs))
        k=0
        
        for i in range(nRows):
            for j in range(nCols):
                currentDF=patientDFList[k]
                print(currentDF['Patient'])
                #sns.catplot(ax=axs[i,j], data=currentDF, x='Session', y='DP', kind='violin', color='.9', inner=None)
                sns.swarmplot(ax=axs[i,j], data=currentDF, x='Session', y='DP', size=3)
                axs[i,j].set_ylabel('')
                if i!=3:
                    axs[i,j].set_xlabel('')
                if j!=0:
                    axs[i,j].set_yticklabels([])
                axs[i,j].set_title('Patient {}'.format(currentDF.iloc[0, 0]))
                axs[i,j].set_ylim([0,25])
                k=k+1
                
        fig2.supylabel('Driving pressure [mmHg]')
        fig2Name = 'driving_pressure_across_patients_and_sessions.pdf'
        fig2.savefig(os.path.join(config.save_folder, fig2Name))
        #plt.tight_layout()
    
    
    # nRows=4
    # nCols=4
    # fig2, axs = plt.subplots(nrows=nRows, ncols=nCols, sharex=True, sharey=False)
    # fig2.set_dpi(100)
    # fig2.suptitle('Peak inspiratory pressure across patients and sessions', fontsize=18)
    # #fig2.tight_layout()
    # fig2.set_figwidth(7)
    # fig2.set_figheight(10)
    # print(len(axs))
    # k=0
    
    # for i in range(nRows):
    #     for j in range(nCols):
    #         currentDF=patientDFList[k]
    #         print(currentDF['Patient'])
    #         #sns.catplot(ax=axs[i,j], data=currentDF, x='Session', y='DP', kind='violin', color='.9', inner=None)
    #         sns.swarmplot(ax=axs[i,j], data=currentDF, x='Session', y='PIP', size=3)
    #         axs[i,j].set_ylabel('')
    #         if i!=3:
    #             axs[i,j].set_xlabel('')
    #         if j!=0:
    #             axs[i,j].set_yticklabels([])
    #         axs[i,j].set_title('Patient {}'.format(currentDF.iloc[0, 0]))
    #         axs[i,j].set_ylim([0,60])
    #         k=k+1
            
    # fig2.supylabel('PIP [mmHg]')
    # fig2Name = 'PIP_across_patients_and_sessions.pdf'
    # fig2.savefig(os.path.join(config.save_folder, fig2Name))    
    
    
    # fig1, axs = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
    # fig1.set_dpi(100)
    # fig1.suptitle('Peak inspiratory pressure across sessions', fontsize=18)
    # fig1.set_figwidth(12)
    # fig1.set_figheight(7)
    # sns.violinplot(ax=axs, data=dataDF, x='Session', y='PIP', kind='violin', color='.9', inner=None)
    # sns.swarmplot(ax=axs, data=dataDF, x='Session', y='PIP', size=3)
    # axs.set_ylabel('PIP [mmHg]')
    # axs.set_ylim([0,60])
    # fig1Name = 'peak_inspiratory_sessions.pdf'
    # fig1.savefig(os.path.join(config.save_folder, fig1Name))
    
    
    
    
    
    
    plt.show()

    # axs=sns.catplot(data=dataDF, x='Session', y='DP', kind='violin', color='.9', inner=None)
    # axs=sns.swarmplot(data=dataDF, x='Session', y='DP', size=3)
    # axs.set_ylabel('Driving pressure [mmHg]')
    # plt.show()



    # sortedDF=dataDF.sort_values(by=['Session'])
    # print(sortedDF)



   
