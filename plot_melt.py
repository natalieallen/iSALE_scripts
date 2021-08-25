# this code makes a plot of the isale profile with marked locations of melted material 
# (material that reached at least 60 GPa - can easily be set to other values if wanted)
import pySALEPlot as psp
import matplotlib.pyplot as plt
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
dirname='Melt Plots'
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
    ax.set_xlim([-200,200])
    ax.set_ylim([-70,70])

    # Read the time step 'i' from the datafile: 
    # read two or more fields by making a list of their abbreviations
    step=model.readStep("TrP",i)
    
    # -- the classic iSALEPlot mirrored setup. Plot the second field
    # -- using negative x values
    p1=ax.pcolormesh(model.x,model.y,step.mat,
            cmap='pink',vmin=1,vmax=model.nmat+1)
    p2=ax.pcolormesh(-model.x,model.y,step.mat, cmap='pink',
            vmin=1,vmax=model.nmat+1)

    # Material boundaries
    [ax.contour(model.xc,model.yc,step.cmc[mat],1,colors='k',linewidths=0.5) for mat in [0,1,2]]
    [ax.contour(-model.xc,model.yc,step.cmc[mat],1,colors='k',linewidths=0.5) for mat in [0,1,2]]

    # Tracer lines
    for u in range(1,model.tracer_numu):
        tru=model.tru[u]
        
        # Plot the tracers in horizontal lines, every 5 lines
        for l in arange(0,len(tru.xlines),5):
    
            # Get the distances between pairs of tracers in xlines
            dist=get_distances(step,tru.xlines[l])
            # Mask the xmark values if separation too big... means the line won't be connected here
            ax.plot(ma.masked_array(step.xmark[tru.xlines[l]][:-1],mask=dist > maxsep*tru.d[0]),
                    step.ymark[tru.xlines[l]][:-1],
                    c='#808080',marker='None',linestyle='-',linewidth=0.5)
 
            ax.plot(ma.masked_array(-1*step.xmark[tru.xlines[l]][:-1],mask=dist > maxsep*tru.d[0]),
                    step.ymark[tru.xlines[l]][:-1],
                    c='#808080',marker='None',linestyle='-',linewidth=0.5)
	
	# loop over tracer clouds
	for u in range(model.tracer_numu): 
		tstart = model.tru[u].start
		tend = model.tru[u].end
		xlist = []
		ylist = []
		tlist = []
        
        # finding the locations of tracers that reached a pressure greater than 60 GPa - our condition for melt
        # tlist has the pressures of each tracer added to the xlist and ylist
		for j in range(len(step.TrP)):
                    if step.TrP[j]> 6e10:
			xlist.append(step.xmark[j])
			ylist.append(step.ymark[j])
			tlist.append(step.TrP[j])

		# plotting the locations of the marked tracers
		scat = ax.scatter(xlist,ylist,s=3, c="red",linewidths=0)
		scat = ax.scatter(-1*np.array(xlist),ylist,s=3, c="red",linewidths=0)

		xlist = []
		ylist = []

    ax.set_title('t = {: 5.2f} s'.format(step.time))
	
	# Save the figure
    fig.savefig('{}/Melt-{:05d}.png'.format(dirname, i), format='png', dpi=300)

    ax.cla()	
	
