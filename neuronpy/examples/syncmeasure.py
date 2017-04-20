# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 14:26:30 2011

@author: -
"""
import sys
import numpy
from matplotlib import pyplot
from neuronpy.util import spiketrain
from neuronpy.graphics import spikeplot

class Correlogram:
    def __init__(self, ref=None, comp=None, fig=None, figsize=None, axlim = (0,500)):
        self.ref = ref
        self.comp = comp
        self.fig = fig
        self.figsize = figsize
        self.axlim = axlim
        self.raster_ax = None
        #self.rect_ax = None
        self.correlogram_ax = None
        self.t = 0
    
    def initfig(self):
        if self.fig is None:
            self.fig = pyplot.figure(figsize=self.figsize)
        self.raster_ax = self.fig.add_axes([.1, .8, .8, .15])
        #self.convolve_ax = self.fig.add_axes([.1, .65, .8, .1])
        self.correlogram_ax = self.fig.add_axes([.1, .1, .8, .55])
    
    def inittrains(self, r=15):
        if self.ref is None:
            self.gen_spikes(r=r)
            
    def gen_spikes(self, num_spikes=20, isi=50, r=15, comp_shift=0):
        """Generate spike trains by having them at a set frequency, then
        shift each spike by some uniform value. Also slide train b by some
        amount in time."""
        self.ref=numpy.ones(num_spikes)
        self.ref=numpy.multiply(self.ref,isi)
        self.ref=numpy.cumsum(self.ref)
        self.comp=numpy.ones(num_spikes)
        self.comp=numpy.multiply(self.comp,isi)
        self.comp=numpy.cumsum(self.comp)
        off_ref = numpy.random.uniform(-r,r,num_spikes)
        self.ref = numpy.add(self.ref, off_ref)
        off_comp = numpy.random.uniform(-r,r,num_spikes)
        self.comp = numpy.add(self.comp, off_comp)
        self.comp = numpy.add(self.comp, isi*comp_shift)
        while self.ref[-1] >= self.axlim[1]-2:
            self.ref = self.ref[:-1]
        while self.comp[-1] >= self.axlim[1]-2:
            self.comp = self.comp[:-1]

        #self.ref = numpy.multiply([i for i in spiketrain.poisson_train(20, 1, seed=2)], 1000.)

    
    def plot_spikes(self):
        self.raster_ax.clear()
        sp = spikeplot.SpikePlot(fig=self.fig, savefig=False)
        sp.set_markercolor('red')
        sp.set_markeredgewidth(2.)
        sp.plot_spikes([self.ref], label='ref', draw=False, )
        sp.set_markercolor('blue')
        sp.plot_spikes([self.comp + self.t], label='comp', cell_offset=1, draw=False )
        coincidences, mask_a, mask_b, ratio = \
                spiketrain.get_sync_traits( self.ref, self.comp+self.t, window=5)
        idx = 0
        for i in mask_a:
            if i == 1:
                self.raster_ax.plot([self.ref[idx]],[.6], marker='o', color='red')
            idx += 1
        idx = 0
        for i in mask_b:
            if i == 1:
                self.raster_ax.plot([self.comp[idx]+self.t],[2.4], marker='o', color='blue')
            idx += 1
        self.raster_ax.set_yticks([1,2])
        self.raster_ax.set_yticklabels(['','%+.1f ms'%self.t])
        self.raster_ax.set_xlim(self.axlim)        

#    def plot_rect(self):
#        dt = 1
#        filtered_ref = spiketrain.filter(self.ref, kernel=numpy.ones(5/dt)/5.*dt, dt=dt, window=self.axlim)
#        x = numpy.arange(len(filtered_ref))*dt
#        #self.rect_ax.plot(x, filtered_ref, color='red')
#        self.raster_ax.plot(x, (filtered_ref*2/dt) + .5, color='red')
#        filtered_comp = spiketrain.filter(self.comp, kernel=numpy.ones(5/dt)/5.*dt, dt=dt, window=self.axlim)
#        x = numpy.arange(len(filtered_comp))*dt
#        #self.rect_ax.plot(x, filtered_comp + dt/4, color='blue')
#        #self.rect_ax.set_xlim(self.axlim)
#        self.raster_ax.plot(x, (filtered_comp*2/dt) + 1.5, color='blue')
#        self.fig.savefig('temp.pdf')
#        
#    def plot_convolve(self):
#        the_len = 4
#        headtail = numpy.zeros(2)
#        rect = numpy.ones(the_len)
#        convolved = numpy.convolve(rect, rect)
#        start = 0
#        for i in range(2):
#            self.convolve_ax.plot(range(start, start + len(headtail)), headtail, color='black', linewidth=2)
#            start += len(headtail)-1
#            self.convolve_ax.plot([start, start], [0, 1], color='black', linewidth=2)
#            self.convolve_ax.plot(range(start, start + len(rect)), rect, color='black', linewidth=2)
#            start += len(rect) - 1
#            self.convolve_ax.plot([start, start], [0, 1], color='black', linewidth=2)
#            self.convolve_ax.plot(range(start, start + len(headtail)), headtail, color='black', linewidth=2)
#            start += len(headtail) - 1
#            start += len(headtail)
#
#        self.convolve_ax.plot(range(start, start + len(convolved)), convolved, color='black', linewidth=2)
#        self.convolve_ax.set_xticks([])
#        self.convolve_ax.set_yticks([])
#        self.convolve_ax.spines['left'].set_color('none')
#        self.convolve_ax.spines['right'].set_color('none')
#        self.convolve_ax.spines['top'].set_color('none')
#        self.convolve_ax.spines['bottom'].set_color('none')
        
    def plot_coincident_point(self):
        self.correlogram_ax.clear()
        coincidences, expected_coincidences, total_spikes = \
                spiketrain.coincident_spikes(self.ref, self.comp+self.t)
        val = float(coincidences)/float(total_spikes)*2
        print "val=", val, "t=", self.t
        self.correlogram_ax.scatter([self.t],[val])
        self.correlogram_ax.set_xlim((-10,10))
        self.correlogram_ax.set_ylim((0,1.02))
        self.correlogram_ax.set_xlabel('lag (ms)')
        self.correlogram_ax.set_ylabel('Synchronized fraction')
        self.correlogram_ax.set_title('%d coincidences out of %d spikes' %(2*coincidences, total_spikes))
        self.correlogram_ax.grid()
        
    def do_all(self):
        self.initfig()
        self.inittrains(r=4)
        for self.t in numpy.linspace(-7.5,7.5,7):
            self.plot_spikes()
            self.plot_coincident_point()
            self.fig.savefig('temp_%.1f.pdf' %self.t)

def run(argv):
    cg = Correlogram()
    cg.do_all()
    
if __name__ == '__main__':
    run(sys.argv[1:])