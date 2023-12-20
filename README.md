# STM Analyzer
## Describe
This app is dedicated to scintists of nanotechnology whom work relies on STM. App works with .SM4 files. It offers showing data about spectra measurements, splitting them into points where measurement has done, visualizing bias-current characteristic and its 1st derivative, choosing curves to display, smoothing them with Savitzky-Golay filter, adding curves and saving images. App also draws topography of scanned probe, including thermal drift finds optimal shift of forward and backward topography and draws mean topography.


## How to run project:
1. Install Python 3.11.4 (https://www.python.org/downloads/release/python-3114/).
VERY IMPORTANT!!! AT THE BEGINNING OF INSTALATION SELECT CHECKBOX "Add python.exe to PATH".

2. Open command prompt and type python --version, if You'll see Python 3.11.4 that means the installation has passed correctly, if not - reinstall Python.

3. Install Visual++ Redistributable (https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170).

4. Type command: pip install -r requirements.txt.

5. Type cd and paste path to the application.

6. Type python main.py.

## How to use project:
1. At the begining You can see a small window that will ask You to choose a file to open:

![1](https://github.com/lucasosiewicz/STM-analyzer/assets/109655615/251d2bc3-c86d-4240-8747-1253a3de4d22)

2. After You choose a file small window displays informations about a measurement. Also another big window will open itself.

![2](https://github.com/lucasosiewicz/STM-analyzer/assets/109655615/96904ef8-3fff-47d0-a6bd-926a0b344136)

3. In the left top corner You can see File tab. Here You can choose new file to analyze and open a large window again if You accidently closed it.

![3](https://github.com/lucasosiewicz/STM-analyzer/assets/109655615/be1e355c-e937-4c99-b93b-0edc5a3a5032)

4. In the bigger window there are three tabs: **Dataset, Plots** and **Topography**. In **Dataset** tab You can check values of each measurement round. As You can see this tab is splitted into **Current** and **dI/dU** tabs. **Current** shows bias-current characteristics, **dI/dU** shows their 1st derivative. App also splits this set into tabs which represent every point where spectra measurement has done. Subtab **Stats** contains mean values for every curve in every direction in every point (*mean_forward/backward_pi*), mean for each point (*mean_pi*) and mean of whole measurement in every direction (*mean_forward/backward*). There is also X columns which represents bias [V].

![4](https://github.com/lucasosiewicz/STM-analyzer/assets/109655615/3a4025d9-b033-4c9c-a374-636014bbb4c8)

5. Next there is a **Plots** tab. Here You can see plots of bias-current characteristics and their 1st derivative. Every curve represent *mean_pi* column from **Dataset** tab.

![5](https://github.com/lucasosiewicz/STM-analyzer/assets/109655615/21b2d004-f2c3-476e-8fc4-e67a8e62201c)

6. On a right side You can see toolbar panel. At the top You can pick curves which You want to display. Under every checkbox there is a square whose color is representative to color of curve.
