# Mark3D : Toolbox for photogrammetry-based 3D head-surface reconstruction and sensor annotaion #
## Modules
The toolbox consists of two modules, to be executed in the following order :  
&nbsp;&nbsp;&nbsp;&nbsp; **Mark3D** : Inputs a video (of a person's head wearing teh EEG cap), recorded on a simple smartphone, and processes it to give a 3D mesh-based head-surface model
&nbsp;&nbsp;&nbsp;&nbsp; **Mark3DGUI** : Launches the GUI for sensor annotation and saving
**For validation and working, check out: https://www.techrxiv.org/users/747344/articles/937306-mark3d-a-semi-automated-open-source-toolbox-for-head-surface-reconstruction-and-electrode-position-registration-using-a-smartphone-camera-video**

### Usage
***Pre-requisites***
- Install depenencies with the Requirements.txt provided
- Download the Meshroom package from the following link: https://github.com/alicevision/meshroom/releases
  Current support for Meshroom: Only with Windows OS
**Mark3D Module**
1. Set an environment in Python as per the **requirements** provided
3. In the command prompt, activate the environment using the following : 
conda activate <env name>
4. Change the directory to the path of the Mark3D module (where the Mark3D.py is located):  
cd /d <path>

5. Run the photogrammetry pipeline that converts a camera video into a 3D head-surface after taking care of any blurs that may incur during the recording of the video using the following:  
**python Mark3D.py <path to the bin folder of aliceVision> <Path where you want your output> <path to Mark3D\Data\"Subject name"\VideoReconImg_1>
note that the folder "VideoReconImg_1" is created automatically and hence, it should not be renamed in the above arguments.

For example, if you store the project under the D: Drive, and if you have the subject name as "Mark3D_7" then you should type the following:
**python Mark3D.py "D:\Mark3D\src\Meshroom_2020_1_1\aliceVision\bin" "D:\Mark3D\Output" "D:\Mark3D\Data\Mark3D_7\VideoReconImg_1" "Mark3D_7"**

**Mark3DGUI Module**
1. Change the directory to the path of the Mark3DGUI module (where the Mark3DGUI.py is located):  
cd /d <path>
2. Run Mark3DGUI.py
