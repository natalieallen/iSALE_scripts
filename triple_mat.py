# this code makes a plots of the material surface from a three isale simulations
# and marks the location of the crater edge with an arrow and distance at a given timestamp
import pySALEPlot as psp
import matplotlib.pyplot as plt
import matplotlib as mpl
from numpy import arange,sqrt,ma
import numpy as np

# If viridis colormap is available, use it here
try:
    plt.set_cmap('viridis')
except:
    plt.set_cmap('YlGnBu_r')

# distances between tracers
def get_distances(s,line):
    x=s.xmark[line]
    y=s.ymark[line]
    return sqrt((x[:-1]-x[1:])**2+(y[:-1]-y[1:])**2)

# Define the maximum separation allowed when plotting lines
maxsep=3.

# Make an output directory
dirname='Triple'
psp.mkdir_p(dirname)

# Open datafiles
model_b=psp.opendatfile('../../Run_09_25_2/Chicxulub/jdata.dat')
model_g=psp.opendatfile('../Chicxulub/jdata.dat')
model_i=psp.opendatfile('../../Run_12_3/Chicxulub/jdata.dat')
# Set the distance units to km
model_b.setScale('km')
model_g.setScale('km')
model_i.setScale('km')

# Set up figure
fig=plt.figure(figsize=(12,5))
mpl.rcParams['axes.linewidth']=1.0
ax1=fig.add_subplot(131,aspect='equal')
ax2=fig.add_subplot(132,aspect='equal', sharey=ax1)
ax3=fig.add_subplot(133,aspect='equal', sharey=ax2)

