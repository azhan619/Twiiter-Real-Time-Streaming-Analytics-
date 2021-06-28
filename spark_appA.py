from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests
import os


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


words = dataStream.flatMap(lambda line: line.split(" "))
if os.path.exists('partA-plot.txt'):
    
    os.remove('partA-plot.txt')

if os.path.exists('partA-output.txt'):
    
    os.remove('partA-output.txt')    



# Removing all the un-necesary hashtags here to limit to the max 5 hashtags only.
hashtags = words.filter(lambda w: w in ['#Crypto', '#Blockchain', '#Cardano', '#Bitcoin', '#Ethereum'] )


# map each hashtag to be a pair of (hashtag,1)
hashtag_counts = hashtags.map(lambda x: (x, 1))

# adding the count of each hashtag to its last count
def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)

# do the aggregation, note that now this is a sequence of RDDs
hashtag_totals = hashtag_counts.updateStateByKey(aggregate_tags_count)





g_file = open('partA-plot.txt', 'a+') 

my_output = open('partA-output.txt', 'a+')



def process_interval(time, rdd):
    
    print("----------- %s -----------" % str(time))
    
    
    my_output.write("********** %s *********\n" % str(time))
   
    try:
        # sort counts (desc) in this time instance and take top 10
        sorted_rdd = rdd.sortBy(lambda x:x[1], False)
        top10 = sorted_rdd.take(10)

        g_file.truncate(0)
        for tag in top10:
            
            
            
            g_file.write('{:<40} {}\n'.format(  tag[0]  , tag[1] ) ) 
            
            my_output.write('{:<40} {}\n'.format(  tag[0]  , tag[1]  )  )
            
            print('{:<40} {}'.format(  tag[0]  , tag[1]  )  )
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

# do this for every single interval
hashtag_totals.foreachRDD(process_interval)



# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()


g_file.close()
my_output.close()