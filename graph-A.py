import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import style

#Reference: https://www.youtube.com/watch?v=ZmYPzESC5YY

fig = plt.figure()

ax = fig.add_subplot(1,1,1)


def animate(i):
	plot_d = open('partA-plot.txt','r').read() 
	
	lines = plot_d.split('\n')
	xs = []
	ys = []
	for line in lines:
		if len(line) > 1:
			
			x,y = line.split() 
			
			xs.append(x + "-" + str(y))
			
			ys.append(int(y))
	
	ax.clear()
	
	ax.bar(xs, ys,width=0.5, align='center', color='blue') 
	
	ax.set_xlabel('Hashtag Name - [# of tweets]', fontsize=10)
	
	ax.set_ylabel('Number of Hashtags', fontsize=10)
	
	ax.plot()

ani = animation.FuncAnimation(fig, animate, interval=3000) 
plt.show()