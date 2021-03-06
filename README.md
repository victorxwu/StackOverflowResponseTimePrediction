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
   
     > filter_tagfile.py tags.xml filteredtags.json

2. filter_year2017.py & filter_year2018.py
   * Both scripts are doing similar things. They take posts.xml and turn it into filtered_posts.json with data from different years. 
   * The difference is that filter_year2017.py is taking 6 months worth of data from year 2017, and filter_year2018.py is taking 3 months worth of data from year 2018. 
   * Please feel free to modify the time intervals for experiments.
   
     > filter.py posts.xml filtered2017.json <br /> 
     > filter.py posts.xml filtered2018.json

3. generate_all.py
   * This script would take the filter_posts.json and calculate features and response time, then store the features and response time into a new csv file (features.csv).
   * Tag.json is used here to create one of the features. 
   
      > generate_all.py filtered2017.json features2017.csv <br /> 
      > generate_all.py filtered2018.json features2018.csv

4. categorize_all.py
   * This script will take the feature csv file (features.csv) and categorize the features based on the response time (labeledfeatures.csv). 
   * Currently the script will group the response time into: within 1 hour, and more than 1 hour.
   * You can modify the script to try different time labels. 
   
      > categorize_all.py features2017.csv labeledfeatures2017.csv <br /> 
      > categorize_all.py features2018.csv labeledfeatures2018.csv

5. analyse_all.py
   * This script will take the labeled feature csv file (labeledfeatures.csv) and do a prediction using RandomForest Classifier. 
   * 10-fold cross validation will be performed.
   
      > analyse_all.py labeledfeatures2017.csv labeledfeatures2018.csv <br /> 
      > analyse_all.py labeledfeatures2018.csv labeledfeatures2017.csv <br />
       * The format is: __analyse_all.py trainingdataset.csv testingdataset.csv__
       * The result will give you the prediction accuracy by training with the first input, and testing using second input. 
       * The 10-fold cross validation will always be performed on the training dataset. And the cross validation result is always for training dataset (the first user input).
