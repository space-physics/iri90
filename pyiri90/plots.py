from matplotlib.pyplot import figure,show
from pandas import DataFrame

def summary(iono,R,latlon,dtime):
    assert isinstance(iono,DataFrame)

    zkm = iono.index # altitude

    Ne = iono['ne']
    dNe = Ne.diff()

    ax = figure().gca()
    ax.plot(Ne,zkm,'b',label='$N_e$')
    ax2 = ax.twiny()
    #ax2.plot(dNe,zkm,'r',label='$ \partial N_e/\partial z $')
    ax2.plot(R,zkm,'r',label='$\Gamma$')
    ax.legend()
    ax2.legend(loc='right')

    ax.set_ylabel('altitude [km]')
    ax.set_xlabel('Number Density')

    ax.autoscale(True,'y',True)
    ax.set_title('({}, {})  {}'.format(latlon[0],latlon[1],dtime),y=1.05)