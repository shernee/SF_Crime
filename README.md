# Crime Data Analyzer and Viewer

### This is a project to understand and analyze certain aspects of crime in San Francisco city

### This is my [Medium blog post](https://medium.com/@neelearning93/interactive-data-visualization-using-bokeh-and-python-c48657294c2c) on it! 

## Sample Data

To download the original data set directly from the website, the link is:

 https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-Historical-2003/tmnf-yvry (I have saved the downloaded data in *Data.csv* and used it in the analysis, but it's not uploaded here because it is large)

For the purpose of the analysis, I have only selected the columns that I thought would be useful and saved the resulting data-frame as a pickle file *Data.pkl*.

The dataset which is used specifically by the bokeh server app is saved as a pickle file *Appdata.pkl*.

*Data.pkl* and *Appdata.pkl* are not directly available in this directory, but the *Analysis.ipynb* code generates these files.

The Libraries required to run this project are available in *Req.txt*..

## Analysis of Data

The Python code for the Analysis of this dataset is in *Analysis.ipynb*

The code for the interactive applet can also be used in a Jupyter Notebook with some changes.

## Running the Data

To view this app from the bokeh server, run the server and point it to this (SF_Crime) directory.
- First, from this directory run,
        
        bokeh serve .
        
- Open a browser and navigate to the following URL,
        
        https://localhost:5006/SF_Crime
        
        
If you need additional configurations to run the app you can refer to Bokeh's user guide:
        
 https://bokeh.pydata.org/en/latest/docs/user_guide/server.html#userguide-server
 https://bokeh.pydata.org/en/latest/docs/reference/command/subcommands/serve.html