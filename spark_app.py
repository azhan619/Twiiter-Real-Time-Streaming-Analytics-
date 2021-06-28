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
ssc = StreamingContext(sc, 5)
# setting a checkpoint for RDD recovery (necessary for updateStateByKey)
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9009
dataStream = ssc.socketTextStream("twitter",9009)

# reminder - lambda functions are just anonymous functions in one line:
#
#   words.flatMap(lambda line: line.split(" "))
#
# is exactly equivalent to
#
#    def space_split(line):
#        return line.split(" ")
#
#    words.filter(space_split)

# split each tweet into words
words = dataStream.flatMap(lambda line: line.split(" "))

# list of hashtags used to filter tweets (5 related #hashtags)
filter_tweets = ['#Palestine', '#PSL2021', '#EURO2020', '#Crypto', '#WTCFinal']

# filter the words to get only hashtags
hashtags = words.filter(lambda w: w in filter_tweets)

# map each hashtag to be a pair of (hashtag,1)
hashtag_counts = hashtags.map(lambda x: (x, 1))

# adding the count of each hashtag to its last count
def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)

# do the aggregation, note that now this is a sequence of RDDs
hashtag_totals = hashtag_counts.updateStateByKey(aggregate_tags_count)

#checks if graph txt file exists and removes it before running
#used for graph.py
if os.path.exists('graph_data.txt'):
    os.remove('graph_data.txt')

#creates new files for graph data and output data
graph_data = open('graph_data.txt', 'a+') # keep apending to file
output = open('A_out.txt', 'a+')


# process a single time interval
def process_interval(time, rdd):
    # print a separator
    print("----------- %s -----------" % str(time))
    output.write("----------- %s -----------\n" % str(time))
    try:
        # sort counts (desc) in this time instance and take top 10
        sorted_rdd = rdd.sortBy(lambda x:x[1], False)
        top10 = sorted_rdd.take(10)

        # print it nicely
        for tag in top10:
            # write output to file
            
            graph_data.write('{:<40} {}\n'.format(tag[0], tag[1])) 
            output.write('{:<40} {}\n'.format(tag[0], tag[1]))
            print('{:<40} {}'.format(tag[0], tag[1]))
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

# do this for every single interval
hashtag_totals.foreachRDD(process_interval)



# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()

#close files
graph_data.close()
output.close()