# README

You are going to need a virtual environment with Jupyter Notebook installed in order to use the toolbox. Follow these steps:

**This guide assumes you have already installed Python 3 on your computer.** To check, enter `python --version`. Sometimes, if you have both Python 2 and 3 installed at the same time, you might need to check using `python3 --version`. In this case, replace `python` with `python3` for the rest of the guide.

## For Windows 10 x64

1. Open a command line in the folder where you have extracted this zip-file. **Hint:** To open the command line in that folder, see the installation guide for Windows
2. Type `python -m venv cid_venv`. This will create the virtual environment.
3. Type `cd cid_venv & cd Scripts & activate.bat`. This will activate the virtual environment.

```shell
(cid_venv) C:\Users\ongun\Documents\GitHub\cid-workshop2\releases\workshop_prep\cid_venv\Scripts>
```

4.  Type `python -m pip install -r ../../requirements.txt` or `python -m pip install numpy matplotlib seaborn glom lxml pyproj jupyterlab`

5. Type `cd ../..` to go to the root folder, i.e. where `cid_mosaic.py` is.

6. Run Jupyter-Notebook using `jupyter notebook`