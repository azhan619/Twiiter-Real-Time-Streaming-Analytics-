import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import style


fig = plt.figure()
ax = fig.add_subplot(111)

#Reference: https://www.youtube.com/watch?v=ZmYPzESC5YY


def animate(i):
    plot_g = open('partB-plot.txt','r').read() 
    
    lines = plot_g.split('\n')
  
    #Dictionary use to store the topic and total number of tweets with positive and negative tweets count for each topic.
    my_dict = {}
    
    x_axis = []
    y_axis = []
    
    my_l = [0,0,0]
    
   
    for line in lines:
        if len(line) > 1:
            
            x,y = line.split() 
            Tname = x.split("-")[0]
            Tsent = x.split("-")[1]
            
            if Tname not in my_dict.keys():

                #First value of the represent list of 3 values first one is total number of tweets for the topic
                #Second element in list is positive number of tweets for the topic.
                #Third element in the value of list is total number of negative values.
                if Tsent == "neutral":
                    my_dict[Tname] =  [(int(y)),0,0] 
                elif Tsent == "positive":
                    my_dict[Tname] =  [(int(y)),int(y),0] 
                else:
                    my_dict[Tname] =  [(int(y)),0,int(y)] 
            else:
                if Tsent == "neutral":
                    my_dict[Tname] =  [my_dict[Tname][0] + (int(y)),my_dict[Tname][1],my_dict[Tname][2]] 
                elif Tsent == "positive":
                    my_dict[Tname] =  [my_dict[Tname][0] + (int(y)),int(y),my_dict[Tname][2]] 
                else:
                    my_dict[Tname] =  [my_dict[Tname][0] + (int(y)),my_dict[Tname][1],int(y)] 
    
    for key,value in my_dict.items():
        x_axis.append(key + " - " + str(value[0]))
        y_axis.append((value[1] - value[2]))
    
    
    #print(my_dict)
    
    #print(last_key + ':' + str(last_value))
   
    ax.clear()
    style.use("ggplot")
    ax.bar(x_axis, y_axis, align='center',width=0.5, color='blue') 
    ax.set_xlabel(' Topic Name - \n [total # of Tweets]', fontsize=7)
    ax.set_ylabel(' Sum [ #Positive Tweets - #Negative Tweets ]', fontsize=8)

    ax.plot()
    

ani = animation.FuncAnimation(fig, animate, interval=2000) #call animate function, interval = 2sec
#plt.tight_layout()
plt.show()