<<<<<<< HEAD
## Mark3D

#### ================ Set the folder hierarchy================ 
The default folder hierarchy needs to be set as follows for seamless functioning:

Mark3D

|___ Data

     |___<SubjectName>
     
          | ____ VID.mp4
          
|___Output

|___src

    |___Meshroom_2020_1_1
    
    |___128Ch_Montage
    
    |___Final_Photogram
    
    |___HM_Utils
    
    |___UI

Kindly download Meshroom_2020_1_1 from the following link: https://github.com/alicevision/meshroom/releases
Place it under the src folder as shown above.
For making new scans, create a new folder under Mark3D/Data with the SubjectName as shown in the hierarchial structure above, and save the video under Mark3D/Data/<SubjectName> as VID.mp4
Follow the photogrammetry pipeline after this. The generated mesh model will be stored in the Output folder. You can use the path of the generated mesh model and run the GUI to annotate and save electrodes.
Make sure that you follow the folder hierarchy to avoid unintended errors in the paths provided in the automated algorithm. 

#### ==========Photogrammetry Pipeline==========
1. Set an environment in Python as per the requirements provided

2. In the command prompt, activate the environment using the following : 
conda activate <env name>

3. Change the directory to the path of the src folder of Mark3D using :  
cd /d <path>

4. Run the photogrammetry pipeline that converts a camera video into a 3D mesh model after taking care of any blurs that may incur during the recording of the video using the following:  

python Final_Photogram.py <path to the bin folder of MeshRoom>  < path to the output folder where you want your 3D model> <Path to videoReconImg_1> <SubjectName>
example: 
python Final_Photogram.py "D:\Mark3D\src\Meshroom_2020_1_1\aliceVision\bin" "D:\Mark3D\Output" "D:\Mark3D\Data\Mark3D_7\VideoReconImg_1" "Mark3D_7"

#### =========Running the UI=========
Visit the following link for more details: 




#### ========== If you use our tool, cite it! ==============
Its currently on arxv, under the following DOI: 10.36227/techrxiv.171617225.52618520/v1
=======
# Mark3D
## A toolbox for 3D head-surface recnstruction from a smartphone video, followed by sensor annotation in an intuitive GUI!
For complete validation, refer to the following article: https://www.techrxiv.org/users/747344/articles/937306-mark3d-a-semi-automated-open-source-toolbox-for-head-surface-reconstruction-and-electrode-position-registration-using-a-smartphone-camera-video


### Module Code - info
There are two parts to this toolbox, listed in the order of usage:  
(1) The 3D head-surface generation (taken care by the **Mark3D** folder)  
&nbsp;     &nbsp;This module allows you to convert a video into a 3D head-surface in the format of .stl  
&nbsp;     &nbsp;The head-surface can be imported into any 3D processing software for usage.  
&nbsp;     &nbsp;However, for our specific goal of the toolbox, we use the 3D head-surface further in the next module of our toolbox, viz, Mark3DGUI  
(2) The GUI for sensor annotation (taken care by the **Mark3DGUI** folder)  
&nbsp;     &nbsp;This module allows you to mark standard EEG positions in the 3D head-surface. The 3D locations are exported along with the sensor labels, so that they can be used to create montage files for FieldTrip and MNE-Python.  

### Instructions to run module code
=================For Module : Mark3D=================  
1. Set an environment in Python as per the requirements provided
2. In the command prompt, activate the environment using the following : 
conda activate <env name>
3. Change the directory to the path of the Mark3D folder of Mark3D using :  
cd /d <path>
4. Run the photogrammetry pipeline that converts a camera video into a 3D mesh model after taking care of any blurs that may incur during the recording of the video using the following:

**python Mark3D.py <aliceVision bin path> <Output folder path> <..\Mark3D\Data\"SubjectName"\VideoReconImg_1> <SubjectName>**
AN example of the same is as follows (assuming that "Mark3D_7" is the subject name====
**python Make3D.py "D:\Mark3D\src\Meshroom_2020_1_1\aliceVision\bin" "D:\Mark3D\Output" "D:\Mark3D\Data\Mark3D_7\VideoReconImg_1" "Mark3D_7"**

=================Running the UI=================  
Run Mark3DGUI.pu in the module Mark3DGUI

>>>>>>> 7844edb370bb739feb7a723d3fa7254cc4b8d59e
