# this code makes a series of three pressure contour plots for three isale simulations
import pySALEPlot as psp
import matplotlib.pyplot as plt
import matplotlib as mpl
from numpy import arange,sqrt,ma
import numpy as np
import matplotlib as mpl
from matplotlib.patches import ConnectionPatch

# setting plotting variables
font = {'size':20}
mpl.rc('font',**font)
plt.rc('xtick',labelsize=20)
mpl.rcParams["axes.linewidth"] = 2.5

# If viridis colormap is available, use it here
try:
    plt.set_cmap('viridis')
except:
    plt.set_cmap('YlGnBu_r')

# Make an output directory
dirname='Triple Pressure'
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
fig=plt.figure(figsize=(17,12))

# more plotting variables
ax1=fig.add_subplot(311,aspect='equal')
ax2=fig.add_subplot(312,aspect='equal')
ax3=fig.add_subplot(313,aspect='equal')
plt.setp(ax1.get_xticklabels(), fontsize=20)
plt.setp(ax2.get_xticklabels(), fontsize=20)
plt.setp(ax3.get_xticklabels(), fontsize=20)
plt.setp(ax1.get_yticklabels(), fontsize=20)
plt.setp(ax2.get_yticklabels(), fontsize=20)
plt.setp(ax3.get_yticklabels(), fontsize=20)
ax1.tick_params(width = 2.5)
ax2.tick_params(width = 2.5)
ax3.tick_params(width = 2.5)

