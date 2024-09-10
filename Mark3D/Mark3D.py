# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 20:41:51 2024

@author: suranjita
"""

import sys
import os , os.path
import shutil
import math
import time
from pathlib import Path
import cv2
import numpy as np

dirname = os.path.dirname(os.path.abspath(__file__))  # Absolute path of this file

verboseLevel = "\"" + "error" + "\""  


def SilentMkdir(theDir):    # function to create a directory
    """
    Creates a directory if it does not already exist.

    This function attempts to create a directory at the specified path. If the directory already exists or an error occurs during 
    the directory creation (e.g., permission issues), the function will silently pass without raising any exceptions. 

    Args:
        theDir (str): The path of the directory to be created.

    Returns:
        int: Always returns 0 indicating that the function has completed.

    Raises:
        OSError: If there is an issue with directory creation that cannot be ignored (though in this function, exceptions are caught and ignored).

    Example:
        SilentMkdir("C:\\Data\\NewFolder")
    
    Notes:
        - The function uses `os.mkdir` to create a single directory. It does not create intermediate directories if they do not exist.
        - If you need to create intermediate directories, consider using `os.makedirs` with the `exist_ok` parameter set to `True`.
    """
    
    try:
        os.mkdir(theDir)
    except:
        pass
    return 0


def VideoToFrames(Sub):
    """
    Converts a video file into individual frames and saves them as image files.

    This function reads a video file located at "../Data/<Sub>/VID.mp4", where `<Sub>` is a 
    parameter representing a specific subject or identifier. It extracts frames from the video 
    and saves each frame as a JPEG image in the directory "../Data/<Sub>/VideoReconImg/".

    The function performs the following steps:
    1. Creates the output directory if it doesn't already exist.
    2. Opens the video file and reads frames sequentially.
    3. Saves each frame as a JPEG image with filenames corresponding to their frame numbers.
    4. Releases the video capture object and destroys any OpenCV windows after processing is complete.

    Args:
        Sub (str): The subject or identifier used to construct the file paths for input video 
                   and output image directory.

    Returns:
        None

    Raises:
        None

    Example:
        VideoToFrames("Subject1")

    Notes:
        - Requires the OpenCV library (`cv2`).
        - Assumes that the directory structure and video file naming conventions are followed.
    """


    print ("VIDEO TO FRAMES")
<<<<<<< HEAD
    DataPath=dirname+"/Data/"+Sub+"/VID.mp4"
    SilentMkdir(dirname+"/Data/"+Sub+"/VideoReconImg/")
=======
    DataPath="../"+"Data/"+Sub+"/VID.mp4"
    SilentMkdir("../"+"Data/"+Sub+"/VideoReconImg/")
>>>>>>> 7844edb370bb739feb7a723d3fa7254cc4b8d59e

    cam = cv2.VideoCapture(DataPath)
    # frame
    currentframe = 0
    count=0
    while(True):
          
        # reading from frame
        ret,frame = cam.read()
      
        if ret:
            # if video is still left continue creating images
<<<<<<< HEAD
            name = dirname+"/Data/"+Sub+"/VideoReconImg/" + str(currentframe) + '.jpg'
=======
            name = "../"+"Data/"+Sub+"/VideoReconImg/" + str(currentframe) + '.jpg'
>>>>>>> 7844edb370bb739feb7a723d3fa7254cc4b8d59e
            print ('Creating...' + name)
            cv2.imwrite(name, frame)
            count=count+1
            currentframe += 1
        else:
            break
    print ("VIDEO TO FRAMES DONE!!!!!!!") 
    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()
    return

def BlurDetection(Sub):
<<<<<<< HEAD
    
=======
>>>>>>> 7844edb370bb739feb7a723d3fa7254cc4b8d59e
    """
    Detects and removes blurry images from a specified directory based on their Laplacian variance.

    This function processes images in the directory "../Data/<Sub>/VideoReconImg/" 
    to identify and remove blurry images. It uses the Laplacian variance method to assess image 
    sharpness. If the variance is below a threshold (100), the image is considered blurry and is 
    deleted.

    The function performs the following steps:
    1. Loads images from the directory specified by the `<Sub>` parameter.
    2. Converts each image to grayscale.
    3. Calculates the Laplacian variance of each image to measure its sharpness.
    4. Deletes images with a Laplacian variance below the threshold (indicative of blurriness).
    
    Args:
        Sub (str): The subject or identifier used to construct the file path for the input images 
                   directory.

    Returns:
        None

    Raises:
        FileNotFoundError: If the directory specified by `LoadRoot` does not exist.
        OSError: If there is an issue with file operations such as deleting a file.

    Example:
        BlurDetection("Subject1")

    Notes:
        - Requires the OpenCV (`cv2`) and NumPy (`numpy`) libraries.
        - Assumes that the directory structure and image file naming conventions are followed.
        - The threshold for detecting blurriness (100) may need to be adjusted based on specific 
          requirements or image characteristics.
    """
    
    print ("Blue Detection")
    # load image
    blur_list=[]
    import cv2
    import numpy as np
<<<<<<< HEAD
    LoadRoot= dirname+"/Data/"+Sub+"/VideoReconImg/"
=======
    LoadRoot= dirname+"Data/"+Sub+"/VideoReconImg/"
>>>>>>> 7844edb370bb739feb7a723d3fa7254cc4b8d59e
    fileList = [f for f in os.listdir(LoadRoot) if f.endswith('.jpg')]
    for j in fileList:
        print("Reading file =================="+ j)
        img = cv2.imread(LoadRoot+j, cv2.IMREAD_GRAYSCALE)
        laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
        if laplacian_var < 100:
            os.remove(LoadRoot+j)
            #print("Image blurry")
            #blur_list.append(j[:-4])
            #print(laplacian_var)
    print ("Blue Detection DONE!!!!!!!!!!")
    return
            
def FinalFrames(Sub):
    """
    Copies a subset of images from a source directory to a new directory and deletes the original directory.

    This function selects and copies images from the directory "../Data/<Sub>/VideoReconImg/" 
    to a new directory "../Data/<Sub>/VideoReconImg_1/". The selection of images is based on 
    an interval defined by the `count` variable, which determines how frequently images are retained. 
    After copying the selected images, the original image directory is deleted.

    The function performs the following steps:
    1. Creates the destination directory if it does not exist.
    2. Loads images from the source directory.
    3. Copies every `count`-th image from the source directory to the destination directory.
    4. Deletes the source directory after copying the images.

    Args:
        Sub (str): The subject or identifier used to construct the file paths for the source and 
                   destination image directories.

    Returns:
        None

    Raises:
        FileNotFoundError: If the source directory does not exist.
        OSError: If there is an issue with file operations such as creating directories, copying files, 
                 or deleting the source directory.

    Example:
        FinalFrames("Subject1")

    Notes:
        - Requires the OpenCV (`cv2`) and NumPy (`numpy`) libraries, and the `shutil` module.
        - Assumes that the source directory contains image files with '.jpg' extension.
        - The `count` variable determines the interval at which images are retained. If `count` is set 
          to 1, all images are retained. If set to a higher number, only every `count`-th image is retained.
        - The original image directory is completely deleted after processing.
    """
    
   
    print ("Final Frames")
<<<<<<< HEAD
    SilentMkdir(dirname+"/Data/"+Sub+"/VideoReconImg_1/")
    LoadRoot=dirname+"/Data/"+Sub+"/VideoReconImg/"
=======
    SilentMkdir("../"+"Data/"+Sub+"/VideoReconImg_1/")
    LoadRoot="../"+"Data/"+Sub+"/VideoReconImg/"
>>>>>>> 7844edb370bb739feb7a723d3fa7254cc4b8d59e
    fileList = [f for f in os.listdir(LoadRoot) if f.endswith('.jpg')]
    n=len(fileList)
    count=1 #Use n/y, if you want only a specific "y" number of frames to be retained; use the integer 1 if all to be retained
    for i in np.arange(1,n-1,count):
        print(i)
        img = cv2.imread(LoadRoot+fileList[i])
<<<<<<< HEAD
        name = dirname+"/Data/"+Sub+"/VideoReconImg_1/" + fileList[i]
=======
        name = "../"+"Data/"+Sub+"/VideoReconImg_1/" + fileList[i]
>>>>>>> 7844edb370bb739feb7a723d3fa7254cc4b8d59e
        print ('Creating...' + name)
        cv2.imwrite(name, img)
    shutil.rmtree(LoadRoot)
    print ("Final Frames DONE")
    return



def run_1_cameraInit(binPath,baseDir,imgDir):
    """
    Initializes camera calibration using the AliceVision `cameraInit` executable.

    This function constructs and executes a command line to run the AliceVision `cameraInit` tool, 
    which initializes camera calibration based on images from a specified directory. It sets up 
    the necessary output and configuration files and executes the tool to generate a camera initialization 
    file.

    The function performs the following steps:
    1. Creates a directory for storing the camera initialization output.
    2. Constructs the command line for running the `cameraInit` tool with specified arguments.
    3. Executes the constructed command line to perform camera initialization.

    Args:
        binPath (str): The directory path where the AliceVision binaries are located.
        baseDir (str): The base directory where the output and task-specific folders will be created.
        imgDir (str): The directory containing images to be used for camera initialization.

    Returns:
        int: Returns 0 upon successful execution of the command.

    Raises:
        OSError: If there is an issue with executing the command line or file operations.

    Example:
        run_1_cameraInit("C:\\Program Files\\AliceVision", "C:\\Data\\Project", "C:\\Data\\Project\\Images")

    Notes:
        - Requires AliceVision binaries to be installed and available at the specified `binPath`.
        - Assumes the presence of `cameraSensors.db` in the AliceVision share directory.
        - The command line includes options such as `--defaultFieldOfView 45`, `--allowSingleView 1`, 
          and `--verboseLevel`, which should be adjusted based on specific requirements.
        - The `verboseLevel` variable must be defined elsewhere in the code.
        - The output is saved as `cameraInit.sfm` in the specified task folder.
    """
    
    taskFolder = "/1_CameraInit"
    SilentMkdir(baseDir + taskFolder)

    print("----------------------- 1/13 CAMERA INITIALIZATION -----------------------")

    imageFolder = "\"" + imgDir + "\""
    sensorDatabase = "\""+ str(Path(binPath).parent) + "\\share\\aliceVision\\cameraSensors.db" "\"" # Path to the sensors database, might change in later versions of meshrrom
   
    output = "\"" + baseDir + taskFolder + "/cameraInit.sfm" + "\""

    cmdLine = binPath + "\\aliceVision_cameraInit.exe"
    cmdLine += " --imageFolder {0} --sensorDatabase {1} --output {2}".format(
        imageFolder, sensorDatabase, output)

    cmdLine += " --defaultFieldOfView 45" 
    cmdLine += " --allowSingleView 1"
    cmdLine += " --verboseLevel " + verboseLevel

    os.system(cmdLine)

    return 0


def run_2_featureExtraction(binPath,baseDir , numberOfImages , imagesPerGroup=40):
    """
    Executes the feature extraction process using the AliceVision `featureExtraction` tool.
   
    This function runs the AliceVision `featureExtraction` tool to extract features from images 
    for the camera initialization pipeline. It handles large numbers of images by processing them 
    in manageable groups to avoid potential performance issues or limitations.
   
    The function performs the following steps:
    1. Creates a directory for storing feature extraction outputs if it does not already exist.
    2. Constructs the command line for executing the `featureExtraction` tool with specified arguments.
    3. If the total number of images exceeds the specified group size (`imagesPerGroup`), it processes 
       images in batches. Each batch is defined by a start index and range size.
    4. Executes the constructed command line or command lines to perform feature extraction.
   
    Args:
        binPath (str): The directory path where the AliceVision binaries are located.
        baseDir (str): The base directory where input and output directories are located.
        numberOfImages (int): The total number of images to process.
        imagesPerGroup (int, optional): The number of images to process in each group. Default is 40.
   
    Returns:
        None
   
    Raises:
        OSError: If there is an issue with executing the command line or file operations.
   
    Example:
        run_2_featureExtraction("C:\\Program Files\\AliceVision", "C:\\Data\\Project", 100, 40)
   
    Notes:
        - Requires AliceVision binaries to be installed and available at the specified `binPath`.
        - Assumes that the camera initialization `.sfm` file is located at `baseDir + "/1_CameraInit/cameraInit.sfm"`.
        - The `--forceCpuExtraction 1` flag is used to force feature extraction on the CPU. Adjust or remove 
          this flag based on whether GPU acceleration is available or desired.
        - Adjust the `imagesPerGroup` parameter based on your system's capability to handle large numbers of images.
        - This script uses Python’s `math.ceil` to determine the number of groups needed for processing.
    """
    taskFolder = "/2_FeatureExtraction"
    SilentMkdir(baseDir + taskFolder)

    print("----------------------- 2/13 FEATURE EXTRACTION -----------------------")

    _input = "\"" + baseDir + "/1_CameraInit/cameraInit.sfm" + "\""
    output = "\"" + baseDir + taskFolder + "\""

    cmdLine = binPath + "\\aliceVision_featureExtraction"
    cmdLine += " --input {0} --output {1}".format(_input, output)
    cmdLine += " --forceCpuExtraction 1"


    #Send images in groups if >40
    if(numberOfImages>imagesPerGroup):
        numberOfGroups=int(math.ceil( numberOfImages/imagesPerGroup))
        for i in range(numberOfGroups):
            cmd=cmdLine + " --rangeStart {} --rangeSize {} ".format(i*imagesPerGroup,imagesPerGroup)
            print("------- group {} / {} --------".format(i+1,numberOfGroups))
            print(cmd)
            os.system(cmd)

    else:
        print(cmdLine)
        os.system(cmdLine)


def run_3_imageMatching(binPath,baseDir):
    """
    Executes the image matching process using the AliceVision `imageMatching` tool.

    This function runs the AliceVision `imageMatching` tool to match features between images based on 
    previously extracted features. The tool generates a list of matched image pairs, which is saved 
    to an output file.

    The function performs the following steps:
    1. Creates a directory for storing the image matching outputs if it does not already exist.
    2. Constructs the command line for executing the `imageMatching` tool with specified arguments.
    3. Executes the constructed command line to perform image matching.

    Args:
        binPath (str): The directory path where the AliceVision binaries are located.
        baseDir (str): The base directory where input and output directories are located.

    Returns:
        None

    Raises:
        OSError: If there is an issue with executing the command line or file operations.

    Example:
        run_3_imageMatching("C:\\Program Files\\AliceVision", "C:\\Data\\Project")

    Notes:
        - Requires AliceVision binaries to be installed and available at the specified `binPath`.
        - Assumes that the camera initialization `.sfm` file is located at `baseDir + "/1_CameraInit/cameraInit.sfm"`.
        - Assumes that the features extracted in the previous step are stored in `baseDir + "/2_FeatureExtraction"`.
        - The output, `imageMatches.txt`, will be saved in `baseDir + "/3_ImageMatching"`.
        - The `--tree` parameter specifies the path to the VLFeat SIFT tree file used for image matching.
        - The `--verboseLevel` parameter controls the verbosity of the output. Ensure `verboseLevel` is defined elsewhere in your code.
        - This script uses Python’s `Path` class from the `pathlib` module to construct the path to the SIFT tree file.
    """
    
    taskFolder = "/3_ImageMatching"
    SilentMkdir(baseDir + taskFolder)

    print("----------------------- 3/13 IMAGE MATCHING -----------------------")

    _input = "\"" + baseDir + "/1_CameraInit/cameraInit.sfm" + "\""
    featuresFolders = "\"" + baseDir + "/2_FeatureExtraction" + "\""
    output = "\"" + baseDir + taskFolder + "/imageMatches.txt" + "\""

    cmdLine = binPath + "\\aliceVision_imageMatching.exe"
    cmdLine += " --input {0} --featuresFolders {1} --output {2}".format(
        _input, featuresFolders, output)

    cmdLine +=  " --tree " + "\""+ str(Path(binPath).parent)+ "/share/aliceVision/vlfeat_K80L3.SIFT.tree\""
    cmdLine += " --verboseLevel " + verboseLevel

    print(cmdLine)
    os.system(cmdLine)


def run_4_featureMatching(binPath,baseDir,numberOfImages,imagesPerGroup=20):
    """
    Executes the feature matching process using the AliceVision `featureMatching` tool.

    This function runs the AliceVision `featureMatching` tool to match features between images and 
    generate a list of matched image pairs. It handles large numbers of images by processing them 
    in batches to optimize performance and manage resource usage.

    The function performs the following steps:
    1. Creates a directory for storing the feature matching outputs if it does not already exist.
    2. Constructs the command line for executing the `featureMatching` tool with specified arguments.
    3. If the total number of images exceeds the specified group size (`imagesPerGroup`), it processes 
       images in batches. Each batch is defined by a start index and range size.
    4. Executes the constructed command line or command lines to perform feature matching.

    Args:
        binPath (str): The directory path where the AliceVision binaries are located.
        baseDir (str): The base directory where input and output directories are located.
        numberOfImages (int): The total number of images to process.
        imagesPerGroup (int, optional): The number of images to process in each group. Default is 20.

    Returns:
        None

    Raises:
        OSError: If there is an issue with executing the command line or file operations.

    Example:
        run_4_featureMatching("C:\\Program Files\\AliceVision", "C:\\Data\\Project", 100, 20)

    Notes:
        - Requires AliceVision binaries to be installed and available at the specified `binPath`.
        - Assumes that the camera initialization `.sfm` file is located at `baseDir + "/1_CameraInit/cameraInit.sfm"`.
        - Assumes that the features extracted in the previous step are stored in `baseDir + "/2_FeatureExtraction"`.
        - The `imageMatches.txt` file, located at `baseDir + "/3_ImageMatching/imageMatches.txt"`, should contain pairs of images to be matched.
        - The command line options used in this script include:
            - `--knownPosesGeometricErrorMax 5`: Sets the maximum geometric error for known camera poses.
            - `--verboseLevel`: Controls the verbosity of the output.
            - `--describerTypes sift`: Uses SIFT for feature description.
            - `--photometricMatchingMethod ANN_L2`: Uses ANN_L2 for photometric matching.
            - `--geometricEstimator acransac`: Uses ACRANSAC for geometric estimation.
            - `--geometricFilterType fundamental_matrix`: Uses the fundamental matrix for geometric filtering.
            - `--distanceRatio 0.8`: Sets the distance ratio for feature matching.
            - `--maxIteration 2048`, `--geometricError 0.0`, `--maxMatches 0`: Sets parameters for the matching process.
            - `--savePutativeMatches False`, `--guidedMatching False`, `--matchFromKnownCameraPoses False`, `--exportDebugFiles True`: Various options for saving and debugging.
        - Adjust the `imagesPerGroup` parameter based on your system's capability to handle large numbers of images.
        - This script uses Python’s `math.ceil` to determine the number of groups needed for processing.
    """
    
    taskFolder = "/4_featureMatching"
    SilentMkdir(baseDir + taskFolder)

    print("----------------------- 4/13 FEATURE MATCHING -----------------------")

    _input = "\"" +   baseDir + "/1_CameraInit/cameraInit.sfm" + "\""
    output = "\""  + baseDir + taskFolder + "\""
    featuresFolders = "\"" +  baseDir + "/2_FeatureExtraction" + "\""
    imagePairsList = "\"" +  baseDir + "/3_ImageMatching/imageMatches.txt" + "\""

    cmdLine = binPath + "\\aliceVision_featureMatching.exe"
    cmdLine += " --input {0} --featuresFolders {1} --output {2} --imagePairsList {3}".format(
        _input, featuresFolders, output, imagePairsList)

    cmdLine += " --knownPosesGeometricErrorMax 5"
    cmdLine += " --verboseLevel " + verboseLevel

    cmdLine += " --describerTypes sift --photometricMatchingMethod ANN_L2 --geometricEstimator acransac --geometricFilterType fundamental_matrix --distanceRatio 0.8"
    cmdLine += " --maxIteration 2048 --geometricError 0.0 --maxMatches 0"
    cmdLine += " --savePutativeMatches False --guidedMatching False --matchFromKnownCameraPoses False --exportDebugFiles True"

    #when there are more than 20 images, send them in batches
    if(numberOfImages>imagesPerGroup):
        numberOfGroups=math.ceil( numberOfImages/imagesPerGroup)
        for i in range(numberOfGroups):
            cmd=cmdLine + " --rangeStart {} --rangeSize {} ".format(i*imagesPerGroup,imagesPerGroup)
            print("------- group {} / {} --------".format(i,numberOfGroups))
            print(cmd)
            os.system(cmd)

    else:
        print(cmdLine)
        os.system(cmdLine)

def run_5_structureFromMotion(binPath,baseDir):
    """
    Executes the Structure-from-Motion (SfM) process using the AliceVision `incrementalSfm` tool.

    This function runs the AliceVision `incrementalSfm` tool to perform Structure-from-Motion, 
    which reconstructs the 3D structure of a scene from a set of images. The process estimates 
    camera poses and generates a 3D point cloud. 

    The function performs the following steps:
    1. Creates a directory for storing the Structure-from-Motion outputs if it does not already exist.
    2. Constructs the command line for executing the `incrementalSfm` tool with specified arguments.
    3. Executes the constructed command line to perform SfM.

    Args:
        binPath (str): The directory path where the AliceVision binaries are located.
        baseDir (str): The base directory where input and output directories are located.

    Returns:
        None

    Raises:
        OSError: If there is an issue with executing the command line or file operations.

    Example:
        run_5_structureFromMotion("C:\\Program Files\\AliceVision", "C:\\Data\\Project")

    Notes:
        - Requires AliceVision binaries to be installed and available at the specified `binPath`.
        - Assumes that the camera initialization `.sfm` file is located at `baseDir + "/1_CameraInit/cameraInit.sfm"`.
        - The output files will be saved in `baseDir + "/5_structureFromMotion"`, including:
            - `sfm.abc`: The main SfM output file in ABC format.
            - `cameras.sfm`: A file containing the reconstructed camera views and poses.
        - The `extraInfoFolder` parameter specifies where additional information related to SfM will be saved.
        - The `featuresFolders` and `matchesFolders` parameters point to the directories containing the extracted features and matched image pairs, respectively.
        - The `--verboseLevel` parameter controls the verbosity of the output. Ensure `verboseLevel` is defined elsewhere in your code.
    """
    
    taskFolder = "/5_structureFromMotion"
    SilentMkdir(baseDir + taskFolder)

    print("----------------------- 5/13 STRUCTURE FROM MOTION -----------------------")

    _input = "\"" +  baseDir + "/1_CameraInit/cameraInit.sfm" + "\""
    output = "\"" +  baseDir + taskFolder + "/sfm.abc" + "\" "
    outputViewsAndPoses = "\"" + baseDir + taskFolder + "/cameras.sfm" + "\""
    extraInfoFolder = "\""  + baseDir + taskFolder + "\""
    featuresFolders = "\"" + baseDir + "/2_FeatureExtraction" + "\""
    matchesFolders = "\"" +  baseDir + "/4_featureMatching" + "\""

    cmdLine = binPath + "\\aliceVision_incrementalSfm.exe"
    cmdLine += " --input {0} --output {1} --outputViewsAndPoses {2} --extraInfoFolder {3} --featuresFolders {4} --matchesFolders {5}".format(
        _input, output, outputViewsAndPoses, extraInfoFolder, featuresFolders, matchesFolders)

    cmdLine += " --verboseLevel " + verboseLevel

    print(cmdLine)
    os.system(cmdLine)


def run_6_prepareDenseScene(binPath,baseDir):
    """
    Prepares the dense scene reconstruction process using the AliceVision `prepareDenseScene` tool.

    This function runs the AliceVision `prepareDenseScene` tool to prepare the input data for dense reconstruction. 
    It processes the Structure-from-Motion (SfM) output to generate the necessary data files for the dense reconstruction step.

    The function performs the following steps:
    1. Creates a directory for storing the dense scene preparation outputs if it does not already exist.
    2. Constructs the command line for executing the `prepareDenseScene` tool with specified arguments.
    3. Executes the constructed command line to prepare the data for dense reconstruction.

    Args:
        binPath (str): The directory path where the AliceVision binaries are located.
        baseDir (str): The base directory where input and output directories are located.

    Returns:
        None

    Raises:
        OSError: If there is an issue with executing the command line or file operations.

    Example:
        run_6_prepareDenseScene("C:\\Program Files\\AliceVision", "C:\\Data\\Project")

    Notes:
        - Requires AliceVision binaries to be installed and available at the specified `binPath`.
        - Assumes that the Structure-from-Motion output `.abc` file is located at `baseDir + "/5_structureFromMotion/sfm.abc"`.
        - The prepared data will be saved in `baseDir + "/6_PrepareDenseScene"`.
        - The `--verboseLevel` parameter controls the verbosity of the output. Ensure `verboseLevel` is defined elsewhere in your code.
    """
    
    taskFolder = "/6_PrepareDenseScene"
    SilentMkdir(baseDir + taskFolder)

    print("----------------------- 6/13 PREPARE DENSE SCENE -----------------------")
    _input = "\"" +  baseDir +  "/5_structureFromMotion/sfm.abc" + "\""
    output = "\"" + baseDir + taskFolder + "\" "

    cmdLine = binPath + "\\aliceVision_prepareDenseScene.exe"
    cmdLine += " --input {0}  --output {1} ".format(_input,  output)

    cmdLine += " --verboseLevel " + verboseLevel

    print(cmdLine)
    os.system(cmdLine)


def run_7_depthMap(binPath,baseDir ,numberOfImages , groupSize=20 , downscale = 1):
    """
    Executes depth map estimation using the AliceVision `depthMapEstimation` tool.

    This function runs the AliceVision `depthMapEstimation` tool to compute depth maps for a set of images 
    based on the Structure-from-Motion (SfM) results. It processes images in batches to manage large datasets 
    and supports downscaling to speed up computation.

    The function performs the following steps:
    1. Creates a directory for storing the depth map outputs if it does not already exist.
    2. Constructs the command line for executing the `depthMapEstimation` tool with specified arguments.
    3. Processes images in batches if the total number of images exceeds the specified `groupSize`.
    4. Executes the constructed command line for each batch to estimate depth maps.

    Args:
        binPath (str): The directory path where the AliceVision binaries are located.
        baseDir (str): The base directory where input and output directories are located.
        numberOfImages (int): The total number of images to process.
        groupSize (int, optional): The number of images to process in each batch. Default is 20.
        downscale (int, optional): The downscale factor for the images. Default is 1 (no downscaling).

    Returns:
        None

    Raises:
        OSError: If there is an issue with executing the command line or file operations.

    Example:
        run_7_depthMap("C:\\Program Files\\AliceVision", "C:\\Data\\Project", 100, 20, 2)

    Notes:
        - Requires AliceVision binaries to be installed and available at the specified `binPath`.
        - Assumes that the SfM output `.abc` file is located at `baseDir + "/5_structureFromMotion/sfm.abc"`.
        - The depth maps will be saved in `baseDir + "/7_DepthMap"`.
        - The `imagesFolder` parameter points to the directory where the prepared images for dense reconstruction are located.
        - The `--verboseLevel` parameter controls the verbosity of the output. Ensure `verboseLevel` is defined elsewhere in your code.
        - The `--downscale` parameter controls the downscaling of images to speed up processing. Adjust based on the balance between speed and accuracy.
        - This script uses Python’s `math.ceil` to determine the number of batches needed for processing.
    """
    
    taskFolder = "/7_DepthMap"
    SilentMkdir(baseDir + taskFolder)

    print("----------------------- 7/13 DEPTH MAP -----------------------")
    _input = "\""  + baseDir +   "/5_structureFromMotion/sfm.abc" + "\""
    output = "\"" + baseDir + taskFolder + "\""
    imagesFolder = "\"" + baseDir + "/6_PrepareDenseScene" + "\""

    cmdLine = binPath + "\\aliceVision_depthMapEstimation.exe"
    cmdLine += " --input {0}  --output {1} --imagesFolder {2}".format(
        _input,  output, imagesFolder)

    cmdLine += " --verboseLevel " + verboseLevel
    cmdLine += " --downscale " + str(downscale)

    
    numberOfBatches = int(math.ceil( numberOfImages / groupSize ))

    for i in range(numberOfBatches):
        groupStart = groupSize * i
        currentGroupSize = min(groupSize,numberOfImages - groupStart)
        if groupSize > 1:
            print("DepthMap Group {} of {} : {} to {}".format(i, numberOfBatches, groupStart, currentGroupSize))
            cmd = cmdLine + (" --rangeStart {} --rangeSize {}".format(str(groupStart),str(groupSize)))       
            print(cmd)
            os.system(cmd)




def run_8_depthMapFilter(binPath,baseDir):
    """
    Executes depth map filtering using the AliceVision `depthMapFiltering` tool.

    This function runs the AliceVision `depthMapFiltering` tool to filter depth maps generated from the depth map estimation process. 
    The filtering process refines the depth maps to remove noise and improve the quality of the depth information.

    The function performs the following steps:
    1. Creates a directory for storing the depth map filtering outputs if it does not already exist.
    2. Constructs the command line for executing the `depthMapFiltering` tool with specified arguments.
    3. Executes the constructed command line to filter the depth maps.

    Args:
        binPath (str): The directory path where the AliceVision binaries are located.
        baseDir (str): The base directory where input and output directories are located.

    Returns:
        None

    Raises:
        OSError: If there is an issue with executing the command line or file operations.

    Example:
        run_8_depthMapFilter("C:\\Program Files\\AliceVision", "C:\\Data\\Project")

    Notes:
        - Requires AliceVision binaries to be installed and available at the specified `binPath`.
        - Assumes that the Structure-from-Motion output `.abc` file is located at `baseDir + "/5_structureFromMotion/sfm.abc"`.
        - The filtered depth maps will be saved in `baseDir + "/8_DepthMapFilter"`.
        - The `depthMapsFolder` parameter points to the directory where the depth maps from the previous step are located.
        - The `--verboseLevel` parameter controls the verbosity of the output. Ensure `verboseLevel` is defined elsewhere in your code.
    """
    
    taskFolder = "/8_DepthMapFilter"
    SilentMkdir(baseDir + taskFolder)

    print("----------------------- 8/13 DEPTH MAP FILTER-----------------------")
    _input = "\""  + baseDir +   "/5_structureFromMotion/sfm.abc" + "\""
    output = "\"" + baseDir + taskFolder + "\""
    depthMapsFolder = "\""  + baseDir + "/7_DepthMap" + "\""

    cmdLine = binPath + "\\aliceVision_depthMapFiltering.exe"
    cmdLine += " --input {0}  --output {1} --depthMapsFolder {2}".format(
        _input,  output, depthMapsFolder)

    cmdLine += " --verboseLevel " + verboseLevel

    print(cmdLine)
    os.system(cmdLine)


def run_9_meshing(binPath,baseDir  , maxInputPoints = 50000000  , maxPoints=1000000):
    """
    Executes the meshing process using the AliceVision `meshing` tool.
 
    This function runs the AliceVision `meshing` tool to generate a 3D mesh from the depth maps and structure-from-motion (SfM) data.
    The meshing process converts the depth maps into a detailed 3D mesh and outputs both the dense point cloud and the mesh model.
 
    The function performs the following steps:
    1. Creates a directory for storing the meshing outputs if it does not already exist.
    2. Constructs the command line for executing the `meshing` tool with specified arguments.
    3. Executes the constructed command line to generate the mesh and dense point cloud.
 
    Args:
        binPath (str): The directory path where the AliceVision binaries are located.
        baseDir (str): The base directory where input and output directories are located.
        maxInputPoints (int, optional): The maximum number of input points to use for meshing. Default is 50,000,000.
        maxPoints (int, optional): The maximum number of points to include in the final mesh. Default is 1,000,000.
 
    Returns:
        None
 
    Raises:
        OSError: If there is an issue with executing the command line or file operations.
 
    Example:
        run_9_meshing("C:\\Program Files\\AliceVision", "C:\\Data\\Project", 10000000, 500000)
 
    Notes:
        - Requires AliceVision binaries to be installed and available at the specified `binPath`.
        - Assumes that the Structure-from-Motion output `.abc` file is located at `baseDir + "/5_structureFromMotion/sfm.abc"`.
        - The generated dense point cloud will be saved as `densePointCloud.abc` and the mesh model as `mesh.obj` in `baseDir + "/9_Meshing"`.
        - The `depthMapsFolder` parameter points to the directory where the filtered depth maps from the previous step are located.
        - The `--verboseLevel` parameter controls the verbosity of the output. Ensure `verboseLevel` is defined elsewhere in your code.
        - Adjust `maxInputPoints` and `maxPoints` based on the complexity of your scene and the desired level of detail in the mesh.
    """
    
    taskFolder = "/9_Meshing"
    SilentMkdir(baseDir + taskFolder)

    print("----------------------- 9/13 MESHING -----------------------")
    _input = "\""  + baseDir +  "/5_structureFromMotion/sfm.abc" + "\""
    output = "\""  + baseDir +   taskFolder + "/densePointCloud.abc" "\""
    outputMesh = "\""  + baseDir + taskFolder + "/mesh.obj" + "\""
    depthMapsFolder = "\"" + baseDir + "/8_DepthMapFilter" + "\""

    cmdLine = binPath + "\\aliceVision_meshing.exe"
    cmdLine += " --input {0}  --output {1} --outputMesh {2} --depthMapsFolder {3} ".format(
        _input,  output, outputMesh, depthMapsFolder)

    cmdLine += " --maxInputPoints " + str(maxInputPoints)
    cmdLine += " --maxPoints " + str(maxPoints)
    cmdLine += " --verboseLevel " + verboseLevel


    print(cmdLine)
    os.system(cmdLine)


def run_10_meshFiltering(binPath,baseDir ,keepLargestMeshOnly="True"):
    """
    Executes mesh filtering using the AliceVision `meshFiltering` tool.

    This function runs the AliceVision `meshFiltering` tool to refine and filter the 3D mesh generated from the previous meshing step. 
    The filtering process can be configured to keep only the largest mesh if desired, which is useful for simplifying and cleaning up the mesh.

    The function performs the following steps:
    1. Creates a directory for storing the mesh filtering outputs if it does not already exist.
    2. Constructs the command line for executing the `meshFiltering` tool with specified arguments.
    3. Executes the constructed command line to filter the mesh.

    Args:
        binPath (str): The directory path where the AliceVision binaries are located.
        baseDir (str): The base directory where input and output directories are located.
        keepLargestMeshOnly (str, optional): Indicates whether to keep only the largest mesh. Should be "True" or "False". Default is "True".

    Returns:
        None

    Raises:
        OSError: If there is an issue with executing the command line or file operations.

    Example:
        run_10_meshFiltering("C:\\Program Files\\AliceVision", "C:\\Data\\Project", "True")

    Notes:
        - Requires AliceVision binaries to be installed and available at the specified `binPath`.
        - Assumes that the input mesh file `mesh.obj` is located at `baseDir + "/9_Meshing/mesh.obj"`.
        - The filtered mesh will be saved as `mesh.obj` in `baseDir + "/10_MeshFiltering"`.
        - The `--verboseLevel` parameter controls the verbosity of the output. Ensure `verboseLevel` is defined elsewhere in your code.
        - The `keepLargestMeshOnly` parameter should be set to "True" or "False" as a string, depending on whether you want to retain only the largest mesh in case multiple meshes are present.
    """
    
    
    taskFolder = "/10_MeshFiltering"
    SilentMkdir(baseDir + taskFolder)

    print("----------------------- 10/13 MESH FILTERING -----------------------")
    inputMesh = "\""  + baseDir + "/9_Meshing/mesh.obj" + "\""
    outputMesh = "\""  + baseDir + taskFolder + "/mesh.obj" + "\""

    cmdLine = binPath + "\\aliceVision_meshFiltering.exe"
    cmdLine += " --inputMesh {0}  --outputMesh {1}".format(
        inputMesh, outputMesh)

    cmdLine += " --verboseLevel " + verboseLevel
    cmdLine += " --keepLargestMeshOnly " + keepLargestMeshOnly

    print(cmdLine)
    os.system(cmdLine)




def main():

    # Pass the arguments of the function as parameters in the command line code
    binPath = sys.argv[1]           ##  --> path of the binary files from Meshroom
    baseDir = sys.argv[2]           ##  --> name of the Folder containing the process (a new folder will be created)
    imgDir = sys.argv[3]            ##  --> Folder containing the images 

    Sub = sys.argv[4]     
    
    
    VideoToFrames(Sub)
    BlurDetection(Sub)
    FinalFrames(Sub)
    

    numberOfImages =  len([name for name in os.listdir(imgDir) if os.path.isfile(os.path.join(imgDir, name))])      ## number of files in the folder

    SilentMkdir(baseDir)

    startTime = time.time()

    run_1_cameraInit(binPath,baseDir,imgDir)
    run_2_featureExtraction(binPath,baseDir , numberOfImages)
    run_3_imageMatching(binPath,baseDir)
    run_4_featureMatching(binPath,baseDir,numberOfImages)
    run_5_structureFromMotion(binPath,baseDir)
    run_6_prepareDenseScene(binPath,baseDir)
    run_7_depthMap(binPath,baseDir , numberOfImages )
    run_8_depthMapFilter(binPath,baseDir)
    run_9_meshing(binPath,baseDir)
    run_10_meshFiltering(binPath,baseDir)


    
    print("-------------------------------- DONE ----------------------")
    endTime = time.time()
    hours, rem = divmod(endTime-startTime, 3600)
    minutes, seconds = divmod(rem, 60)
    print("time elapsed: "+"{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))


main()
