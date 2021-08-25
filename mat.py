# this code makes a plot of the material surface from an isale simulation
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
dirname='Material'
psp.mkdir_p(dirname)

# Open the datafile
model=psp.opendatfile('../Chicxulub/jdata.dat')

# Set the distance units to km
model.setScale('km')

# Set up figure
fig=plt.figure(figsize=(8,4))

ax=fig.add_subplot(111,aspect='equal')

# Loop over timesteps
for i in arange(0,202,2):

    # Set the axis labels
    ax.set_xlabel('r [km]')
    ax.set_ylabel('z [km]')

    # Set the axis limits
    ax.set_xlim([-200,200])

    ax.set_ylim([-70,70])

    # Read the time step 'i' from the datafile: 
    # read two or more fields by making a list of their abbreviations
    step=model.readStep('Tmp',i)
    
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
    
            ax.plot(ma.masked_array(-step.xmark[tru.xlines[l]][:-1],mask=dist > maxsep*tru.d[0]),
                    step.ymark[tru.xlines[l]][:-1],
                    c='#808080',marker='None',linestyle='-',linewidth=0.5)

    ax.set_title('t = {: 5.2f} s'.format(step.time))
	# Save the figure
    fig.savefig('{}/Material-{:05d}.png'.format(dirname, i), format='png', dpi=300,bbox_inches="tight", pad_inches=0.1)

    ax.cla()	
	
