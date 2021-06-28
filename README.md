For Part A:
     Open the terminal and use   -->   docker run -it -v $PWD:/app --name twitter -w /app python bash
     After this  --> pip install tweepy
     Then do --> python twitter_appA.python

     Then open another terminal:
        
        In the 2nd terminal use --> – docker run -it -v $PWD:/app --link twitter:twitter eecsyorku/eecs4415

        Then use --> spark-submit spark_appA.py

     After this open another terminal:
        
        Inside the 3rd terminal use --> python graph-A.py   
 
 
 
 For Part A:
     
     Open the terminal and use   -->   docker run -it -v $PWD:/app --name twitter -w /app python bash
     
     After this  --> pip install tweepy
     
     Then do --> python twitter_appB.python
 
 
 
 
 
 
 Then open another terminal:
        In the 2nd terminal use --> – docker run -it -v $PWD:/app --link twitter:twitter eecsyorku/eecs4415
        
        Since the docker has python 2, we need additional steps before submitting spark
        
        Once the docker is connected use --> export PYSPARK_PYTHON=python3.5

        
        Then use --> apt-get update
        
        Then use --> apt-get install gcc
        
        After this use --> apt-get python-dev python3-dev
        
        Once all the installation are completed use -->  pip install nltk

        After this open the bash for python using --> python3

        Once inside the bash use --> import nltk
        Then again inside the bash use --> nltk.download("vader_lexicon")
        After this close the bash e.g --> exit()

        After getting back to docker terminal use ---> spark-submit spark_appB.py

        After this open another 3rd terminal for the graph:
            Inside the 3rd terminal , you have 2 options:

            If you want the graph with Sum and total tweet count use --> python graph-B-Sum.py
            
          Else, if you want the graph with average of sentiments use --> python graph-B-avg.py
