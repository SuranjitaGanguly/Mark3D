# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 10:53:06 2024

@author: suran
"""

import os.path as op
import os
import cv2
import pytest
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch, call
import math

current_file_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(current_file_path)
grandparent_dir = os.path.dirname(parent_dir)

import numpy as np
import pandas as pd
import pyvista as pv
import numpy.testing as npt
import Mark3D_GUI
from Mark3D_GUI import *


#%% test_import_file
def test_import_file():
    # Mock the external dependencies
    with patch('PyQt5.QtWidgets.QFileDialog') as MockFileDialog, \
         patch('PyQt5.QtWidgets.QApplication') as MockApp, \
         patch('PyVista.read') as MockRead, \
         patch('MyPlotter.clear') as MockClear, \
         patch('MyPlotter.add_mesh') as MockAddMesh, \
         patch('MyPlotter.enable_point_picking') as MockEnablePointPicking, \
         patch('HM_Utils.picked_points', new_callable=MagicMock) as MockPickedPoints, \
         patch('HM_Utils.Label_sensors', new_callable=MagicMock) as MockLabelSensors, \
         patch('update_montage') as MockUpdateMontage:
        
        # Setup the mock objects
        mock_file_dialog = MagicMock()
        mock_file_dialog.exec_ = MagicMock(return_value=QFileDialog.Accepted)
        mock_file_dialog.selectedFiles = MagicMock(return_value=['path/to/mock_file.obj'])
        MockFileDialog.return_value = mock_file_dialog

        mock_mesh = MagicMock()
        mock_mesh.decimate = MagicMock(return_value=mock_mesh)
        mock_mesh.points = 'mock_vertices'
        mock_mesh.faces = 'mock_faces'
        MockRead.return_value = mock_mesh

        # Call the method
        import_file()  # Make sure import_file is in the same scope or import it correctly

        # Check that the methods were called with the correct arguments
        MockClear.assert_called_once()
        MockRead.assert_called_once_with('path/to/mock_file.obj')
        MockAddMesh.assert_called_once()
        MockEnablePointPicking.assert_called_once()
        MockUpdateMontage.assert_called_once()

        # Verify that instance variables are set correctly
        assert hasattr(self, 'vertices')
        assert hasattr(self, 'positionArray')
        assert hasattr(self, 'imported_labels')
        assert hasattr(self, 'ButtonStatus')
        assert self.vertices == 'mock_vertices'
        assert self.positionArray.tolist() == [0, 0, 0]
        assert self.imported_labels == []
        assert self.ButtonStatus == [0] * len(self.df)
        assert HM_Utils.picked_points == []
        assert HM_Utils.Label_sensors == []

#%% test_import_existing_data

def test_import_existing_data():
    # Mock the external dependencies
    with patch('numpy.loadtxt') as MockLoadtxt, \
         patch('builtins.open', new_callable=MagicMock) as MockOpen, \
         patch('MyPlotter.add_mesh') as MockAddMesh, \
         patch('MyPlotter.add_point_labels') as MockAddPointLabels, \
         patch('HM_Utils.picked_points', new_callable=MagicMock) as MockPickedPoints, \
         patch('HM_Utils.Label_sensors', new_callable=MagicMock) as MockLabelSensors, \
         patch('update_montage') as MockUpdateMontage:
        
        # Setup the mock objects
        MockLoadtxt.side_effect = [np.array([[1, 2, 3], [4, 5, 6]]), np.array([0, 1])]
        mock_file = MagicMock()
        mock_file.readlines.return_value = ['label1\n', 'label2\n']
        MockOpen.return_value.__enter__.return_value = mock_file

        # Create an instance of the class that contains import_existing_data
        instance = YourClass()  # Replace YourClass with the actual class name
        instance.ImportStatus = 0  # Set initial ImportStatus

        # Call the method
        instance.import_existing_data()

        # Verify that methods were called with the correct arguments
        MockLoadtxt.assert_any_call("Coordinates_savelfile.txt")
        MockLoadtxt.assert_any_call("ButtonStatus.txt")
        MockOpen.assert_called_once_with("Labels_savedfile.txt", "r")
        MockAddMesh.assert_called()
        MockAddPointLabels.assert_called_once()
        MockUpdateMontage.assert_called_once()

        # Verify instance variables were set correctly
        assert instance.ImportStatus == 1
        assert np.array_equal(instance.ButtonStatus, np.array([0, 1]))
        assert instance.imported_labels == ['label1', 'label2']
        assert np.array_equal(HM_Utils.picked_points, np.array([[0, 0, 0], [1, 2, 3], [4, 5, 6]]))
        assert HM_Utils.Label_sensors == ['label1', 'label2']


#%% test_view_axis

def test_view_axis():
    # Mock the MyPlotter class and its methods
    with patch('MyPlotter.add_axes') as MockAddAxes:
        
        # Create an instance of the class that contains view_axis
        instance = YourClass()  # Replace YourClass with the actual class name

        # Call the method
        instance.view_axis()

        # Verify that MyPlotter.add_axes() was called once
        MockAddAxes.assert_called_once()

#%% test_view_montage

def test_view_montage():
    # Mock the MyPlotter2 class and its methods
    with patch('MyPlotter2.add_points') as MockAddPoints, \
         patch('MyPlotter2.add_point_labels') as MockAddPointLabels:
        
        # Create a mock instance of the class that contains view_montage
        instance = YourClass()  # Replace YourClass with the actual class name
        
        # Setup mock data
        instance.df = [['label1'], ['label2'], ['label3']]  # Example data
        instance.df2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Example data
        
        # Call the method
        instance.view_montage()
        
        # Prepare expected arguments
        expected_points = instance.df2
        expected_labels = ['label1', 'label2', 'label3']
        expected_font_size = 10
        
        # Verify that add_points was called with the correct arguments
        MockAddPoints.assert_called_once_with(
            expected_points,
            show_edges=True,
            color='w',
            point_size=15
        )
        
        # Verify that add_point_labels was called with the correct arguments
        MockAddPointLabels.assert_called_once_with( pv.PolyData(instance.df2),
                                                'My Labels',
                                                font_size=expected_font_size)

#%% test_remove_montage

def test_remove_montage():
    # Mock the MyPlotter2 class and its methods
    with patch('MyPlotter2.clear') as MockClear:
        
        # Create a mock instance of the class that contains remove_montage
        instance = YourClass()  # Replace YourClass with the actual class name
        
        # Call the method
        instance.remove_montage()
        
        # Verify that clear was called exactly once
        MockClear.assert_called_once()



#%%  test_update_montage

def test_update_montage():
    # Create mocks for MyPlotter2 methods
    with patch('MyPlotter2.clear') as mock_clear, \
         patch('MyPlotter2.add_points') as mock_add_points, \
         patch('MyPlotter2.add_point_labels') as mock_add_point_labels:

        # Create mock instance of the class containing update_montage
        instance = YourClass()  # Replace YourClass with the actual class name
        
        # Set up instance attributes for the test
        instance.df = [['test1'], ['test2']]  # Replace with appropriate test data
        instance.df2 = np.array([[1, 2], [3, 4], [5, 6]])  # Replace with appropriate test data
        instance.ButtonStatus = [1, 0]  # Example statuses
        
        # Call the method
        instance.update_montage()
        
        # Verify clear was called once
        mock_clear.assert_called_once()
        
        # Check add_points calls
        assert mock_add_points.call_count == 2
        # Verify that add_points was called with expected arguments
        mock_add_points.assert_any_call(np.asarray([[1, 3, 5], [2, 4, 6]]), show_edges=True, color='red', point_size=15)
        mock_add_points.assert_any_call(np.asarray([[1, 2], [3, 4]]), show_edges=True, point_size=15)
        
        # Check add_point_labels calls
        assert mock_add_point_labels.call_count == 2
        # Verify that add_point_labels was called with expected arguments
        mock_add_point_labels.assert_any_call(pv.PolyData([[1, 3, 5], [2, 4, 6]]), "My Labels", point_size=2, font_size=10)
        mock_add_point_labels.assert_any_call(pv.PolyData([[1, 2], [3, 4]]), "My Labels", point_size=10, font_size=10)


#%% test_save_file

def test_save_file():
    # Create mock for HM_Utils and its attributes
    with patch('HM_Utils.picked_points', new=MagicMock()) as mock_picked_points, \
         patch('HM_Utils.Label_sensors', new=MagicMock()) as mock_label_sensors:
        
        # Set up mock data
        mock_picked_points = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        mock_label_sensors = ["label1", "label2", "label3"]
        
        # Create a mock instance of the class containing save_file
        instance = YourClass()  # Replace YourClass with the actual class name
        
        # Set up instance attributes for the test
        instance.ButtonStatus = [1, 0, 1]  # Example ButtonStatus
        
        # Call the method
        instance.save_file()
        
        # Verify file creation and content
        assert os.path.isfile("Coordinates_savelfile.txt")
        assert os.path.isfile("ButtonStatus.txt")
        assert os.path.isfile("Labels_savedfile.txt")
        
        # Check the content of Coordinates_savelfile.txt
        expected_coords = np.array([[1, 4, 7], [2, 5, 8]])
        actual_coords = np.loadtxt("Coordinates_savelfile.txt")
        np.testing.assert_array_equal(expected_coords, actual_coords)
        
        # Check the content of ButtonStatus.txt
        expected_status = [1, 0, 1]
        actual_status = np.loadtxt("ButtonStatus.txt").astype(int).tolist()
        assert expected_status == actual_status
        
        # Check the content of Labels_savedfile.txt
        with open("Labels_savedfile.txt", "r") as file:
            actual_labels = [line.strip() for line in file.readlines()]
        assert mock_label_sensors == actual_labels

        # Clean up files after test
        os.remove("Coordinates_savelfile.txt")
        os.remove("ButtonStatus.txt")
        os.remove("Labels_savedfile.txt")


#%% test_createArray

def test_createArray():
    # Create an instance of the class containing the method
    instance = YourClass()  # Replace YourClass with the actual class name
    
    # Initial setup
    instance.positionArray = np.array([[0, 0, 0]])  # Assuming this is the initial state
    
    # Define a point to add
    point = np.array([1, 2, 3])
    
    # Call the method
    instance.createArray(point)
    
    # Expected result after adding the point
    expected_array = np.array([[0, 0, 0, 1],
                               [0, 0, 0, 2],
                               [0, 0, 0, 3]])
    
    # Check the result
    np.testing.assert_array_equal(instance.positionArray, expected_array)

    # Test with a new point
    new_point = np.array([4, 5, 6])
    instance.createArray(new_point)
    
    # Expected result after adding another point
    expected_array_after_second = np.array([[0, 0, 0, 1, 4],
                                           [0, 0, 0, 2, 5],
                                           [0, 0, 0, 3, 6]])
    
    # Check the result
    np.testing.assert_array_equal(instance.positionArray, expected_array_after_second)


#%% test_callback

def test_callback():
    # Setup mock objects
    with patch('HM_Utils.picked_points', new_callable=MagicMock) as mock_picked_points:
        with patch('MyPlotter.add_mesh') as mock_add_mesh:
            # Initialize the mocked data
            HM_Utils.picked_points = np.array([[0, 0, 0]])
            
            # Define test inputs
            mesh = MagicMock()
            id = 1  # Index for the vertices array
            
            # Call the function
            callback(mesh, id)
            
            # Expected result
            expected_picked_points = np.array([[0, 0, 0], [1, 1, 1]])
            
            # Check if HM_Utils.picked_points was updated correctly
            np.testing.assert_array_equal(HM_Utils.picked_points, expected_picked_points)
            
            # Check if MyPlotter.add_mesh was called with the correct parameters
            mock_add_mesh.assert_called_once_with(pv.Sphere(radius=5, center=[1, 1, 1]), color='red')

#%% test_on_click
def test_on_click():
    # Setup mock objects
    with patch('MyPlotter.add_point_labels') as mock_add_point_labels:
        with patch('MyPlotter.add_mesh') as mock_add_mesh:
            with patch('update_montage') as mock_update_montage:
                # Initialize the mocked data
                HM_Utils.picked_points = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
                HM_Utils.Label_sensors = ['label1', 'label2', 'label3']
                self = MagicMock()
                self.point = np.array([1, 1, 1])
                self.df = ['label1', 'label2', 'label3']
                self.ButtonStatus = [0, 0, 0]

                # Call the function
                on_click(False, 'label2')
                
                # Expected changes
                expected_picked_points = np.array([[0, 0, 0], [1, 1, 1]])
                expected_label_sensors = ['label1', 'label3']
                
                # Check if `add_point_labels` was called correctly
                mock_add_point_labels.assert_called_once_with(np.add(self.point, [0.7, 0.7, 0.7]), ['label2'], point_size=10, font_size=20, text_color='red')
                
                # Check if `add_mesh` was called correctly
                mock_add_mesh.assert_called_once_with(pv.Sphere(radius=5, center=[1, 1, 1]), color='yellow')
                
                # Check if `update_montage` was called
                mock_update_montage.assert_called_once()

                # Check if `HM_Utils` was updated correctly
                np.testing.assert_array_equal(HM_Utils.picked_points, expected_picked_points)
                assert HM_Utils.Label_sensors == expected_label_sensors

#%% test_Create2DLayout

@patch('mne.channels.make_dig_montage')
@patch('mne.create_info')
@patch('mne.io.RawArray')
@patch('mne.channels.make_eeg_layout')
@patch('scipy.io.loadmat')
def test_Create2DLayout(mock_loadmat, mock_make_eeg_layout, mock_RawArray, mock_create_info, mock_make_dig_montage):
    # Mocking the `loadmat` return value
    mock_loadmat.return_value = {
        'Mon': {
            'xposition': np.array([[1, 2, 3]]),
            'yposition': np.array([[4, 5, 6]]),
            'zposition': np.array([[7, 8, 9]]),
            'electrodename': np.array([['e1', 'e2', 'e3']]),
            'electrodenumber': np.array([[1, 2, 3]]),
            'gridxposition': np.array([[10, 11, 12]]),
            'gridyposition': np.array([[13, 14, 15]]),
            'gridzposition': np.array([[16, 17, 18]])
        }
    }

    # Mocking `make_dig_montage`
    mock_make_dig_montage.return_value = MagicMock()

    # Mocking `create_info`
    mock_create_info.return_value = MagicMock()

    # Mocking `RawArray`
    mock_RawArray.return_value = MagicMock()

    # Mocking `make_eeg_layout`
    mock_make_eeg_layout.return_value = MagicMock(
        pos=np.array([[1, 2], [3, 4], [5, 6]]),
        names=['e1', 'e2', 'e3']
    )

    AuxList = ['aux1', 'aux2']
    pos, names = Create2DLayout(AuxList)

    # Define expected results
    expected_pos = np.array([
        [1, 2],
        [3, 4],
        [5, 6],
        [0, 0],  # Simulated auxiliary positions
        [0, 0],
        [0, 0]
    ])
    expected_names = ['e1', 'e2', 'e3', 'Nasion', 'LPA', 'RPA', 'aux1', 'aux2']

    # Assertions
    np.testing.assert_array_equal(pos, expected_pos)
    assert names == expected_names

    # Verify that mocks were called as expected
    mock_loadmat.assert_called_once_with('D:/PhD Data/Affect/Montage/128Ch_Montage_IncludingSpacers.mat')
    mock_make_dig_montage.assert_called_once()
    mock_create_info.assert_called_once()
    mock_RawArray.assert_called_once()
    mock_make_eeg_layout.assert_called_once()


#%% test_sensor_marker
def test_sensor_marker():
    # Mock the Sphere class from pyvista
    with patch('pyvista.Sphere') as mock_sphere:
        # Mock the `p` object
        with patch('your_module.p') as mock_p:
            # Create a mock object for `p` with `add_mesh` method
            mock_p = MagicMock()
            # Set `p` to the mocked object
            p = mock_p

            # Define a test point
            test_point = [1, 2, 3]
            
            # Call the function
            sensor_marker(test_point)
            
            # Check if Sphere was called with the correct parameters
            mock_sphere.assert_called_once_with(radius=3, center=test_point)
            
            # Verify that add_mesh was called with the right arguments
            mock_p.add_mesh.assert_called_once_with(mock_sphere.return_value, color='red')

#%%



























