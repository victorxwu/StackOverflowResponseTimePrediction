# Stack Overflow Response Time Prediction
Predicting response time on posts from Stack Overflow using tag based features and ML algorithms

This approach attempts to improve on the ML model created by Goderie et al. You can find their paper at: https://ieeexplore.ieee.org/document/7180106

This approach also is based on https://github.com/true-developer/Research-ML, which is done by former students __chrisfosterelli__ and __erwinli__ at Thompson Rivers University. 

## Preparation: <br /> 
Data dump from StackExchange regarding both posts and tags from Stack Overflow are used to create the model. To get started, you will need to download the newest data dump from archive.org:
  * __stackoverflow.com-Posts.7z:__ https://archive.org/download/stackexchange/stackoverflow.com-Posts.7z
  * __stackoverflow.com-Tags.7z:__ https://archive.org/download/stackexchange/stackoverflow.com-Tags.7z
  
Once you finish downloading both zip files, you can: <br /> 
1. Fork and clone the project to your local drive. 
2. Unzip both posts.xml and tags.xml to the folder where you cloned the project to. 

Setting up the work space: <br /> 
1. Install visual cpp build tools <br />
Link: http://landinghub.visualstudio.com/visual-cpp-build-tools

2. This project is based on python version 3.5.2: https://www.python.org/downloads/release/python-352/ <br />
Please make sure you added the python executable path to your PATH ENVIRONMENT variable.

3. List of libraries used in this experiment:
   * numpy‑1.15.4+mkl‑cp35‑cp35m‑win_amd64.whl
   
     > command prompt: pip install numpy‑1.15.4+mkl‑cp35‑cp35m‑win_amd64.whl <br />
     > direct download: http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy 
   
   * scipy-1.2.0-cp35-cp35m-win_amd64.whl
   
     > command prompt: pip install scipy-1.2.0-cp35-cp35m-win_amd64.whl <br />
     > direct download: https://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy 
   
   * scikit_learn-0.20.2-cp35-cp35m-win_amd64.whl
   
     > command prompt: pip install scikit_learn-0.20.2-cp35-cp35m-win_amd64.whl <br />
     > direct download: https://www.lfd.uci.edu/~gohlke/pythonlibs/#scikit-learn

## Instructions: <br />
1. filter_tagfile.py
   * This script takes tags.xml and turn it into tags.json format so it is easier to work with. 
   * Tags.json will later be used in generate_all.py.

2. filter_year2017.py & filter_year2018.py
   * Both scripts are doing similar things. They take posts.xml and turn it into filtered_posts.json with data from different years. 
   * The difference is that filter_year2017.py is taking 6 months worth of data from year 2017, and filter_year2018.py is taking 3 months worth of data from year 2018. 
   * Please feel free to modify the time intervals for experiments.

3. generate_all.py
   * This script would take the filter_posts.json and calculate features and response time, then store the features and response time into a new csv file (features.csv).
   * Tag.json is used here to create one of the features. 

4. categorize_all.py


5. analyse_all.py

