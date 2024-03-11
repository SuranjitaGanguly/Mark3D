## Mark3D

#### ================ Set the folder hierarchy================ 
The default folder hierarchy is as follows:

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


For making new scans, create a new folder under Mark3D/Data with the SubjectName, and save the video under Mark3D/Data/<SubjectName> as VID.mp4
Follow the photogrammetry pipeline after this. 
Make sure that you follow the folder hierarchy to avoid unintended errors in the paths provided in the automated algorithm. 

#### ==========Photogrammetry Pipeline==========
1. Set an environment in Python as per the requirements provided

2. In the command prompt, activate the environment using the following : 
conda activate <env name>

3. Change the directory to the path of the src folder of Mark3D using :  
cd /d <path>

4. Run the photogrammetry pipeline that converts a camera video into a 3D mesh model after taking care of any blurs that may incur during the recording of the video using the following:  

python Final_Photogram.py <path to the bin folder of MeshRoom>  < path to the output folder where you want your 3D model> <Path to videoReconImg_1> <SubjectName>
python Final_Photogram.py "D:\Mark3D\src\Meshroom_2020_1_1\aliceVision\bin" "D:\Mark3D\Output" "D:\Mark3D\Data\Mark3D_7\VideoReconImg_1" "Mark3D_7"

#### =========Running the UI=========
Visit the following link for more details: 

