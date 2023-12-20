# STM Analyzer
## Describe
This app is dedicated to scintists of nanotechnology whom work relies on STM. App works with .SM4 files. It offers showing data about spectra measurements, splitting them into points where measurement has done, visualizing bias-current characteristic and its 1st derivative, choosing curves to display, smoothing them with Savitzky-Golay filter, adding curves and saving images. App also draws topography of scanned probe, including thermal drift finds optimal shift of forward and backward topography and draws mean topography.


## How to open:
1. Install Python 3.11.4 (https://www.python.org/downloads/release/python-3114/).
VERY IMPORTANT!!! AT THE BEGINNING OF INSTALATION SELECT CHECKBOX "Add python.exe to PATH".

2. Open command prompt and type python --version, if You'll see Python 3.11.4 that means the installation has passed correctly, if not - reinstall Python.

3. Install Visual++ Redistributable (https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170).

4. Type command: pip install -r requirements.txt.

5. Type cd and paste path to the application.

6. Type python main.py.
