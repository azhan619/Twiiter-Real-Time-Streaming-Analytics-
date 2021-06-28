from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer as sentInstance 

# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")
# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# create the Streaming Context from spark context, interval size 5 seconds
ssc = StreamingContext(sc, 3)
# setting a checkpoint for RDD recovery (necessary for updateStateByKey)
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9009
dataStream = ssc.socketTextStream("twitter",9009)


topic_hashtags = {'Bitcoin': ['#bitcoin', '#btc', '#bitcoinnews', '#bitcoinprice', '#bitcoincash','#bitcointrading','#bitcoinmine',
                    '#binancebitcoin','#litecoin','#bitcointesla'],
       'Cardano': ['#cardano', '#ada', '#cardanocommunity', '#cardanoada', '#tesla4ada','#cardanonft','#wearecardano'
                 , '#adausdt','#hoskinson' ,'#$ada'],
       'Ethereum': ['#ethereum', '#ethereumclassic', '#ethereumprice', '#ethereumnews', '#ethereummining', '#ethereuminvestment'
                    ,'#ethereumtrading','#eth','#ethereummax','#etherium'],            
       'Dogecoin': ['#doge', '#dogefather', '#dogetothemoon', '#dogecoin', '#dogecoin','#dogecointothemoon','#doge4tesla'
       ,'#dogetesla','#dogearmy','#dogelife'],
       'Binance': ['#bnb','#binance','#binancesmartchain','#bsc','#binancetrading','#binanceexchange','#binancecoin'
       ,'#binancesignals','#binancecoach','#binancedex'] }


# The function below is used to filter the incoming data stream of tweet, it returns true if the values of a certain topic matches
# Once the value of hashtag matches the, all the words of that tweet are added to the hashmaps later, in order to computer sentiments.

def hashtag_clean(line):
    
    found_hashtag = False
    
    for text in line.split(" "):
    
        for hash in topic_hashtags.values():
    
            if text.lower() in hash:
    
                found_hashtag = True
                return found_hashtag
    
    return found_hashtag


hashtags = dataStream.filter(hashtag_clean)

# The function below takes the tweet, and extract the topic name using hashtag name from the dctionary.
def hashtag_topic(tweet):
    
    TopicName = ""
    
    for word in tweet.split(" "):
        
        for topic in topic_hashtags.keys():
            
            for hashtags in topic_hashtags[topic]:
                
                if hashtags.upper() == word.upper():
                    
                    TopicName = topic
    
    return TopicName

#Referenced from the Reddit link in the assignment 3 document.
def sent_finder(tweet):
    sia = sentInstance()
    polarity = sia.polarity_scores(tweet)

    if polarity['compound'] > 0.2:
        
        return('-positive')
    
    elif polarity['compound'] < -0.2:
        
        return('-negative')
    
    else:
        
        return('-neutral')
    
# 
hashtag_counts = hashtags.map(lambda x: ( hashtag_topic(x) + sent_finder(x), 1))

# adding the count of each hashtag to its last count
def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)

# do the aggregation, note that now this is a sequence of RDDs
hashtag_totals = hashtag_counts.updateStateByKey(aggregate_tags_count)

#Here we check if the file already exisits, if it does then remove it.
if os.path.exists('partB-plot.txt'):
    
    os.remove('partB-plot.txt')

#Here we check if the file already exisits, if it does then remove it.
if os.path.exists('partB-output.txt'):
    
    os.remove('partB-output.txt')    



plot = open('partB-plot.txt', 'a+')

console_out = open('partB-output.txt', 'a+')

# process a single time interval
def process_interval(time, rdd):

    print("----------- %s -----------" % str(time))
    
    
    console_out.write("************* %s *************\n" % str(time))
    
    try:
        
        records = rdd.take(900)

        # Empty the graph plot file so that un-necessary data is not printed.
        plot.truncate(0)
        
        for thash in records:
            

            plot.write('{:<40} {}   \n'.format( thash[0], thash[1] )  ) 
            
            console_out.write('{:<40} {} \n'.format( thash[0] , thash[1] ) )
            
            print('{:<40} {}'.format(  thash[0] , thash[1] ) )
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

hashtag_totals.foreachRDD(process_interval)



# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()

# close files
plot.close()
console_out.close()