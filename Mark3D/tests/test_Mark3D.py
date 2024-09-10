# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:48:01 2024

@author: suranjita
"""

import os.path as op
import os
import cv2
import pytest
from pathlib import Path
import unittest
from unittest.mock import patch, call
import math


# Get the absolute path of the current script
current_file_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(current_file_path)
grandparent_dir = os.path.dirname(parent_dir)

os.chdir(grandparent_dir)
import numpy as np
import pandas as pd
import numpy.testing as npt
import Mark3D
from Mark3D import *#SilentMkdir, VideoToFrames, BlurDetection, FinalFrames


#%% test_video_to_frames

@pytest.fixture
def setup_test_environment():
    """
    Fixture to set up and tear down the test environment.
    Creates a temporary directory structure and a sample video file.
    """
    # Define paths
    base_dir = 'test_data'  
    video_path = os.path.join(base_dir, 'VID.mp4')
    output_dir = os.path.join(base_dir, 'VideoReconImg')
    
    # Create test directories
    os.makedirs(base_dir, exist_ok=True)
    SilentMkdir(output_dir)
    
    # Create a sample video with a single frame
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_path, fourcc, 1.0, (100, 100))
    frame = cv2.imread('test_image.png')  # Create or load a sample image
    video_writer.write(frame)
    video_writer.release()
    
    yield base_dir, output_dir
    
    # Clean up test directories and files
    for file in Path(base_dir).rglob('*'):
        file.unlink()
    os.rmdir(base_dir)

def test_video_to_frames(setup_test_environment):
    base_dir, output_dir = setup_test_environment
    sub = 'test_subject'

    # Adjust paths for the function call
    test_video_path = os.path.join(base_dir, 'VID.mp4')
    
    # Call the function to be tested
    VideoToFrames(sub)

    # Check if the directory exists
    assert os.path.isdir(output_dir), "Output directory was not created"

    # Check if the frame image file was created
    frame_files = list(Path(output_dir).glob('*.jpg'))
    assert len(frame_files) > 0, "No frame images were created"

    # Optionally, check the properties of the created frame images
    for frame_file in frame_files:
        img = cv2.imread(str(frame_file))
        assert img is not None, f"Image {frame_file} could not be read"
        assert img.shape == (100, 100, 3), f"Image {frame_file} has incorrect dimensions"

#%% test_blur_detection.py

@pytest.fixture
def setup_test_environment():
    """
    Fixture to set up and tear down the test environment.
    Creates a temporary directory structure and sample images (both blurry and sharp).
    """
    base_dir = 'test_data'
    video_recon_img_dir = os.path.join(base_dir, 'VideoReconImg')
    
    # Create test directory
    os.makedirs(video_recon_img_dir, exist_ok=True)
    
    # Create sample images
    sharp_image_path = os.path.join(video_recon_img_dir, 'sharp_image.jpg')
    blurry_image_path = os.path.join(video_recon_img_dir, 'blurry_image.jpg')

    # Create a sharp image (solid color for simplicity)
    sharp_img = np.full((100, 100, 3), 255, dtype=np.uint8)
    cv2.imwrite(sharp_image_path, sharp_img)
    
    # Create a blurry image (use Gaussian blur)
    blurry_img = cv2.GaussianBlur(sharp_img, (15, 15), 0)
    cv2.imwrite(blurry_image_path, blurry_img)
    
    yield base_dir, video_recon_img_dir
    
    # Clean up test directories and files
    for file in Path(base_dir).rglob('*'):
        file.unlink()
    os.rmdir(base_dir)

def test_blur_detection(setup_test_environment):
    base_dir, video_recon_img_dir = setup_test_environment
    sub = 'test_subject'
    
    # Adjust paths for the function call
    test_image_dir = video_recon_img_dir

    # Call the function to be tested
    BlurDetection(sub)

    # Check if the blurry image has been removed
    remaining_files = list(Path(video_recon_img_dir).glob('*.jpg'))
    assert len(remaining_files) == 1, "Blurry image was not removed"
    
    # Check if the remaining image is the sharp one
    remaining_file_names = [f.name for f in remaining_files]
    assert 'sharp_image.jpg' in remaining_file_names, "Sharp image was removed or not found"


#%% Final Frames

@pytest.fixture
def setup_directories_and_files(tmp_path):
    # Create source directory
    source_dir = tmp_path / "VideoReconImg"
    source_dir.mkdir()

    # Create destination directory (will be created by FinalFrames)
    dest_dir = tmp_path / "VideoReconImg_1"

    # Create sample images in the source directory
    for i in range(10):
        file_path = source_dir / f"image_{i}.jpg"
        img = np.zeros((100, 100, 3), dtype=np.uint8)  # Create a dummy image
        cv2.imwrite(str(file_path), img)

    return {
        "source_dir": source_dir,
        "dest_dir": dest_dir,
        "tmp_path": tmp_path,
    }

def test_final_frames(setup_directories_and_files):
    dirs = setup_directories_and_files
    source_dir = dirs["source_dir"]
    dest_dir = dirs["dest_dir"]

    # Run FinalFrames function
    FinalFrames(source_dir.name)

    # Check if destination directory exists
    assert dest_dir.exists(), "Destination directory was not created"

    # Check if the correct number of files are copied
    source_files = sorted(f for f in source_dir.glob("*.jpg"))
    dest_files = sorted(f for f in dest_dir.glob("*.jpg"))
    
    # Assuming 'count' is set to 1 in FinalFrames
    expected_files = [f'image_{i}.jpg' for i in range(0, len(source_files))]
    assert sorted(f.name for f in dest_files) == expected_files, "Files in destination directory are incorrect"

    # Check if source directory is deleted
    assert not source_dir.exists(), "Source directory was not deleted"


#%% test_run_1_cameraInit()

def test_run_1_cameraInit():
    """
    Function to test the `run_1_cameraInit` function.
    """
    
    binPath = "C:\\Program Files\\AliceVision"
    baseDir = "C:\\Data\\Project"
    imgDir = "C:\\Data\\Project\\Images"
    verboseLevel = "info"

    # Define a mock for SilentMkdir and os.system
    with patch("os.system") as mock_os_system, patch("builtins.print") as mock_print, patch("SilentMkdir") as mock_mkdir:
        # Arrange
        mock_os_system.return_value = 0  # Simulate successful execution of os.system
        
        # Call the function
        result = run_1_cameraInit(binPath, baseDir, imgDir)

        # Check SilentMkdir call
        mock_mkdir.assert_called_once_with(baseDir + "/1_CameraInit")
        
        # Construct the expected command line
        expected_cmd = (
            binPath + "\\aliceVision_cameraInit.exe"
            + " --imageFolder \"C:\\Data\\Project\\Images\""
            + " --sensorDatabase \"C:\\Program Files\\AliceVision\\share\\aliceVision\\cameraSensors.db\""
            + " --output \"C:\\Data\\Project/1_CameraInit/cameraInit.sfm\""
            + " --defaultFieldOfView 45 --allowSingleView 1 --verboseLevel " + verboseLevel
        )

        # Check the call to os.system
        mock_os_system.assert_called_once_with(expected_cmd)
        
        # Validate the result
        assert result == 0, "Expected result to be 0 for successful execution"

    print("All tests passed!")

#%% test_run_2_featureExtraction()
def test_run_2_featureExtraction():
    """
    Function to test the `run_2_featureExtraction` function.
    """

    binPath = "C:\\Program Files\\AliceVision"
    baseDir = "C:\\Data\\Project"
    numberOfImages = 100
    imagesPerGroup = 40

    with patch("os.system") as mock_os_system, patch("SilentMkdir") as mock_mkdir, patch("builtins.print") as mock_print:
        # Arrange
        mock_os_system.return_value = 0  # Simulate successful execution of os.system

        # Call the function
        run_2_featureExtraction(binPath, baseDir, numberOfImages, imagesPerGroup)

        # Check SilentMkdir call
        mock_mkdir.assert_called_once_with(baseDir + "/2_FeatureExtraction")

        # Expected commands
        cmdLine_base = (
            binPath + "\\aliceVision_featureExtraction"
            + " --input \"C:\\Data\\Project/1_CameraInit/cameraInit.sfm\""
            + " --output \"C:\\Data\\Project/2_FeatureExtraction\""
            + " --forceCpuExtraction 1"
        )

        # Verify the correct number of groups and commands are called
        numberOfGroups = math.ceil(numberOfImages / imagesPerGroup)
        expected_calls = []

        for i in range(numberOfGroups):
            group_cmd = cmdLine_base + " --rangeStart {} --rangeSize {} ".format(i * imagesPerGroup, imagesPerGroup)
            expected_calls.append(call(group_cmd))
        
        mock_os_system.assert_has_calls(expected_calls, any_order=False)

        # Check print statements
        mock_print.assert_any_call("----------------------- 2/13 FEATURE EXTRACTION -----------------------")
        for i in range(numberOfGroups):
            mock_print.assert_any_call("------- group {} / {} --------".format(i+1, numberOfGroups))

    print("All tests passed!")

#%% test_run_3_imageMatching()

def test_run_3_imageMatching():
    """
    Function to test the `run_3_imageMatching` function.
    """

    binPath = "C:\\Program Files\\AliceVision"
    baseDir = "C:\\Data\\Project"
    verboseLevel = "info"  # Assuming `verboseLevel` is set globally

    # Mock external functions
    with patch("os.system") as mock_os_system, patch("SilentMkdir") as mock_mkdir, patch("builtins.print") as mock_print:
        # Arrange
        mock_os_system.return_value = 0  # Simulate successful execution of os.system

        # Call the function
        run_3_imageMatching(binPath, baseDir)

        # Verify SilentMkdir was called with the correct path
        mock_mkdir.assert_called_once_with(baseDir + "/3_ImageMatching")

        # Construct the expected command line
        expected_cmd = (
            binPath + "\\aliceVision_imageMatching.exe"
            + " --input \"C:\\Data\\Project/1_CameraInit/cameraInit.sfm\""
            + " --featuresFolders \"C:\\Data\\Project/2_FeatureExtraction\""
            + " --output \"C:\\Data\\Project/3_ImageMatching/imageMatches.txt\""
            + " --tree \"" + str(Path(binPath).parent) + "/share/aliceVision/vlfeat_K80L3.SIFT.tree\""
            + " --verboseLevel " + verboseLevel
        )

        # Check if the os.system call was made with the correct command
        mock_os_system.assert_called_once_with(expected_cmd)

        # Validate print statements
        mock_print.assert_any_call("----------------------- 3/13 IMAGE MATCHING -----------------------")
        mock_print.assert_any_call(expected_cmd)

    print("All tests passed!")

#%%  test_run_4_featureMatching()

def test_run_4_featureMatching():
    """
    Function to test the `run_4_featureMatching` function.
    """

    binPath = "C:\\Program Files\\AliceVision"
    baseDir = "C:\\Data\\Project"
    numberOfImages = 100
    imagesPerGroup = 20
    verboseLevel = "info"  # Assuming `verboseLevel` is set globally

    # Mock external functions
    with patch("os.system") as mock_os_system, patch("SilentMkdir") as mock_mkdir, patch("builtins.print") as mock_print:
        # Arrange
        mock_os_system.return_value = 0  # Simulate successful execution of os.system

        # Call the function
        run_4_featureMatching(binPath, baseDir, numberOfImages, imagesPerGroup)

        # Check SilentMkdir call
        mock_mkdir.assert_called_once_with(baseDir + "/4_featureMatching")

        # Construct the base command line
        expected_cmd_base = (
            binPath + "\\aliceVision_featureMatching.exe"
            + " --input \"C:\\Data\\Project/1_CameraInit/cameraInit.sfm\""
            + " --featuresFolders \"C:\\Data\\Project/2_FeatureExtraction\""
            + " --output \"C:\\Data\\Project/4_featureMatching\""
            + " --imagePairsList \"C:\\Data\\Project/3_ImageMatching/imageMatches.txt\""
            + " --knownPosesGeometricErrorMax 5"
            + " --verboseLevel " + verboseLevel
            + " --describerTypes sift --photometricMatchingMethod ANN_L2 --geometricEstimator acransac"
            + " --geometricFilterType fundamental_matrix --distanceRatio 0.8"
            + " --maxIteration 2048 --geometricError 0.0 --maxMatches 0"
            + " --savePutativeMatches False --guidedMatching False"
            + " --matchFromKnownCameraPoses False --exportDebugFiles True"
        )

        # Calculate the number of groups
        numberOfGroups = math.ceil(numberOfImages / imagesPerGroup)

        # Verify the correct number of groups and commands are called
        expected_calls = []

        for i in range(numberOfGroups):
            group_cmd = expected_cmd_base + " --rangeStart {} --rangeSize {} ".format(i * imagesPerGroup, imagesPerGroup)
            expected_calls.append(call(group_cmd))
        
        mock_os_system.assert_has_calls(expected_calls, any_order=False)

        # Check print statements
        mock_print.assert_any_call("----------------------- 4/13 FEATURE MATCHING -----------------------")
        for i in range(numberOfGroups):
            mock_print.assert_any_call("------- group {} / {} --------".format(i, numberOfGroups))

    print("All tests passed!")

#%% test_run_5_structureFromMotion()

def test_run_5_structureFromMotion():
    """
    Function to test the `run_5_structureFromMotion` function.
    """
    
    binPath = "C:\\Program Files\\AliceVision"
    baseDir = "C:\\Data\\Project"
    verboseLevel = "info"  # Assuming `verboseLevel` is set globally

    # Mock external functions
    with patch("os.system") as mock_os_system, patch("SilentMkdir") as mock_mkdir, patch("builtins.print") as mock_print:
        # Arrange
        mock_os_system.return_value = 0  # Simulate successful execution of os.system

        # Call the function
        run_5_structureFromMotion(binPath, baseDir)

        # Check SilentMkdir call
        mock_mkdir.assert_called_once_with(baseDir + "/5_structureFromMotion")

        # Construct the expected command line
        expected_cmd = (
            binPath + "\\aliceVision_incrementalSfm.exe"
            + " --input \"C:\\Data\\Project/1_CameraInit/cameraInit.sfm\""
            + " --output \"C:\\Data\\Project/5_structureFromMotion/sfm.abc\" "
            + " --outputViewsAndPoses \"C:\\Data\\Project/5_structureFromMotion/cameras.sfm\""
            + " --extraInfoFolder \"C:\\Data\\Project/5_structureFromMotion\""
            + " --featuresFolders \"C:\\Data\\Project/2_FeatureExtraction\""
            + " --matchesFolders \"C:\\Data\\Project/4_featureMatching\""
            + " --verboseLevel " + verboseLevel
        )

        # Verify that os.system was called with the expected command
        mock_os_system.assert_called_once_with(expected_cmd)

        # Check print statements
        mock_print.assert_any_call("----------------------- 5/13 STRUCTURE FROM MOTION -----------------------")
        mock_print.assert_any_call(expected_cmd)

    print("All tests passed!")

#%% test_run_6_prepareDenseScene()

def test_run_6_prepareDenseScene():
    """
    Function to test the `run_6_prepareDenseScene` function.
    """
    
    binPath = "C:\\Program Files\\AliceVision"
    baseDir = "C:\\Data\\Project"
    verboseLevel = "info"  # Assuming `verboseLevel` is set globally

    # Mock external functions
    with patch("os.system") as mock_os_system, patch("SilentMkdir") as mock_mkdir, patch("builtins.print") as mock_print:
        # Arrange
        mock_os_system.return_value = 0  # Simulate successful execution of os.system

        # Call the function
        run_6_prepareDenseScene(binPath, baseDir)

        # Check SilentMkdir call
        mock_mkdir.assert_called_once_with(baseDir + "/6_PrepareDenseScene")

        # Construct the expected command line
        expected_cmd = (
            binPath + "\\aliceVision_prepareDenseScene.exe"
            + " --input \"C:\\Data\\Project/5_structureFromMotion/sfm.abc\""
            + " --output \"C:\\Data\\Project/6_PrepareDenseScene\" "
            + " --verboseLevel " + verboseLevel
        )

        # Verify that os.system was called with the expected command
        mock_os_system.assert_called_once_with(expected_cmd)

        # Check print statements
        mock_print.assert_any_call("----------------------- 6/13 PREPARE DENSE SCENE -----------------------")
        mock_print.assert_any_call(expected_cmd)

    print("All tests passed!")

#%%  test_run_7_depthMap()

def test_run_7_depthMap():
    binPath = "C:\\Program Files\\AliceVision"
    baseDir = "C:\\Data\\Project"
    verboseLevel = "1"  # Define a value for verboseLevel

    @patch('os.system')  # Mock os.system to avoid executing the actual command
    @patch('builtins.print')  # Mock print to capture printed output
    def run_tests(mock_print, mock_os_system):
        # Test case 1: Single batch
        numberOfImages = 15
        groupSize = 20
        downscale = 1
        run_7_depthMap(binPath, baseDir, numberOfImages, groupSize, downscale)

        expected_cmdLine = (f"{binPath}\\aliceVision_depthMapEstimation.exe "
                            f"--input \"{baseDir}/5_structureFromMotion/sfm.abc\" "
                            f"--output \"{baseDir}/7_DepthMap\" "
                            f"--imagesFolder \"{baseDir}/6_PrepareDenseScene\" "
                            f"--verboseLevel {verboseLevel} "
                            f"--downscale {downscale}")

        # Check that os.system was called with the correct command
        mock_os_system.assert_called_once_with(expected_cmdLine)

        # Reset mock for next test case
        mock_os_system.reset_mock()
        mock_print.reset_mock()

        # Test case 2: Multiple batches
        numberOfImages = 50
        groupSize = 20
        run_7_depthMap(binPath, baseDir, numberOfImages, groupSize, downscale)

        numberOfBatches = math.ceil(numberOfImages / groupSize)
        expected_cmdLine = (f"{binPath}\\aliceVision_depthMapEstimation.exe "
                            f"--input \"{baseDir}/5_structureFromMotion/sfm.abc\" "
                            f"--output \"{baseDir}/7_DepthMap\" "
                            f"--imagesFolder \"{baseDir}/6_PrepareDenseScene\" "
                            f"--verboseLevel {verboseLevel} "
                            f"--downscale {downscale}")

        # Check that os.system was called the correct number of times
        assert mock_os_system.call_count == numberOfBatches

        # Check the individual calls to os.system
        expected_calls = [call(f"{expected_cmdLine} --rangeStart {i * groupSize} --rangeSize {groupSize}") 
                          for i in range(numberOfBatches)]
        mock_os_system.assert_has_calls(expected_calls)

        # Reset mock for next test case
        mock_os_system.reset_mock()
        mock_print.reset_mock()

        # Test case 3: Downscale factor
        numberOfImages = 30
        groupSize = 15
        downscale = 2
        run_7_depthMap(binPath, baseDir, numberOfImages, groupSize, downscale)

        expected_cmdLine = (f"{binPath}\\aliceVision_depthMapEstimation.exe "
                            f"--input \"{baseDir}/5_structureFromMotion/sfm.abc\" "
                            f"--output \"{baseDir}/7_DepthMap\" "
                            f"--imagesFolder \"{baseDir}/6_PrepareDenseScene\" "
                            f"--verboseLevel {verboseLevel} "
                            f"--downscale {downscale}")

        # Check that os.system was called with the correct command
        mock_os_system.assert_called_once_with(expected_cmdLine)

    run_tests()

#%% test_run_8_depthMapFilter()

def test_run_8_depthMapFilter():
    binPath = "C:\\Program Files\\AliceVision"
    baseDir = "C:\\Data\\Project"
    verboseLevel = "1"  # Define a value for verboseLevel

    @patch('os.system')  # Mock os.system to avoid executing the actual command
    @patch('builtins.print')  # Mock print to capture printed output
    @patch('path.to.your.module.SilentMkdir')  # Mock SilentMkdir if it's defined elsewhere
    def run_tests(mock_silent_mkdir, mock_print, mock_os_system):
        # Define the expected command line
        expected_cmdLine = (f"{binPath}\\aliceVision_depthMapFiltering.exe "
                            f"--input \"{baseDir}/5_structureFromMotion/sfm.abc\" "
                            f"--output \"{baseDir}/8_DepthMapFilter\" "
                            f"--depthMapsFolder \"{baseDir}/7_DepthMap\" "
                            f"--verboseLevel {verboseLevel}")

        # Call the function
        run_8_depthMapFilter(binPath, baseDir)

        # Check that os.system was called with the correct command
        mock_os_system.assert_called_once_with(expected_cmdLine)
        # Check that print was called to output the command
        mock_print.assert_called_once_with(expected_cmdLine)
        # Check that SilentMkdir was called to create the directory
        mock_silent_mkdir.assert_called_once_with(baseDir + "/8_DepthMapFilter")

    run_tests()


#%% test_run_9_meshing

def test_run_9_meshing():
    binPath = "C:\\Program Files\\AliceVision"
    baseDir = "C:\\Data\\Project"
    maxInputPoints = 10000000
    maxPoints = 500000
    verboseLevel = "1"  # Define a value for verboseLevel

    @patch('os.system')  # Mock os.system to avoid executing the actual command
    @patch('builtins.print')  # Mock print to capture printed output
    @patch('path.to.your.module.SilentMkdir')  # Mock SilentMkdir if it's defined elsewhere
    def run_tests(mock_silent_mkdir, mock_print, mock_os_system):
        # Define the expected command line
        expected_cmdLine = (f"{binPath}\\aliceVision_meshing.exe "
                            f"--input \"{baseDir}/5_structureFromMotion/sfm.abc\" "
                            f"--output \"{baseDir}/9_Meshing/densePointCloud.abc\" "
                            f"--outputMesh \"{baseDir}/9_Meshing/mesh.obj\" "
                            f"--depthMapsFolder \"{baseDir}/8_DepthMapFilter\" "
                            f"--maxInputPoints {maxInputPoints} "
                            f"--maxPoints {maxPoints} "
                            f"--verboseLevel {verboseLevel}")

        # Call the function
        run_9_meshing(binPath, baseDir, maxInputPoints, maxPoints)

        # Check that os.system was called with the correct command
        mock_os_system.assert_called_once_with(expected_cmdLine)
        # Check that print was called to output the command
        mock_print.assert_called_once_with(expected_cmdLine)
        # Check that SilentMkdir was called to create the directory
        mock_silent_mkdir.assert_called_once_with(baseDir + "/9_Meshing")

    run_tests()

#%% test_run_10_meshFiltering()

def test_run_10_meshFiltering():
    binPath = "C:\\Program Files\\AliceVision"
    baseDir = "C:\\Data\\Project"
    keepLargestMeshOnly = "True"
    verboseLevel = "1"  # Define a value for verboseLevel

    @patch('os.system')  # Mock os.system to avoid executing the actual command
    @patch('builtins.print')  # Mock print to capture printed output
    @patch('path.to.your.module.SilentMkdir')  # Mock SilentMkdir if it's defined elsewhere
    def run_tests(mock_silent_mkdir, mock_print, mock_os_system):
        # Define the expected command line
        expected_cmdLine = (f"{binPath}\\aliceVision_meshFiltering.exe "
                            f"--inputMesh \"{baseDir}/9_Meshing/mesh.obj\" "
                            f"--outputMesh \"{baseDir}/10_MeshFiltering/mesh.obj\" "
                            f"--verboseLevel {verboseLevel} "
                            f"--keepLargestMeshOnly {keepLargestMeshOnly}")

        # Call the function
        run_10_meshFiltering(binPath, baseDir, keepLargestMeshOnly)

        # Check that os.system was called with the correct command
        mock_os_system.assert_called_once_with(expected_cmdLine)
        # Check that print was called to output the command
        mock_print.assert_called_once_with(expected_cmdLine)
        # Check that SilentMkdir was called to create the directory
        mock_silent_mkdir.assert_called_once_with(baseDir + "/10_MeshFiltering")

    run_tests()

