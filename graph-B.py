import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import style

style.use('ggplot') # visually apealing
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
my_dict={}

# i = interval
# uses iterable frames 
def animate(i):
    graph_data = open('graph_data.txt','r').read() #reads line in file
    lines = graph_data.split('\n')
    xs = []
    my_dict={}
    x_axis = []
    y_axis = []
    
    ys = []
    for line in lines:
        if len(line) > 1:
            x,y = line.split() # split hashtag and count
            last_key = x
            last_value = int(y)
        if x in my_dict.keys():

            my_dict[x] =  my_dict[x] + int(y)
            
        else:
            my_dict[x] =  int(y)

    my_dict[last_key] = my_dict[last_key] - last_value         
    my_dict2 = {}
    
    for key,value in my_dict.items():
        my_l=[]
        a = []


        Tname = key.split("-")[0]
        Tsent = key.split("-")[1]

        if Tname not in my_dict2.keys():

            if (Tsent == "positive" ):
                my_l.insert(0,value)
                my_l.insert(1,float(value * 1))
                my_dict2[Tname] = my_l
            elif (Tsent == "negative" ):
                my_l.insert(0,value)
                my_l.insert(1,float(value * -1))
                my_dict2[Tname] = my_l
            else:
                my_l.insert(0,value)
                my_l.insert(1,0)
                my_dict2[Tname] = my_l                

        else:
            if (Tsent == "positive" ):
                a = my_dict2[Tname]
                b = a[0]
                my_l.insert(0, b + value)
                c = a[1] + float(value * 1)
                my_l.insert(1,c)
                my_dict2[Tname] = my_l
            elif (Tsent == "negative" ):
                a = my_dict2[Tname]
                b = a[0]
                my_l.insert(0, b + value)
                c = a[1] + float(value * -1)
                my_l.insert(1,c)
                my_dict2[Tname] = my_l
            else:
                a = my_dict2[Tname]
                b = a[0]
                c = a[1]
                my_l.insert(0, b + value)
                my_l.insert(1,c)
                my_dict2[Tname] = my_l     
    
    for key,value in my_dict2.items():
        xs.append(key + " - " + str(value[0]))
        ys.append(value[1])



    print(my_dict2)
    print(my_dict)
    #print(last_key + ':' + str(last_value))
   
    ax.clear()
    ax.bar(xs, ys, align='center', color='red') #horizontal bar graph
    ax.set_xlabel('# Occurrences', fontsize=13)
    ax.plot()
    

ani = animation.FuncAnimation(fig, animate, interval=000) #call animate function, interval = 2sec
#plt.tight_layout()
plt.show()