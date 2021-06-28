import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import style

style.use('dark_background') 
fig = plt.figure()
ax = fig.add_subplot(1,1,1)


def animate(i):
	graph_data = open('partA-graph.txt','r').read() 
	lines = graph_data.split('\n')
	xs = []
	ys = []
	for line in lines:
		if len(line) > 1:
			x,y = line.split() 
			xs.append(x)
			ys.append(int(y))
	ax.clear()
	ax.bar(xs, ys,width=0.5, align='center', color='blue') 
	ax.set_xlabel('Hashtag Name', fontsize=10)
	ax.set_ylabel('Number of Hashtags', fontsize=10)
	ax.plot()

ani = animation.FuncAnimation(fig, animate, interval=2000) 
plt.show()