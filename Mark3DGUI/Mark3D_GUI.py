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
dirname = os.path.dirname(os.path.abspath(__file__))
verboseLevel = "\"" + "error" + "\""  
#%%
class MainWindow(QMainWindow):

    def __init__(self):
        
        def import_file():

            """
            Opens a file dialog to select a 3D mesh file and processes the selected file.
        
            The function uses PyQt5 to present a file dialog that allows the user to choose a 
            3D mesh file with the extension `.stl` or `.obj`. Upon file selection, the function 
            reads the mesh file, reduces its complexity by decimating the mesh, and updates 
            the visualization in `MyPlotter`. It also initializes or resets various internal 
            attributes and utilities.
        
            Functionality:
            - Initializes a PyQt5 application and file dialog.
            - Filters for `.stl` and `.obj` file types.
            - Reads the selected mesh file and applies decimation to reduce its complexity.
            - Updates `MyPlotter` with the processed mesh.
            - Resets internal attributes such as `self.vertices`, `self.positionArray`, 
              `self.imported_labels`, and `self.ButtonStatus`.
            - Clears and updates utilities such as `HM_Utils.picked_points` and `HM_Utils.Label_sensors`.
            - Calls `update_montage()` to refresh the visualization or associated data.
            - Runs the PyQt5 application event loop.
        
            Dependencies:
            - `PyQt5` for GUI components.
            - `pv` for reading and processing 3D mesh files.
            - `MyPlotter` for 3D mesh visualization.
            - `HM_Utils` for managing picked points and sensor labels.
            - `update_montage()` for updating visualization.
        
            Notes:
            - Ensure that `MyPlotter`, `pv`, `HM_Utils`, and `update_montage` are correctly 
              defined and imported in your code.
            - The `callback` function used in `MyPlotter.enable_point_picking` should be defined 
              elsewhere in your code.
        
            Returns:
            - None
            """

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

            """
            Imports existing data from saved files and updates the visualization and internal state.
         
            This function loads data from predefined text files that store coordinates, button statuses,
            and labels. It updates internal attributes with the loaded data and visualizes the imported 
            coordinates by adding spheres and labels to the plot. The function also updates the layout 
            of the visualization.
         
            Functionality:
            - Sets the `ImportStatus` attribute to `1` to indicate data import.
            - Loads coordinate data from "Coordinates_savelfile.txt" and button status from "ButtonStatus.txt".
            - Reads label data from "Labels_savedfile.txt" and stores it in `self.imported_labels`.
            - Updates `HM_Utils.picked_points` with the loaded coordinates.
            - Updates `HM_Utils.Label_sensors` with the loaded labels.
            - Adds spheres at the imported coordinates to `MyPlotter` with a red color.
            - Adds point labels to the plot using the loaded coordinates and labels.
            - Calls `update_montage()` to refresh the visualization layout.
         
            Dependencies:
            - `np` (NumPy) for loading coordinate and button status data.
            - `MyPlotter` for visualizing spheres and point labels.
            - `HM_Utils` for managing picked points and sensor labels.
            - `pv` (presumably PyVista or a similar library) for creating spheres.
            - `update_montage()` for updating the visualization layout.
         
            Notes:
            - Ensure that the files "Coordinates_savelfile.txt", "ButtonStatus.txt", and "Labels_savedfile.txt"
              exist in the working directory and are correctly formatted.
            - The function assumes that `MyPlotter` and `HM_Utils` are properly initialized and accessible.
         
            Returns:
            - None
            """
  
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

            """
            Adds axes to the current plot in `MyPlotter`.
        
            This function calls `MyPlotter.add_axes()` to display axes in the plot, providing a reference 
            for orientation and scale within the visualization. The axes help in understanding the 
            spatial arrangement of the plotted data.
        
            Dependencies:
            - `MyPlotter` for adding axes to the plot.
        
            Notes:
            - Ensure that `MyPlotter` is correctly initialized and that the plot is currently active 
              when this function is called.
        
            Returns:
            - None
            """
            
            MyPlotter.add_axes()
            
        def view_montage():    
            """
            Visualizes the montage by adding points and labels to `MyPlotter2`.
        
            This function processes data to display a montage visualization. It performs the following 
            tasks:
            - Constructs a list of labels from `self.df`.
            - Creates a `pv.PolyData` object with the data from `self.df2`.
            - Associates the labels with the `PolyData` object.
            - Adds points to the plot using `MyPlotter2`, with specified attributes for visibility.
            - Adds labels to the points in the plot using `MyPlotter2`.
        
            Functionality:
            - Constructs `dff` as a list of labels derived from `self.df`.
            - Creates a `pv.PolyData` object using `self.df2` and assigns the constructed labels to it.
            - Uses `MyPlotter2` to add points from `self.df2` to the plot, showing edges and setting the color and size.
            - Adds point labels to the plot with the specified font size.
        
            Dependencies:
            - `pv` (assumed to be PyVista or a similar library) for creating `PolyData` objects.
            - `MyPlotter2` for adding points and labels to the plot.
        
            Notes:
            - Ensure that `self.df` and `self.df2` contain the necessary data and are properly formatted.
            - Ensure that `MyPlotter2` is correctly initialized and capable of adding points and labels.
        
            Returns:
            - None
            """
   
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

            """
            Clears the current montage from `MyPlotter2`.
        
            This function removes all visual elements, such as points and labels, from the plot 
            managed by `MyPlotter2`. It effectively resets the visualization to its initial state.
        
            Dependencies:
            - `MyPlotter2` for clearing the plot.
        
            Notes:
            - Ensure that `MyPlotter2` is properly initialized before calling this function.
        
            Returns:
            - None
            """
            
            MyPlotter2.clear()
            
        def update_montage(): #updates the 2D layout of the montage
            """
            Updates the 2D layout of the montage in `MyPlotter2`.
        
            This function clears the existing plot and then updates it based on the current 
            status of buttons and data. It organizes data into two categories based on 
            button status, creates visual representations for each category, and adds them 
            to the plot.
        
            Functionality:
            - Clears the current plot using `MyPlotter2.clear()`.
            - Segregates data points into two groups based on their associated button status:
              - **Green** (active): Data points where `ButtonStatus[i]` is 1.
              - **White** (inactive): Data points where `ButtonStatus[i]` is not 1.
            - Creates `pv.PolyData` objects for each group with associated labels.
            - Adds points and labels to the plot for both categories with specified attributes.
        
            Dependencies:
            - `pv` (assumed to be PyVista or a similar library) for creating `PolyData` objects.
            - `MyPlotter2` for managing and visualizing points and labels.
        
            Notes:
            - Ensure that `self.df`, `self.df2`, and `self.ButtonStatus` are properly defined and 
              contain valid data.
            - The function assumes that `MyPlotter2` is correctly initialized and capable of adding 
              points and labels.
        
            Returns:
            - None
            """

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

            """
            Saves the current state of the montage to files.
         
            This function exports the current data, including the positions of picked points, 
            button statuses, and labels to text files. It saves the coordinates, button statuses, 
            and labels in separate files for future retrieval or analysis.
         
            Functionality:
            - Retrieves and transposes the picked points from `HM_Utils.picked_points`.
            - Removes the first row of the transposed points data.
            - Saves the processed coordinates to "Coordinates_savelfile.txt".
            - Saves the button statuses to "ButtonStatus.txt".
            - Saves the labels to "Labels_savedfile.txt", with each label on a new line.
         
            Dependencies:
            - `HM_Utils` for accessing picked points and labels.
            - `np` (NumPy) for saving coordinate and button status data.
         
            Notes:
            - Ensure that `HM_Utils.picked_points`, `self.ButtonStatus`, and `HM_Utils.Label_sensors` 
              contain valid and up-to-date data.
            - The function assumes that the current directory is writable and accessible.
         
            Returns:
            - None
            """

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

            """
            Adds a new point to the `positionArray` and prints the updated array.
        
            This function appends a new point to the existing `positionArray` by column-stacking it 
            with the current array. The updated `positionArray` is then printed to the console.
        
            Parameters:
            - point (array-like): The point to be added to `positionArray`. It should be a 1D or 2D array 
              with shape compatible for column stacking.
        
            Functionality:
            - Appends the provided point to `self.positionArray` by adding it as a new column.
            - Prints the updated `positionArray` to the console.
        
            Dependencies:
            - `self.positionArray` must be initialized before calling this function.
        
            Notes:
            - Ensure that `self.positionArray` and `point` have compatible shapes for column stacking.
            - The function does not perform any checks on the shape or validity of `point`.
        
            Returns:
            - None
            """

            self.positionArray=np.column_stack((self.positionArray, point))
            print(self.positionArray)
            return

        def callback(mesh, id):

            """
            Callback function to handle point selection and update visualization.
        
            This function is triggered when a point is picked from the mesh. It updates the list of 
            picked points and adds a visual representation of the selected point to the plot.
        
            Parameters:
            - mesh (object): The mesh object from which the point was selected. This parameter is not 
              used directly in the function but is included for compatibility with the callback signature.
            - id (int): The index of the selected point in the `vertices` array.
        
            Functionality:
            - Prints a message indicating that the callback is working, including the mesh and point ID.
            - Retrieves the coordinates of the selected point from `self.vertices` using the provided `id`.
            - Updates the `HM_Utils.picked_points` by appending the selected point.
            - Adds a red sphere to `MyPlotter` at the location of the selected point to visually indicate 
              the selection.
        
            Dependencies:
            - `self.vertices` for accessing the coordinates of the selected point.
            - `HM_Utils` for managing the list of picked points.
            - `MyPlotter` for visualizing the selected point with a sphere.
            - `pv` (assumed to be PyVista or a similar library) for creating the sphere representation.
        
            Notes:
            - Ensure that `self.vertices` and `HM_Utils.picked_points` are properly initialized.
            - The `createArray(self.point)` line is commented out but could be used as an alternative to 
              update `self.positionArray`.
        
            Returns:
            - None
            """
            

            print("code snippet working!", mesh, "   ", id)
            self.point=self.vertices[id]
            print("vertex is", self.point)
            #createArray(self.point) ================================ Can ALSO USE THIS
            HM_Utils.picked_points=np.column_stack((HM_Utils.picked_points,self.point))
            print(HM_Utils.picked_points)
            MyPlotter.add_mesh(pv.Sphere(radius=5, center=self.point),
                           color='red')
             
            
        def on_click(state,selected_button):  #The callback is here ; responsible for toggle

            """
            Handles button click events by updating point labels and button statuses.
        
            This function is called when a button is clicked. It updates the visualization with a label 
            at the location of the selected point and modifies the button status based on the click state.
        
            Parameters:
            - state (bool): The state of the button (e.g., pressed or released). If `True`, the button is 
              in an active state; if `False`, it is in an inactive state.
            - selected_button (str): The label or identifier of the button that was clicked.
        
            Functionality:
            - Prints a message indicating the button click event, including the button label and state.
            - Adds a label to the point in `MyPlotter` with a position slightly offset from the actual point, 
              using the `selected_button` label.
            - Updates `HM_Utils.Label_sensors` by appending the `selected_button` if the button is pressed.
            - Updates the `self.ButtonStatus` array to reflect the active state of the button.
        
            Dependencies:
            - `MyPlotter` for visualizing the label at the point location.
            - `HM_Utils` for managing the list of label sensors.
            - `self.ButtonStatus` for tracking the status of buttons.
            - `self.df` for mapping button labels to indices.
        
            Notes:
            - Ensure that `self.point` is defined and contains the current point coordinates before 
              calling this function.
            - The function assumes that `selected_button` is a valid label present in `self.df`.
        
            Returns:
            - None
            """

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

            """
            Creates a 2D layout of EEG sensors based on a montage file.
        
            This function loads a montage file to retrieve the positions and details of EEG sensors, 
            creates a digmontage for the EEG sensors, and generates a 2D layout of the sensors for 
            visualization. It also adds additional sensor names from `AuxList` to the layout.
        
            Parameters:
            - AuxList (list of str): A list of additional sensor names to be included in the 2D layout.
        
            Returns:
            - pos (numpy.ndarray): A 2D array of sensor positions with additional sensors appended.
            - names (list of str): A list of sensor names with additional sensors appended.
        
            Dependencies:
            - `loadmat` for loading the montage data from a .mat file.
            - `mne` for creating a digmontage and EEG data structure.
            - `pandas` for handling sensor data and names.
        
            Notes:
            - Ensure that the file path `'D:/PhD Data/Affect/Montage/128Ch_Montage_IncludingSpacers.mat'` 
              is accessible and contains the expected format.
            - The function assumes the use of MNE library for EEG processing.
            """

            mon1=loadmat(dirname+'/128Ch_Montage.mat')
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
            
            return pos, names
            
        def sensor_marker():

            """
            Adds a red sphere marker to the plot at the specified point location.
        
            This function creates a red sphere marker at the location specified by the `point` 
            variable and adds it to the plot using the `p` PyVista plotting object.
        
            Dependencies:
            - `p` (assumed to be a PyVista plotting object) for adding the sphere marker.
            - `point` (assumed to be a variable holding the coordinates for the sphere center).
        
            Notes:
            - Ensure that `point` is defined and contains valid coordinates for the sphere's center before 
              calling this function.
            - The sphere radius is set to 3 units, and the color of the sphere is red.
        
            Returns:
            - None
            """

            w = p.add_mesh(pv.Sphere(radius=3, center=point),
                           color='red')
            return
        

