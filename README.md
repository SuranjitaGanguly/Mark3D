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