# Loop over timesteps
for i in arange(00,202,2):

    # Set the axis labels
    ax1.set_xlabel('r [km]')
    ax1.set_ylabel('z [km]')
    ax2.set_xlabel('r [km]')
    ax3.set_xlabel('r [km]')

    # Set the axis limits
    ax1.set_aspect("auto")
    ax1.set_xlim([0,150])
    ax1.set_ylim([-75,75])
    ax1.set(adjustable="box-forced", aspect="equal")

    ax2.set_aspect("auto")
    ax2.set_xlim([0,150])
    ax2.set_ylim([-75,75])
    ax2.set(adjustable="box-forced", aspect="equal")

    ax3.set_aspect("auto")
    ax3.set_xlim([0,150])
    ax3.set_ylim([-75,75])
    ax3.set(adjustable="box-forced", aspect="equal")
    
    # Read the time step 'i' from the datafile: 
    # read two or more fields by making a list of their abbreviations
    step_i=model_i.readStep('Pre',i)
    step_g=model_g.readStep('Pre',i)
    step_b=model_b.readStep('Pre',i)
    
    # setting up the surface
    p1=ax1.pcolormesh(model_g.x,model_g.y,step_g.mat,
            cmap='pink',vmin=1,vmax=model_g.nmat+1)
    p2=ax2.pcolormesh(model_b.x,model_b.y,step_b.mat, cmap='pink',
            vmin=1,vmax=model_b.nmat+1)
    p3=ax3.pcolormesh(model_i.x,model_i.y,step_i.mat, cmap='pink',
            vmin=1,vmax=model_i.nmat+1)
    
    # Material boundaries
    [ax1.contour(model_g.xc,model_g.yc,step_g.cmc[mat],1,colors='k',linewidths=0.5) for mat in [0,1,2]]
    [ax2.contour(model_b.xc,model_b.yc,step_b.cmc[mat],1,colors='k',linewidths=0.5) for mat in [0,1,2]]
    [ax3.contour(model_i.xc,model_i.yc,step_i.cmc[mat],1,colors='k',linewidths=0.5) for mat in [0,1,2]]
    
    # Tracer lines
    for u in range(1,model_g.tracer_numu):
        tru1=model_g.tru[u]
        
        # Plot the tracers in horizontal lines, every 5 lines
        for l in arange(0,len(tru1.xlines),5):
    
            # Get the distances between pairs of tracers in xlines
            dist=get_distances(step_g,tru1.xlines[l])
            # Mask the xmark values if separation too big... means the line won't be connected here
            ax1.plot(ma.masked_array(step_g.xmark[tru1.xlines[l]][:-1],mask=dist > maxsep*tru1.d[0]),
                    step_g.ymark[tru1.xlines[l]][:-1],
                    c='#808080',marker='None',linestyle='-',linewidth=0.5, rasterized=True)


    for j in range(1,model_b.tracer_numu):
	tru2=model_b.tru[j]
        
        # Plot the tracers in horizontal lines, every 5 lines
        for k in arange(0,len(tru2.xlines),5):
    
            # Get the distances between pairs of tracers in xlines
            dist2=get_distances(step_b,tru2.xlines[k])
            # Mask the xmark values if separation too big... means the line won't be connected here
            ax2.plot(ma.masked_array(step_b.xmark[tru2.xlines[k]][:-1],mask=dist2 > maxsep*tru2.d[0]),
                    step_b.ymark[tru2.xlines[k]][:-1],
                    c='#808080',marker='None',linestyle='-',linewidth=0.5, rasterized=True)

    for m in range(1,model_i.tracer_numu):
	tru3=model_i.tru[m]
        
        # Plot the tracers in horizontal lines, every 5 lines
        for n in arange(0,len(tru3.xlines),5):
    
            # Get the distances between pairs of tracers in xlines
            dist3=get_distances(step_i,tru3.xlines[n])
            # Mask the xmark values if separation too big... means the line won't be connected here
            ax3.plot(ma.masked_array(step_i.xmark[tru3.xlines[n]][:-1],mask=dist3 > maxsep*tru3.d[0]),
                    step_i.ymark[tru3.xlines[n]][:-1],
                    c='#808080',marker='None',linestyle='-',linewidth=0.5)


    # marking the location of the edge of the crater at timestep 200
    # by marking the location where the slope of the surface changes from positive to negative
    # may have to play around with the m,n,t values (where it starts looking for the slope change)
    # because there are small slope changes closer to the center sometimes
    if i ==200:
	xlist_g = []
	ylist_g = []
	xlist_b = []
	ylist_b = []
	xlist_i = []
	ylist_i = []
	j = 2
	k = 0
	while j < 200:
		use = []
		arr = step_g.ymark[(step_g.xmark <= j) & (step_g.xmark >=k)]
		# making sure the point seen as the surface isn't really high in the air 
		# (single stuck tracers can get caught high in the simulation and mess with the surface)
		if max(arr) > 500:
			use = arr[arr <= 500]
			ylist_g.append(max(use))
		else:
			ylist_g.append(max(arr))
			xlist_g.append(j)
		j=j+2
		k=k+2

	a = 2
	b = 0
	while a < 200:
		use = []
		arr = step_b.ymark[(step_b.xmark <= a) & (step_b.xmark >=b)]
		if max(arr) > 500:
			use = arr[arr <= 500]
			ylist_b.append(max(use))
		else:
			ylist_b.append(max(arr))
			xlist_b.append(a)
		a=a+2
		b=b+2

	c = 2
	d = 0
	while c < 200:
		use = []
		arr = step_i.ymark[(step_i.xmark <= c) & (step_i.xmark >=d)]
		if max(arr) > 500:
			use = arr[arr <= 500]
			ylist_i.append(max(use))
		else:
			ylist_i.append(max(arr))
			xlist_i.append(c)
		c=c+2
		d=d+2
	if i ==200:
		m = 65
		while m < 100:
			if ylist_g[m-1]<ylist_g[m] and ylist_g[m]>0:
				y_end = ylist_g[m]
				x_end = xlist_g[m]
				break
			else:
				m = m+1
		n = 62
		while n < 100:
			if ylist_b[n-1]<ylist_b[n] and ylist_b[n]>0:
				y_end2 = ylist_b[n]
				x_end2 = xlist_b[n]
				break
			else:
				n=n+1
		t=15
		while t < 100:
			if ylist_i[t-1]<ylist_i[t] and ylist_i[t]>0:
				y_end3 = ylist_i[t]
				x_end3 = xlist_i[t]
				break
			else:
				t = t+1

		# plot arrows at the found location of the edge of the crater
		ax1.annotate("{0} km".format(xlist_g[m]), xy = (x_end,y_end+10),xycoords='data',xytext=(x_end-17, y_end+50),horizontalalignment="left", textcoords='data',arrowprops = dict(arrowstyle="simple", connectionstyle="arc3"))

		ax2.annotate("{0} km".format(xlist_b[n]),xy = (x_end2, y_end2+10), xycoords ='data', xytext=(x_end2-16.5,y_end2+50), textcoords='data', arrowprops = dict(arrowstyle='simple', connectionstyle="arc3"))

		ax3.annotate("{0} km".format(xlist_i[t]), xy = (x_end3,y_end3+10),xycoords='data',xytext=(x_end3-14, y_end3+50), textcoords='data',arrowprops = dict(arrowstyle="simple", connectionstyle="arc3"))
    
    ax2.set_title('t = {: 5.2f} s'.format(step_g.time), rasterized=True)
	# Save the figure
    fig.savefig('{}/Material-{:05d}.png'.format(dirname, i), format='png', dpi=300)

    ax1.cla()
    ax2.cla()
    ax3.cla()	

