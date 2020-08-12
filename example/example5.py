import matplotlib.pyplot as plt
import numpy as np
from lmfit import Minimizer, Parameters, report_fit

# for local imports include parent path for import of kMap classes
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

# now import classes from kMap
from kmap.library.orbital import Orbital
from kmap.library.sliceddata import SlicedData

# define common (kx,ky)-grid for deconvolution
dk = 0.05
kx = np.arange(-3.0,3.0,dk)
ky = kx

# read PTCDA orbitals from file and compute kmaps 
names  = ['PTCDA_C','PTCDA_D','PTCDA_E','PTCDA_F']
params = Parameters() # parameters object for minimization

sim_kmaps = []
for name in names:
    cuberead = open(name+'.cube').read()       # read cube-file from file
    orbital  = Orbital(cuberead,dk3D=0.15)     # 3D-FT 
    sim_kmap = orbital.get_kmap(E_kin=28,     
                         phi=0,theta=0,psi=0,  # Euler angles 
                         Ak_type='toroid',     # toroidal analyzer 
                         polarization='p',     # p-polarized light
                         alpha=60)             # angle of incidence
    sim_kmap.interpolate(kx,ky,update=True)
    sim_kmaps.append(sim_kmap)
    params.add(name,value=1,min=0)   # fit parameter weight of orbital

params.add('background',value=1, min=0)   # also use constant background as fit parameter

# Load experimental data-file: ARPES data of M3-feature of PTCDA/Ag(110)
exp_data = SlicedData.init_from_hdf5('example5_6584.hdf5') 

# define function to be minimized
def chi2_function(params,data):
    p = params.valuesdict()   
    sum_sim_kmap = np.zeros_like(data)
    for i, weight in enumerate(p):
        if weight != 'background':
            sum_sim_kmap += p[weight]*sim_kmaps[i].data    
    difference = sum_sim_kmap - (exp_kmap.data - p['background'])
    return difference

# main program
nslice = exp_data.data.shape[0]
pDOS   = np.zeros((nslice,len(names)+1))
for i in range(nslice):
    exp_kmap = exp_data.slice_from_index(i)  # get kmap slice from exp. data
    exp_kmap.interpolate(kx,ky,update=True)  # interpolate to common (kx,ky)-grid
    minner = Minimizer(chi2_function, params, fcn_kws={'data': exp_kmap.data}, nan_policy='omit')
    result = minner.minimize()
    pdir   = result.params.valuesdict()
    for j,p in enumerate(pdir):
        pDOS[i,j] = pdir[p]
#    report_fit(result)

# plot results: weights of orbitals (pDOS) vs. kinetic energy
fig,ax  = plt.subplots()
x       = exp_data.axes[0].axis
x_label = exp_data.axes[0].label + '(' + exp_data.axes[0].units + ')'
for j,p in enumerate(names):
    ax.plot(x,pDOS[:,j],label=p)
plt.legend()
plt.xlabel(x_label)
plt.xlabel('weights (arb. units)')
plt.show()

