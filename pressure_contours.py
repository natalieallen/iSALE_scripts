# this code makes a pressure contour plot for an isale simulation
import pySALEPlot as psp
import matplotlib.pyplot as plt
from numpy import arange,sqrt,ma
import numpy as np
import matplotlib as mpl

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
dirname='Contour Plots'
psp.mkdir_p(dirname)

# Open the datafile
model=psp.opendatfile('../Chicxulub/jdata.dat')

# Set the distance units to km
model.setScale('km')

# Set up figure
fig=plt.figure(figsize=(8,4))

ax=fig.add_subplot(111,aspect='equal')

# Loop over timesteps - currently defined just for one specific timestamp, but can easily be changed to 
# plot a series of timesteps by changing the arange values
for i in arange(200,202,2):

    # Set the axis labels
    ax.set_xlabel('r [km]')
    ax.set_ylabel('z [km]')

    # Set the axis limits
    ax.set_xlim([0,140])
    ax.set_ylim([-40,5])

    # Read the time step 'i' from the datafile: 
    # read two or more fields by making a list of their abbreviations
    step=model.readStep("TrP",i)
    # setting up the surface
    p1=ax.pcolormesh(model.x,model.y,step.mat,
            cmap='pink',vmin=1,vmax=model.nmat+1, alpha=0.25)

	# some initializing for the contour plots
	xvals = step.xmark[step.ymark<10]
	yvals = step.ymark[step.ymark<10]
	triang = mpl.tri.Triangulation(xvals,yvals)

    # these are to make horizontal lines to mark today's erosion level
	ax.axhline(y=-8)
	ax.axhline(y=-11)
	
    # creating the contours here I manually set the levels to 5, 10, 25, 40, 60, 80 GPa
	c = ax.tricontour(triang,step.TrP[step.ymark<10],levels=[5e9,10e9,25e9,40e9,60e9,80e9], colors="black")
	fmt={}
	strs =["5","10","25","40","60","80"]
	for l,s in zip(c.levels,strs):
		fmt[l]=s
	
    # here I set manual locations for the contour labels
    # can just set to auto instead of manual if you want them auto-placed, but it can get messy
	ax.clabel(c,c.levels[::1],inline=True,fmt=fmt,fontsize=10,manual=True)
	
    x.set_title('t = {: 5.2f} s'.format(step.time))
	# Save the figure
    fig.tight_layout()
    fig.savefig('{}/Pressure-{:05d}.png'.format(dirname, i), format='png', dpi=300)

    ax.cla()	