# Loop over timesteps - currently defined just for one specific timestamp, but can easily be changed to 
# plot a series of timesteps by changing the arange values
for i in arange(200,202,2):

    # Read the time step 'i' from the datafile: 
    # read two or more fields by making a list of their abbreviations
    step_i=model_i.readStep('TrP',i)
    step_g=model_g.readStep('TrP',i)
    step_b=model_b.readStep('TrP',i)
    
    # setting up the surface
    p1=ax1.pcolormesh(model_g.x,model_g.y,step_g.mat,
            cmap='pink',vmin=1,vmax=model_g.nmat+1, alpha = 0.25)
    p2=ax2.pcolormesh(model_b.x,model_b.y,step_b.mat, cmap='pink',
            vmin=1,vmax=model_b.nmat+1, alpha =0.25)
    p3=ax3.pcolormesh(model_i.x,model_i.y,step_i.mat, cmap='pink',
            vmin=1,vmax=model_i.nmat+1, alpha = 0.25)
    
    # Material boundaries
    [ax1.contour(model_g.xc,model_g.yc,step_g.cmc[mat],1,colors='k',linewidths=0.5) for mat in [0,1,2]]
    [ax2.contour(model_b.xc,model_b.yc,step_b.cmc[mat],1,colors='k',linewidths=0.5) for mat in [0,1,2]]
    [ax3.contour(model_i.xc,model_i.yc,step_i.cmc[mat],1,colors='k',linewidths=0.5) for mat in [0,1,2]]
   
    # some initializing for the contour plots
	xvals_g = step_g.xmark[step_g.ymark<10]
	yvals_g = step_g.ymark[step_g.ymark<10]
	triang_g = mpl.tri.Triangulation(xvals_g,yvals_g)

	# these are to make horizontal lines to mark today's erosion level
	ax1.axhline(y=-8, linewidth = 2)
	ax1.axhline(y=-11, linewidth = 2)

    # creating the contours - here I manually set the levels to 5, 10, 25, 40 GPa
	c_g = ax1.tricontour(triang_g,step_g.TrP[step_g.ymark<10],levels=[5e9,10e9,25e9,40e9], colors="black")
	fmt={}
	strs =["5","10","25","40"]
	for l,s in zip(c_g.levels,strs):
		fmt[l]=s
	
    # here I set manual locations for the contour labels (manual_locations=[(87,-59),(48,-56),(25,-42)])
	# can just set to auto instead of manual if you want them auto-placed, but it can get messy
	ax1.clabel(c_g,c_g.levels[::1],inline=True,fmt=fmt,fontsize=10, manual = ((80,-20),(60,-22),(28,-30),(12,-18)))
	
    # doing the same as above for the second contour plot
	xvals_b = step_b.xmark[step_b.ymark<10]
	yvals_b = step_b.ymark[step_b.ymark<10]
	triang_b = mpl.tri.Triangulation(xvals_b,yvals_b)
	ax2.axhline(y=-8, linewidth = 2)
	ax2.axhline(y=-11, linewidth = 2)
	
	c_b = ax2.tricontour(triang_b,step_b.TrP[step_b.ymark<10],levels=[5e9,10e9,25e9,40e9], colors="black")
	fmt={}
	strs =["5","10","25","40"]
	for l,s in zip(c_b.levels,strs):
		fmt[l]=s
	#manual_locations=[(87,-59),(48,-56),(25,-42)]
	ax2.clabel(c_b,c_b.levels[::1],inline=True,fmt=fmt,fontsize=10, manual=((80,-20), (60,-25),(30,-28),(11,-20)))
    
    # doing the same as above for the third contour plot
	xvals_i = step_i.xmark[step_i.ymark<10]
	yvals_i = step_i.ymark[step_i.ymark<10]
	triang_i = mpl.tri.Triangulation(xvals_i,yvals_i)
	ax3.axhline(y=-8, linewidth = 2)
	ax3.axhline(y=-11, linewidth = 2)
	
	c_i = ax3.tricontour(triang_i,step_i.TrP[step_i.ymark<10],levels=[5e9,10e9,25e9,40e9], colors="black")
	fmt={}
	strs =["5","10","25"]
	for l,s in zip(c_i.levels,strs):
		fmt[l]=s
	#manual_locations=[(87,-59),(48,-56),(25,-42)]
	ax3.clabel(c_i,c_i.levels[::1],inline=True,fmt=fmt,fontsize=10, manual=((50,-20),(30,-25),(15,-18)))
	
	# Setting labels and limits
    ax1.set_ylabel('z [km]')
    ax1.text(91,1,'Model A')
    ax2.set_ylabel('z [km]')
    ax2.text(91,1,'Model B')
    ax3.set_xlabel('r [km]', labelpad=30)
    ax3.set_ylabel('z [km]')
    ax3.text(91,1,'Model C')

    ax1.set_aspect("auto")
    ax1.set_xlim([0,100])
    ax1.set_ylim([-40,5])

    ax2.set_aspect("auto")
    ax2.set_xlim([0,100])
    ax2.set_ylim([-40,5])

    ax3.set_aspect("auto")
    ax3.set_xlim([0,100])
    ax3.set_ylim([-40,5])
    ax1.set_title('t = {: 5.2f} s'.format(step_g.time))
    
    # setting the location of horizontal lines to define outer limits of geologic evidence
    ax3.axvline(x=9,ymin=0.019,ymax=3.382,linewidth=10,color="red",alpha=0.7,clip_on=False,zorder=1000)
    ax3.axvline(x=45,ymin=0.019,ymax=3.382,linewidth=10,color="purple",alpha=0.7,clip_on=False,zorder=1000)
    ax3.axvline(x=90,ymin=0.019,ymax=3.382,linewidth=10,color="green",alpha=0.7,clip_on=False,zorder=1000)
    ax3.text(9,-50,"Melt\n(60-100 GPa)",ha="center")
    ax3.text(45,-50,"PDFs\n(8-25 GPa)",ha="center")
    ax3.text(90,-50,"Shatter Cones\n(2-10 GPa)",ha="center")

	# Save the figure
    fig.savefig('{}/Pressure-{:05d}.png'.format(dirname, i), format='png', dpi=300)

    ax1.cla()
    ax2.cla()
    ax3.cla()	