#%%
        """
        Initializes the state for the application, sets up the 3D mesh and 2D layout, and prepares data structures.
        
        This initialization block performs the following tasks:
        
        1. **Imports and Initialization**:
           - Sets the initial import status (`self.ImportStatus`) to `0`.
           - Defines a list of auxiliary sensor labels (`AuxList`).
        
        2. **Mesh Loading and Decimation**:
           - Loads a 3D mesh file from a specified path using `pv.read()`.
           - Applies mesh decimation to reduce the complexity of the mesh by 80% using `mesh.decimate(target_reduction=0.8)`.
           - Updates the `mesh` object with the decimated mesh.
           - Extracts the vertices and faces of the mesh and stores them in `self.vertices` and `self.faces`.
        
        3. **Data Preparation**:
           - Initializes `self.positionArray` to an array of zeros and `self.buttonArray` to an empty list.
           - Initializes `self.imported_labels` as an empty list.
           - Calls the `Create2DLayout` function with `AuxList` to generate the 2D layout of sensors. This function returns `temp1` and `temp2`.
           - Converts `temp2` (sensor names/labels) to a NumPy array and assigns it to `self.df`.
           - Initializes `self.ButtonStatus` as a list of zeros with length equal to the number of sensors (based on `self.df`).
        
        4. **Data Adjustment**:
           - Converts `temp1` (sensor positions) to a NumPy array and assigns it to `self.df2`.
           - Adds a column of zeros to `self.df2` for additional data that may be used later.
           - Note: The commented-out lines suggest additional processing or alternative methods for finding projections on a sphere, but they are not currently used.
        
        Dependencies:
        - `pv.read()` for reading the 3D mesh file.
        - `Create2DLayout()` for generating the 2D layout of sensor positions and labels.
        - `numpy` for array manipulations.
        
        Notes:
        - Ensure that the paths to the mesh files and other resources are correct and accessible.
        - The `Create2DLayout` function must be properly defined and functional for this initialization to work as expected.
        - The commented-out code may indicate future enhancements or alternative approaches.
        
        Returns:
        - None
        """
        #-------------------------------------------------------------Imports
        self.ImportStatus=0
        AuxList=['Aux1', 'Aux2', 'Aux3', 'Aux4', 'Aux5', 'Aux6', 'Aux7', 'Aux8', 'Aux9', 'Aux10', 'Aux11', 'Aux12', 'Aux13']

