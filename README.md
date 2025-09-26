# CV_assignment_1

__Environment setup:__
Create virtual environment using 'uv venv --python 3.12' command. 
Use 'source .venv/bin/activate' to activate virtual environment.

All packages with their versions are listed in 'requirements.txt' file.

__How to run application:__
Application can be started by running 'main.py' script. 
The main framework of the application is located in 'app.py' file.
'Modules' folder contains all implemented application functions.

__Functions:__
After running application, the webcam feed will be displayed in full screen. At the bottom of the window there is displayed a menu with all possible modes:

* Normal - this is the initial mode, which can be also entered by pressing '__n__' key. This mode is essential to switch between different modes (going back from submode menu to mode menu). You can switch between specific groups of submodes only when being in correct mode.

* Colors - press '__c__' key to enter. Available submodes:
    * RGB (press '__r__') - converts image into RGB mode,
    * Gray (presss '__g__') - applies gray scale to the image,
    * HSV (press '__h__') - converts image into HSV mode,
    * Brightness/contrast (press '__b__') - enables adjusting brightness and contrast level by buildin trackbars.

    For all submodes mentioned above, a histogram can be displayed in separate window (press '__o__' to open and '__c__' to close). Be careful while changing submodes - the histogram may hide under the main app window, so it's recommended to close it before changing to another submode.

* Filters - press '__f__' key to enter. Available submodes:
    * Gaussian (press '__g__') - applies Gaussian blur, which can be adjusted by kernel size and sigmaX parameters,
    * Bilateral (press '__b__') - applies Bilateral blur, which can be adjusted by d, sigmaColor and sigmaSpace parameters,
    * Canny (press '__c__') - applies Canny edge detection, which can be adjusted by threshold1 and threshold2 parameters,
    * Hough (press '__h__') - applies Hough Transform line detection, which can be adjusted by rho, theta and threshold parameters.

* Geometry - press '__g__' key to enter. Available submodes:
    * Translate (press '__t__') - enables moving image in x or y axis.
    * Rotate (press '__r__') - enables rotating image for up to 360 degrees.
    * Scale (press '__s__') - enables zooming in and out the picture.

* Panorama - press '__p__' key to enter. The horizontal panorama can be captured by pressing and holding '__c__' key and reset by pressing '__r__' key.

* Calibrate - press '__i__' key to enter. This mode allows to calibrate the camera using a chessboard pattern ('A4_Chessboard_9x6.png'). The program automatically detects corners of the pattern and, after collecting 20 different views of the chessboard, computes the camera matrix and distortion coefficients.
These parameters are saved to 'calibration.npz' file, which are then used to correct image distortion in AR.

* AR - press '__a__' key to enter. The system detects ArUco markers in the camera feed ('A4_ArUco_Marker.png') and uses the previously obtained calibration parameters from 'calibration.npz' file to estimate their 3D position and orientation (without this file the AR may not work correctly).
Based on these parameters, it overlays virtual 3D dinosaur object on top of the detected markers, so they appear anchored in the real world and follow the marker’s movement.
The trex has been placed so that his legs are coming out of the marker. When marker is fliped upside down or positioned at odd angles, the apllication may crash.

The application can be quit by pressing '__q__' key from every level of application.
