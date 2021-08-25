# this code makes three plots of the isale profile with marked locations of melted material 
# (material that reached at least 60 GPa - can easily be set to other values if wanted)
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

# setting plot linewidth
mpl.rcParams["axes.linewidth"] = 1

# distances between tracers
def get_distances(s,line):
    x=s.xmark[line]
    y=s.ymark[line]
    return sqrt((x[:-1]-x[1:])**2+(y[:-1]-y[1:])**2)

# Define the maximum separation allowed when plotting lines
maxsep=3.

# Make an output directory
dirname='Triple Melt'
psp.mkdir_p(dirname)

# Open three datafiles
model_b=psp.opendatfile('../../Run_09_25_2/Chicxulub/jdata.dat')
model_g=psp.opendatfile('../Chicxulub/jdata.dat')
model_i=psp.opendatfile('../../Run_12_3/Chicxulub/jdata.dat')
# Set the distance units to km
model_b.setScale('km')
model_g.setScale('km')
model_i.setScale('km')

# Set up figure
fig=plt.figure(figsize=(12,5))
ax1=fig.add_subplot(131,aspect='equal')
ax2=fig.add_subplot(132,aspect='equal', sharey=ax1)
ax3=fig.add_subplot(133,aspect='equal', sharey=ax2)

# Loop over timesteps - currently defined just for one specific timestamp, but can easily be changed to 
# plot a series of timesteps by changing the arange values
for i in arange(200,202,2):

    # Setting labels
    ax1.set_xlabel('r [km]')
    ax1.text(132,62,'Model A')
    ax1.set_ylabel('z [km]')

    ax2.set_xlabel('r [km]')
    ax2.text(132,62,'Model B')

    ax3.set_xlabel('r [km]')
    ax3.text(132,62,'Model C')
    
    # Setting axis limits
    ax1.set_aspect("auto")
    ax1.set_xlim([0,180])
    ax1.set_ylim([-75,75])
    ax1.set(adjustable="box-forced", aspect="equal")

    ax2.set_aspect("auto")
    ax2.set_xlim([0,180])
    ax2.set_ylim([-75,75])
    ax2.set(adjustable="box-forced", aspect="equal")

    ax3.set_aspect("auto")
    ax3.set_xlim([0,180])
    ax3.set_ylim([-75,75])
    ax3.set(adjustable="box-forced", aspect="equal")

    # Read the time step 'i' from the datafile: 
    # read two or more fields by making a list of their abbreviations
    step_i=model_i.readStep("TrP",i)
    step_g=model_g.readStep("TrP",i)
    step_b=model_b.readStep("TrP",i)
    
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
                    c='#808080',marker='None',linestyle='-',linewidth=0.5)


    for j in range(1,model_b.tracer_numu):
	tru2=model_b.tru[j]
        
        # Plot the tracers in horizontal lines, every 5 lines
        for k in arange(0,len(tru2.xlines),5):
    
            # Get the distances between pairs of tracers in xlines
            dist2=get_distances(step_b,tru2.xlines[k])
            # Mask the xmark values if separation too big... means the line won't be connected here
            ax2.plot(ma.masked_array(step_b.xmark[tru2.xlines[k]][:-1],mask=dist2 > maxsep*tru2.d[0]),
                    step_b.ymark[tru2.xlines[k]][:-1],
                    c='#808080',marker='None',linestyle='-',linewidth=0.5)

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
	
	xlist1 = []
	ylist1 = []
	tlist1 = []

	xlist2 = []
	ylist2 = []
	tlist2 = []

	xlist3 = []
	ylist3 = []
	tlist3 = []

    # finding the locations of tracers that reached a pressure greater than 60 GPa - our condition for melt
    # tlist has the pressures of each tracer added to the xlist and ylist
	for j in range(len(step_g.TrP)):
            if step_g.TrP[j]> 6e10:
		xlist1.append(step_g.xmark[j])
		ylist1.append(step_g.ymark[j])
		tlist1.append(step_g.TrP[j])

	for k in range(len(step_b.TrP)):
            if step_b.TrP[k]> 6e10:
		xlist2.append(step_b.xmark[k])
		ylist2.append(step_b.ymark[k])
		tlist2.append(step_b.TrP[k])


	for n in range(len(step_i.TrP)):
            if step_i.TrP[n]> 6e10:
		xlist3.append(step_i.xmark[n])
		ylist3.append(step_i.ymark[n])
		tlist3.append(step_i.TrP[n])
	
	# plotting the locations of the marked tracers
	scat1 = ax1.scatter(xlist1,ylist1, c="red",linewidths=0)
	
	scat2 = ax2.scatter(np.array(xlist2),ylist2, c="red",linewidths=0)

	scat3 = ax3.scatter(np.array(xlist3),ylist3, c="red",linewidths=0)

    ax2.set_title('t = {: 5.2f} s'.format(step_g.time))
	
	# Save the figure
    fig.savefig('{}/Melt-{:05d}.png'.format(dirname, i), format='png', dpi=300)

    ax1.cla()
    ax2.cla()
    ax3.cla()	