# Stack Overflow Response Time Prediction
Predicting response time on posts from Stack Overflow using tag based features and ML algorithms

This approach attempts to improve on the ML model created by Goderie et al. You can find their paper at: https://ieeexplore.ieee.org/document/7180106

## Preparation: <br /> 
Data dump from StackExchange regarding both posts and tags from Stack Overflow are used to create the model. To get started, you will need to download the newest data dump from archive.org:
  * __stackoverflow.com-Posts.7z:__ https://archive.org/download/stackexchange/stackoverflow.com-Posts.7z
  * __stackoverflow.com-Tags.7z:__ https://archive.org/download/stackexchange/stackoverflow.com-Tags.7z
  
Once you finish downloading both zip files, you can: <br /> 
1. Fork and clone the project to your local drive. 
2. Unzip both posts.xml and tags.xml to the folder where you cloned the project to. 

Setting up the work space: <br /> 
1. This project is based on python version 3.5.2: https://www.python.org/downloads/release/python-352/ <br/ >
Please make sure you added the python executable path to your PATH ENVIRONMENT variable.

2. List of libraries used in this experiment:
   * numpy‑1.15.4+mkl‑cp35‑cp35m‑win_amd64.whl
    > command prompt: pip install numpy‑1.15.4+mkl‑cp35‑cp35m‑win_amd64.whl <br />
    > direct download: http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy 
   * 


## Instruction: <br />
