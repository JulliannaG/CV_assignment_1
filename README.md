# CV_assignment_1

__Installation and setup:__
For this assignment I used python virtual environment and created .venv folder using 'uv venv --python 3.12'. All packages are listed in 'requirements.txt' file.
Application can be open by running 'app.py' script. 'Modules' folder includes all functions required for this task.

__How to use application:__
After running application, the webcam feed will be displayed in full screen. At the bottom of the window there is displayed a menu with all possible modes:
* Normal - this is the initial mode, which can be also enered by pressing 'n' key. This mode is essential to switch between different modes (go back from submode menu to mode menu).

* Colors - this mode can be enetered by pressing 'c' key. There are a few submodes available:
    * RGB (press 'r') - converts image into RGB mode,
    * Gray (presss 'g') - applies gray scale to the image,
    * HSV (press 'h') - converts image into HSV mode,
    * Brightness/contrast (press 'b') - enables adjusting brightness and contrast level by buildin trackbars.

    For all submodes mentioned above a histogram can be displayed in separate window (press 'o' to open and 'c' to close). Be careful while changing submodes - the histogram may hide under the main app window, so it's recommended to close it before changing to another submode.

* Filters - this mode can be entered by pressing 'f' key. There are a few submodes available:
    * Gaussian (press 'g') - applies Gaussian blur, which can be adjusted by kernel size and sigmaX parameters,
    * Bilateral (press 'b') - applies Bilateral blur, which can be adjusted by d, sigmaColor and sigmaSpace parameters,
    * Canny (press 'c') - applies Canny edge detection, which can be adjusted by treshold1 and treshold2 parameters,
    * Hough (press 'h') - applies Hough Transform line detection, which can be adjusted by rho, theta and treshold parameters.

* Geometry - this mode can be entered by pressing 'g' key. There are a few submodes available:
    * Translate (press 't') - enables moving image in x or y axis.
    * Rotate (press 'r') - enables rotating image for up to 360 degrees.
    * Scale (press 's') - enables zooming in and out the picture.

* Panorama - this mode can be entered by pressing 'p' key. The panorama can be captured by pressing 'c' key and reset by pressing 'r' key.

* Calibrate - this mode can be entered by pressing 'i' key. It allows to calibrate the camera using a chessboard pattern. The program automatically detects corners of the pattern and, after collecting 20 different views of the chessboard, computes the camera matrix and distortion coefficients.
These parameters are saved to 'calibration.npz' file. then used to correct image distortion, which improves accuracy for tasks like augmented reality or 3D reconstruction.

* AR - this mode can be entered by pressing 'a' key. The system detects ArUco markers in the camera feed and uses the previously obtained calibration parameters from 'calibration.npz' file to estimate their 3D position and orientation. Without this file the AR moght not work correctly. Based on this, it overlays virtual 3D dinosaur object on top of the detected markers, so they appear anchored in the real world and follow the marker’s movement.

The application can be quit by pressing 'q' key from every level of application.
