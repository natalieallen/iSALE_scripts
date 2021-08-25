# this code reads the distance that set pressures occur from the center of isale simulations at given depths
import pySALEPlot as psp
import matplotlib.pyplot as plt
import numpy as np

# Create ouptut directory
dirname='Distance'
psp.mkdir_p(dirname)

# Open the datafile
model=psp.opendatfile('../Chicxulub/jdata.dat')

# Set the distance units to km
model.setScale('km')

# Set up a pyplot figure
fig=plt.figure()
ax=fig.add_subplot(111)

# Set the axis labels
ax.set_xlabel('Distance from impact point [km]')
ax.set_ylabel('Tracer Peak Pressure [GPa]')

# Set the axis limits
ax.set_xlim(0,150)
ax.set_ylim(0,60)

# Read the time steps from the datafile
step=model.readStep('TrP',140)

# interested in pressures at depths around 8 km, 9 km, 10 km (give some leeway around that value)
depth_8 = np.where((step.ymark < - 7.75) & (step.ymark > -8.25))
depth_9 = np.where((step.ymark < -8.75) & (step.ymark > -9.25))
depth_10 = np.where((step.ymark < -9.75) & (step.ymark > -10.25))

xval_8 = step.xmark[depth_8]
xval_9 = step.xmark[depth_9]
xval_10 = step.xmark[depth_10]

# Plot TrP as a function of the distance
trp_8 = step.TrP[depth_8]*1e-9
trp_9 = step.TrP[depth_9]*1e-9
trp_10 = step.TrP[depth_10]*1e-9

# plot the above recorded distances
ax.plot(np.sort(xval_8),trp_8[np.argsort(xval_8)],'--', label = "z=-8 km")
ax.plot(np.sort(xval_9),trp_9[np.argsort(xval_9)],'-.',label = "z=-9 km")
ax.plot(np.sort(xval_10),trp_10[np.argsort(xval_10)],':',label = "z=-10 km")
ax.legend()

# mark the pressures corresponding to some important impact morphology
ax.axhline(y=2, color = "cyan", label = "Begin: SH")
ax.axhline(y = 20, color = "m", label = "Begin: Zircon PF's")
ax.axhline(y=15,color = "y", label="Begin: PDFs")
ax.legend(loc=1)
fig.suptitle('{: 5.2f} s'.format(step.time))

# Save the figure
fig.savefig('DepthPlot.png', format='png', dpi=300)
