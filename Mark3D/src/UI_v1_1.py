# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 16:33:59 2022

@author: Suranjita

"""

import sys

# Setting the Qt bindings for QtPy
import os
os.environ["QT_API"] = "pyqt5"
from qtpy import QtWidgets

import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor, MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
#FOr buttons
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#End for buttons

import pandas as pd
import functools
from functools import partial
from PyQt5.Qt import *

#Importing background plotter so that we can operate on the pyvista mesh and 
#update it in the background
from pyvistaqt import BackgroundPlotter
import HM_Utils
from HM_Utils import *
import pandas as pd
import scipy
from scipy.io import loadmat
import mne

#%%
class MainWindow(QMainWindow):

    def __init__(self):
        
        def import_file():
            from PyQt5.QtWidgets import QApplication, QFileDialog

            app = QApplication([])
            
            file_dialog = QFileDialog()
            file_dialog.setNameFilter("Text files (*.stl *.obj)")
            file_dialog.selectNameFilter("Text files (*.stl *.obj)")
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setWindowTitle("Open File")
            
            if file_dialog.exec_() == QFileDialog.Accepted:
                MyPlotter.clear()
                selected_file = file_dialog.selectedFiles()[0]
                mesh = pv.read(selected_file)
                decimated_mesh= mesh.decimate(target_reduction=0.8) #reduce the mesh
                mesh=decimated_mesh
                vertices = mesh.points
                faces = mesh.faces.reshape((-1,4))[:, 1:4]
                self.vertices=vertices
                self.positionArray=np.array([0,0,0])
                self.imported_labels=[]
                self.ButtonStatus=[0]*(len(self.df))
                MyPlotter.add_mesh(mesh, show_edges=True, color='w')
                MyPlotter.enable_point_picking(callback=callback, point_size=1, color='red', use_mesh=True)
                

                HM_Utils.picked_points=[]
                HM_Utils.Label_sensors=[]
                  
                update_montage()
                
            app.exec_()
        def import_existing_data():
            #File imports  
            self.ImportStatus=1
            dataframe1 = np.loadtxt("Coordinates_savelfile.txt")
            self.ButtonStatus=np.loadtxt("ButtonStatus.txt")
            my_file = open("Labels_savedfile.txt", "r")
            dataframe2 = my_file.readlines()
            self.imported_labels=[]
            for d in dataframe2:
                d=d.replace("\n", "")
                self.imported_labels.append(d)
            my_file.close()
            HM_Utils.picked_points=np.vstack(([0,0,0],dataframe1)).transpose()
            HM_Utils.Label_sensors=self.imported_labels
            for point in dataframe1:
                MyPlotter.add_mesh(pv.Sphere(radius=3, center=point),color='red')
            MyPlotter.add_point_labels(dataframe1, dataframe2, point_size=2, font_size=10)
                
            #Update layout
            update_montage()            
            return
       
        def view_axis():
            MyPlotter.add_axes()
            
        def view_montage():         
            dff=['test']
            for i in self.df:
                dff.append(i[0])
            dff.pop(0)
            poly=pv.PolyData(self.df2)
            poly["My Labels"] =dff
            self.actor=MyPlotter2.add_points(self.df2, show_edges=True, color='w', point_size=15)
            self.actorLabels=MyPlotter2.add_point_labels(poly, "My Labels", font_size=10)
            
        def remove_montage():
            MyPlotter2.clear()
            
        def update_montage(): #updates the 2D layout of the montage
            MyPlotter2.clear()
            
            temp_dff1=['test']
            temp_dff2=['test']
            temp_df2_1=np.array([0,0,0])
            temp_df2_2=np.array([0,0,0])
            #pos_2d, names_2d = Create2DLayout()
            for i, j in enumerate(self.df):
                if self.ButtonStatus[i]==1: #Green
                    temp_dff1.append(j)
                    temp_df2_1=np.column_stack((temp_df2_1,self.df2[i]))
                else:                       #White
                    temp_dff2.append(j)
                    temp_df2_2=np.column_stack((temp_df2_2,self.df2[i]))
            temp_dff1.pop(0)
            temp_dff2.pop(0)
            temp_df2_1=temp_df2_1.transpose().tolist()
            temp_df2_2=temp_df2_2.transpose().tolist()
            temp_df2_1.pop(0)
            temp_df2_2.pop(0)
            
            
            poly1=pv.PolyData(temp_df2_1)
            poly1["My Labels"] = temp_dff1
            
            poly2=pv.PolyData(temp_df2_2)
            poly2["My Labels"] = temp_dff2  
            
            MyPlotter2.add_points(np.asarray(temp_df2_1), show_edges=True, color='red', point_size=15)
            MyPlotter2.add_point_labels(poly1, "My Labels", point_size=2, font_size=10)
            
            MyPlotter2.add_points(np.asarray(temp_df2_2), show_edges=True, point_size=15)
            MyPlotter2.add_point_labels(poly2, "My Labels", point_size=10, font_size=10)

                        
        def save_file():
            temp=HM_Utils.picked_points
            temp=temp.transpose().tolist()
            #if self.ImportStatus==0:
            temp.pop(0)
            temp=np.asarray(temp)
            np.savetxt("Coordinates_savelfile.txt", temp)
            np.savetxt("ButtonStatus.txt", self.ButtonStatus)
            #np.savetxt("labels.txt",HM_Utils.Label_sensors )
            a_list = HM_Utils.Label_sensors
            textfile = open("Labels_savedfile.txt", "w")
            for element in a_list:
                textfile.write(element + "\n")
            textfile.close()
            
        
        def createArray(point):
            self.positionArray=np.column_stack((self.positionArray, point))
            print(self.positionArray)
            return

        def callback(mesh, id):
            print("code snippet working!", mesh, "   ", id)
            self.point=self.vertices[id]
            print("vertex is", self.point)
            #createArray(self.point) ================================ Can ALSO USE THIS
            HM_Utils.picked_points=np.column_stack((HM_Utils.picked_points,self.point))
            print(HM_Utils.picked_points)
            MyPlotter.add_mesh(pv.Sphere(radius=5, center=self.point),
                           color='red')
             
            
        def on_click(state,selected_button):  #The callback is here ; responsible for toggle
            print('button click of',selected_button, " ", state)
            MyPlotter.add_point_labels(np.add(self.point, [0.7,0.7,0.7]), [selected_button], point_size=10, font_size=20, text_color='red') 
            #self.buttonArray=self.buttonArray+self.button_select
            index=[i for i,x in enumerate(self.df) if x == selected_button][0]
            if state:
                HM_Utils.Label_sensors=HM_Utils.Label_sensors+[selected_button]
                #index=self.df.index(selected_button)
                self.ButtonStatus[index]=1
               
                
            if not state:
                self.ButtonStatus[index]=0
                
                #rempove the specific vertex from HM_Utils.picked_points
                temp1=HM_Utils.picked_points.transpose().tolist()
                
                temp2=HM_Utils.Label_sensors
                indx=temp2.index(selected_button)
                MyPlotter.add_mesh(pv.Sphere(radius=5, center=HM_Utils.picked_points.transpose()[indx+1]),
                           color='yellow')
                
                temp1.pop(indx+1)
                temp2.pop(indx)
                
                HM_Utils.picked_points=np.asarray(temp1).transpose()
                HM_Utils.Label_sensors=temp2
              
            update_montage()
            
        def Create2DLayout(AuxList):
            #Digmontage
            #%%
            mon1=loadmat("C:/Mark3D/src/128Ch_Montage.mat")
            xpos=mon1['Mon']['xposition'][0][0].ravel()
            ypos=mon1['Mon']['yposition'][0][0].ravel()
            zpos=mon1['Mon']['zposition'][0][0].ravel()
            nch=len(xpos)
            
            ch_pos1=np.concatenate((xpos.reshape(nch,1),ypos.reshape(nch,1),zpos.reshape(nch,1)),axis=1)
            
            Ename=mon1['Mon']['electrodename'][0][0].flatten()
            Ename2=[]
            for i in np.arange(len(Ename)):
                chx=Ename[i][0]
                Ename2=np.append(Ename2,chx)
                   
                
            Enum=mon1['Mon']['electrodenumber'][0][0].ravel()
            #Enum is the electrode number from the electrode box itself
            
            df=pd.DataFrame()
            df['xpos']=xpos
            df['ypos']=ypos
            df['zpos']=zpos
            df['ch_names']=Ename2
            df['ch_num']=Enum
            df2=df.sort_values('ch_num')        
           
               
            #---------------------------------------
            
            
            Nzx=mon1['Mon']['gridxposition'][0][0].ravel()[0]
            Nzy=mon1['Mon']['gridyposition'][0][0].ravel()[0]
            Nzz=mon1['Mon']['gridzposition'][0][0].ravel()[0]
            Nz_pos=np.array([Nzx,Nzy,Nzz])
            
            Nzx=mon1['Mon']['gridxposition'][0][0].ravel()[73]
            Nzy=mon1['Mon']['gridyposition'][0][0].ravel()[73]
            Nzz=mon1['Mon']['gridzposition'][0][0].ravel()[73]
            A1=np.array([Nzx,Nzy,Nzz])
            
            Nzx=mon1['Mon']['gridxposition'][0][0].ravel()[74]
            Nzy=mon1['Mon']['gridyposition'][0][0].ravel()[74]
            Nzz=mon1['Mon']['gridzposition'][0][0].ravel()[74]
            A2=np.array([Nzx,Nzy,Nzz])
            
            xpos1=df2.iloc[0,0]
            ypos1=df2.iloc[0,1]
            zpos1=df2.iloc[0,2]
            
            ch_dict={df2.iloc[0,3]:np.array([xpos1,ypos1,zpos1])}
            
            for i in np.arange(df2.shape[0]-1):
                xpos2=df2.iloc[i+1,0]
                ypos2=df2.iloc[i+1,1]
                zpos2=df2.iloc[i+1,2]
                dict1={df2.iloc[i+1,3]:np.array([xpos2,ypos2,zpos2])}
                ch_dict.update(dict1)
                #%%
            digMon1=mne.channels.make_dig_montage(ch_pos=ch_dict,nasion=Nz_pos, lpa=A1, rpa=A2)

            ch_names=pd.Series.tolist(df2['ch_names'])
            Enum=pd.Series.tolist(df2['ch_num']-1)

            eegdat=np.zeros((131,1))
            #-------------------------------------------
            eegdat_final=eegdat[Enum,:]
            eegdat=eegdat_final
            #eegdat2=np.concatenate((eegdat,Trig1200.reshape(1,eegdat.shape[1])))

            #Create the data structure
            sampling_freq=1200
            #ch_names=ch_names.tolist()
            #ch_types=['eeg']*1+['misc']*2+['eeg']*125+['ecg']*2+['stim']*1   #misc are our two reference channels
            ch_types=['eeg']*1+['misc']*2+['eeg']*78+['eog']+['eeg']*8+['eog']+['eeg']*33   #misc are our two reference channels
            info1=mne.create_info(ch_names=ch_names, ch_types=ch_types,sfreq=sampling_freq)  #- this gives error
            # to automatically set momtage ------info1.set_montage('standard_1020')
            print(info1)
            raw=mne.io.RawArray(eegdat,info1)
            raw.set_montage(digMon1, on_missing='ignore')

            #PLOT EEG SENSOR LOCS
            layout_from_raw = mne.channels.make_eeg_layout(raw.info)
           
            #layout_from_raw.plot()
            pos=layout_from_raw.pos[:,0:2]
            pos=np.vstack((pos, [0,0]))
            pos=np.vstack((pos, [0,0]))
            pos=np.vstack((pos, [0,0]))
            names=layout_from_raw.names
            names.append("Nasion")
            names.append("LPA")
            names.append("RPA")
            for i in AuxList:
                pos=np.vstack((pos, [0,0]))
                names.append(i)
                #%%
            return pos, names
            
        def sensor_marker():
            w = p.add_mesh(pv.Sphere(radius=3, center=point),
                           color='red')
            return
        
#%%        
        #-------------------------------------------------------------Imports
        self.ImportStatus=0
        AuxList=['Aux1', 'Aux2', 'Aux3', 'Aux4', 'Aux5', 'Aux6', 'Aux7', 'Aux8', 'Aux9', 'Aux10', 'Aux11', 'Aux12', 'Aux13']
        #mesh = pv.read(r"D:\Mark3D_ExptData\SubjectsWithRedmiAndEinscan\Mark3D_11\CloudCompare\720_rescaled.stl") #Recon_phoneVid.stl #Somen_rotating.stl
        mesh = pv.read("D:\PhD Data\Affect\Data\Einscan Scan\S14.stl")
        decimated_mesh= mesh.decimate(target_reduction=0.8) #reduce the mesh
        mesh=decimated_mesh
        vertices = mesh.points
        faces = mesh.faces.reshape((-1,4))[:, 1:4]
        self.vertices=vertices
        self.positionArray=np.array([0,0,0])
        self.buttonArray=([])
        self.imported_labels=[]
             
        temp1,temp2=Create2DLayout(AuxList)
        
        #self.df = temp2
        self.df=np.asarray(temp2)
        self.ButtonStatus=[0]*(len(self.df))  # Stores either 0 or 1 based on the status of click
        

        self.df2=np.asarray(temp1)
        temp=np.zeros(len(temp2));
        self.df2=np.column_stack((self.df2,temp))
        #self.df2=np.asarray(FindProjectionOnSphereFromLayoutOnly(self.df2))
        #df stores the names/labels of the electrodes
        #df2 stores the default corodinates of the corresponding labels
#%%        
        #-----------------------------------------------Set UI Layout elements      
        super(MainWindow, self).__init__()
        self.setWindowTitle("Mark3D")

        hbox = QHBoxLayout()        
        topleft = QFrame()
        topleft.setFrameShape(QFrame.StyledPanel)
        HMframe = QFrame()
        HMframe.setFrameShape(QFrame.StyledPanel)
        HMframe.setMinimumHeight(512)
        		
        splitter1 = QSplitter(Qt.Vertical) #Horizontally splits the frame horizontally into two
        bottomleft = QFrame()
      
        splitter1.addWidget(topleft)
        splitter1.addWidget(bottomleft)
        splitter1.setSizes([3,2]) #give the ratio of the divide as arg
        
		
        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(HMframe)
        splitter2.setSizes([256,1024]) 
        
        
        hbox.addWidget(splitter2)
        widget = QWidget()
        widget.setLayout(hbox)
        self.setGeometry(10, 50, 2048, 1024)
        self.setCentralWidget(widget)
        
        
        #-----------------------------------------------------------Make Menus
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        viewMenu = mainMenu.addMenu('View')
        
        #File Menu Buttons
        exitButton = QtWidgets.QAction('Exit', self)
        newButton = QtWidgets.QAction('Import file', self)
        saveButton = QtWidgets.QAction('Save file', self)
        importdataButton = QtWidgets.QAction('Import Marked Locations', self)
        #View Menu Buttons
        axisButton = QtWidgets.QAction('View Axis', self)
        layoutButton = QtWidgets.QAction('View Layout', self)
        removelayoutButton = QtWidgets.QAction('Remove Layout', self)
                
        exitButton.setShortcut('Ctrl+Q')
        newButton.setShortcut('Ctrl+N')
        saveButton.setShortcut('Ctrl+S')
        
        exitButton.triggered.connect(self.close)
        newButton.triggered.connect(import_file)
        saveButton.triggered.connect(save_file)
        importdataButton.triggered.connect(import_existing_data)
        axisButton.triggered.connect(view_axis)
        layoutButton.triggered.connect(view_montage)
        removelayoutButton.triggered.connect(remove_montage)
        
        fileMenu.addAction(exitButton)
        fileMenu.addAction(newButton)
        fileMenu.addAction(saveButton)
        fileMenu.addAction(importdataButton)
        viewMenu.addAction(axisButton)
        viewMenu.addAction(layoutButton)
        viewMenu.addAction(removelayoutButton)
        
        
        
        
        #------------------------------------------- Add elements to UI layout
        self.BackgroundPlotter = QtInteractor(HMframe)
        MyPlotter=self.BackgroundPlotter  
        MyPlotter.setMinimumHeight(1024)
        MyPlotter.setMinimumWidth(1500)
        
        
        self.BackgroundPlotter = QtInteractor(bottomleft)
        MyPlotter2=self.BackgroundPlotter 
        
        '''
        AuxList=['Aux1', 'Aux2', 'Aux3', 'Aux4', 'Aux5', 'Aux6', 'Aux7', 'Aux8', 'Aux9', 'Aux10', 'Aux11', 'Aux12', 'Aux13']
        self.df.tolist()
        for temp_aux in AuxList:
            self.df=np.append(self.df,temp_aux)
        '''
        len_df=len(self.df)  
        row_len=np.sqrt(len_df)
        row_len=round(row_len)
        _list=self.df
        rows = int(row_len+1)
        columns = int(row_len+1)
        len_list = len(_list)
        i = 0
        j=0
        indx=0
        #buttonlist=[]
        
        for row in range(rows): 
           for column in range(columns): 
                self.button = QPushButton(f'{_list[indx]}', topleft)
                print(_list[indx])
                text = self.button.text()
                
                self.button.setGeometry(50,50,50,50) #(left, top, width, height)
                self.button.move(10*i+10,10*j+10)
                self.button.setCheckable(True)
                state=self.button.isChecked()
                self.button.clicked.connect(lambda state=state,text=text: on_click(state,text))
                i += 5
                indx+=1
                if indx == len_list: 
                    break
            
           j += 5
           i=0
           if indx == len_list: 
                    break
           
        
        i=0
        
        MyPlotter.add_mesh(mesh, show_edges=True, color='w')
        MyPlotter.enable_point_picking(callback=callback, point_size=1, color='red', use_mesh=True)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    app.exec()