#%%        
        #-------------------------------------------------------------Imports
        self.ImportStatus=0
        AuxList=['Aux1', 'Aux2', 'Aux3', 'Aux4', 'Aux5', 'Aux6', 'Aux7', 'Aux8', 'Aux9', 'Aux10', 'Aux11', 'Aux12', 'Aux13']
        
        mesh = pv.read(dirname+"\data\SampleMesh.stl")
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

        
#%%      
        """
        Sets up the user interface layout and menu actions for the application.
        
        This initialization block performs the following tasks:
        
        1. **UI Layout Setup**:
           - Initializes the main window and sets its title to "Mark3D".
           - Configures the layout using `QHBoxLayout` and `QSplitter` to organize the main window into different sections:
             - `topleft`: A frame positioned at the top-left of the window.
             - `HMframe`: A frame positioned to the right of the `splitter1`, with a minimum height of 512 pixels.
             - `bottomleft`: A frame positioned at the bottom of `splitter1`.
           - `splitter1` splits the window vertically, dividing the top and bottom sections.
           - `splitter2` splits the window horizontally, incorporating `splitter1` and `HMframe`.
           - Sets the main widget layout and geometry for the window, ensuring the correct size and positioning.
        
        2. **Menu Setup**:
           - Creates a main menu bar with two menus: "File" and "View".
           - Adds actions to the "File" menu:
             - **Exit**: Closes the application (shortcut `Ctrl+Q`).
             - **Import file**: Triggers the `import_file` function (shortcut `Ctrl+N`).
             - **Save file**: Triggers the `save_file` function (shortcut `Ctrl+S`).
             - **Import Marked Locations**: Triggers the `import_existing_data` function.
           - Adds actions to the "View" menu:
             - **View Axis**: Triggers the `view_axis` function.
             - **View Layout**: Triggers the `view_montage` function.
             - **Remove Layout**: Triggers the `remove_montage` function.
           - Connects each menu action to its corresponding function.
        
        Dependencies:
        - `PyQt5.QtWidgets` for creating and managing the main window, layouts, and menus.
        - `QSplitter`, `QFrame`, `QWidget`, `QHBoxLayout`, `QAction`, and other PyQt5 components for UI layout and interaction.
        - The functions `import_file`, `save_file`, `import_existing_data`, `view_axis`, `view_montage`, and `remove_montage` must be defined elsewhere in the code.
        
        Notes:
        - Ensure that the `import_file`, `save_file`, `import_existing_data`, `view_axis`, `view_montage`, and `remove_montage` functions are properly implemented and accessible within the class.
        - Adjust the size and positioning parameters as needed for the specific requirements of the application.
        
        Returns:
        - None
        """
  
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
        
        
        
        """
        Adds elements to the user interface layout and configures visualization components.
        
        This block of code performs the following tasks:
        
        1. **UI Element Setup**:
           - **Background Plotter**:
             - Initializes `QtInteractor` for `HMframe` and assigns it to `self.BackgroundPlotter`, with the alias `MyPlotter`.
             - Sets the minimum height and width for `MyPlotter`.
             - Initializes another `QtInteractor` for `bottomleft` and reassigns it to `self.BackgroundPlotter`, with the alias `MyPlotter2`.
           
           - **Button Grid Creation**:
             - Calculates the number of rows and columns required for arranging buttons based on the length of `self.df`.
             - Iterates through rows and columns to create and place buttons on the `topleft` frame:
               - Each button is labeled with an element from `self.df`.
               - Sets geometry and position for each button.
               - Configures buttons to be checkable and connects their click events to the `on_click` function.
               - Adjusts button positioning incrementally to create a grid layout.
        
        2. **Mesh Visualization**:
           - Adds the 3D mesh to `MyPlotter` with white edges and enables point picking with the `callback` function.
        
        Dependencies:
        - `QtInteractor` from the PyQt5 library for interactive 3D plotting.
        - `QPushButton` for creating buttons in the UI.
        - `on_click` and `callback` functions must be defined elsewhere in the code.
        - `self.df` must be populated with appropriate data for button labels.
        - `mesh` must be defined and available for visualization.
        
        Notes:
        - Ensure that `QtInteractor` is properly imported and configured for 3D visualization.
        - Adjust button dimensions, positions, and layout parameters as needed to fit the UI requirements.
        - Verify that `self.df` contains sufficient data to generate the required number of buttons and that `self.df` is appropriately formatted.
        
        Returns:
        - None
        """

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