***************************
SpikePlot Demo and Tutorial
***************************

This tutorial illustrates how to make spike raster plots using the 
:mod:`neuronpy.graphics.spikeplot` module. This document also exists as an
interactive worksheet on the NEURON Sage server: https://nn.med.yale.edu:8000.
Log onto the server and search the published worksheets for "SpikePlot demo".

Introduction
============

Spike trains are formatted as single vectors 
(Lists or 1D numpy arrays) or as 2D vectors (List of Lists or 2D numpy arrays). The 
elements of the vectors are the spike times. Plots are such that time is in the horizontal 
axis and each row is a given cell.

Basic example
=============

The following example shows the basic steps using some artificially created spikes. We 
simply create a SpikePlot object then plot the spikes.

::

    import numpy
    from neuronpy.graphics import spikeplot
    
    spikes = []
    num_cells = 10
    num_spikes_per_cell = 20
    frequency = 20
    
    # Make the spike data. Use a simple Poisson-like spike generator 
    # (just for illustrative purposes here. Better spike generators should 
    # be used in simulations).
    for i in range(num_cells):
        isi=numpy.random.poisson(frequency, num_spikes_per_cell)
        spikes.append(numpy.cumsum(isi))
        
    # spikes is now a list of lists where each cell has a list of spike
    # times. Now, let's plot these spikes.
    sp = spikeplot.SpikePlot(savefig=True)
    sp.plot_spikes(spikes)

Let's step through the details.

Import the module
=================

First, import the module.

::

    from neuronpy.graphics import spikeplot


Basic plot
==========

Plotting spike data requires an instance of a SpikePlot object. Instantiate the object and 
call :py:func:`~neuronpy.graphics.spikeplot.SpikePlot.plot_spikes`. (The object uses a 
``savefig=True``
option that makes drawing write to a file, which is required over the web. When using in a 
dynamic mode with matplotlib, you can leave this at its default value, which is False.)

::

    sp = spikeplot.SpikePlot(savefig=True)
    sp.plot_spikes(spikes)

In addition to noting that the tick marks are by default black vertical bars that just 
touches each other, there are a few things to note about this plot. In particular, 
SpikePlot uses `matplotlib <http://matplotlib.sourceforge.net/>`_ Figures. As such, this 
figure takes many Matplotlib.Figure and Axes defaults.


- The figure size is 8x6 inches.
- Axis tick marks are automatically generated.
- There are no axis labels, no title, and no legends.

We will add these elements and add/edit other properties of the spike plot as we progress 
throug the tutorial.

SpikePlot variables
===================

SpikePlot has several different variables below that can be set and retrieved: :ref:`marker`_

    * :ref:`marker`
    * :ref:`markercolor`
    * :ref:`markerscale`
    * :ref:`markeredgewidth`
    * :ref:`linestyle`
    * :ref:`linewidth`
    * :ref:`fig_name`
    * :ref:`figsize`
    * :ref:`figure and axes handles <figaxes>`
    * :ref:`Adding shaded regions <shaded>`

These variables are illustrated below. Python does not have the capability of hiding 
variables, so these variables are accessible directly as ``_<var_name>`` (note the 
underscore in front of the variable name). However, the ``set_<var_name>`` methods perform 
error checking to help ensure that the proposed variable value is valid, so use the 
accessor methods instead of setting the variable directly.

marker
------

By default, the marker is a vertical line. This can be changed to any valid
`Matplotlib.lines.Line2D marker \
<http://matplotlib.sourceforge.net/api/artist_api.html#matplotlib.lines.Line2D.set_marker>`_.
For example, the marker can be set to circles.

::

    # Make the marker filled circles.
    sp=spikeplot.SpikePlot(savefig=True, marker='.')
    sp.plot_spikes(spikes)

Note that this is equivalent to

::

    sp=spikeplot.SpikePlot(savefig=True)
    sp.set_marker('.')    # Make all subsequent marks circles
    sp.plot_spikes(spikes)

markercolor
-----------

The markercolor can be changed with any valid `Matplotlib color \
<http://matplotlib.sourceforge.net/api/colors_api.html>`_. This means strings like 
'red' and 'blue' can be used as well as RGB tuples and html strings. This sets the 
complete element to a solid color. There is no discrepancy between facecolor and edgecolor. 
If horizontal lines are shown (described below), this also colors the line with the same 
color.

::

    sp=spikeplot.SpikePlot(savefig=True)
    sp.set_markercolor('red')
    sp.plot_spikes(spikes)

markerscale
-----------

The markerscale corresponds to the height of the rows. With a default value of 1 and when 
vertical bars are used as the tick marks, each row just touches the other. With a value of 
0.5, the tick marks would be half as tall. In the previous examples using circle tick marks, 
the marks were quite large. Setting this value to a smaller value may help that issue. 
Additionally, larger values than 1 will bleed across rows, which may be desired in some 
situations.

::

    sp=spikeplot.SpikePlot(savefig=True)
    sp.set_markerscale(0.5)
    sp.plot_spikes(spikes)

markeredgewidth
---------------

The markeredgewidth also defines the size of the tick mark. By default, this has a value 
of 1. This can be made even smaller for sharper tick marks or larger to widen the mark. 
For example, here we set the width to 10.

::

    sp=spikeplot.SpikePlot(savefig=True)
    sp.set_markeredgewidth(10)
    sp.plot_spikes(spikes)


linestyle
---------

The linestyle defines the horizontal line that is drawn across each spike train. By 
default, the linestyle is ``None`` so that no lines are drawn. This can accept any 
linestyle defined by `Matplotlib.lines \
<http://matplotlib.sourceforge.net/api/artist_api.html#matplotlib.lines.Line2D.set_linestyle>`_, 
but for the most part, either ``None`` or ``'-'`` will be used.

::

    sp=spikeplot.SpikePlot(savefig=True)
    sp.set_linestyle('-')
    sp.set_markerscale(0.5)
    sp.plot_spikes(spikes)

linewidth
---------
When the linestyle is not ``None``, then a horizontal line is drawn. The width of that 
line can be set to be different from it's default value of 0.75.

::

    sp=spikeplot.SpikePlot(savefig=True)
    sp.set_linestyle('-')
    sp.set_linewidth(3)
    sp.set_markerscale(0.5)
    sp.plot_spikes(spikes)

fig_name
--------

The ``fig_name`` variable is "spikeplot.png" by default. Changing this to 
"<filename>.<format>" allows other options. Allowable file formats are largely determined 
by the graphics backend that is used, but for the most part, png, pdf, ps, eps and svg 
extensions are permitted.

This parameter raises an interesting point. When ``savefig=True``, 
:py:func:`~neuronpy.graphics.spikeplot.SpikePlot.plot_spikes` writes its output to 
a file, but this can be modified, as discussed later.

::

    sp=spikeplot.SpikePlot(savefig=True)
    sp.set_fig_name('myplot.pdf')
    sp.plot_spikes(spikes)

figsize
-------

The ``figsize`` parameter is a tuple of length 2 specifying the width and height of the 
figure in inches. By default, this is 8x6 (or to the value specified in the Matplotlib 
rc file). Avoid setting this value by getting the figure handle and setting the size. Use 
the :py:func:`~neuronpy.graphics.spikeplot.SpikePlot.set_figsize` method, or start with 
the desired output size as the parameter.

::

    sp=spikeplot.SpikePlot(savefig=True, figsize=(6,2))
    sp.plot_spikes(spikes)

.. _figaxes
figure and axes handle
----------------------

It is possible to pass a figure handle to the SpikePlot object as well as an axes object. 
This can be useful for specifying titles, axis labels, tick marks, and general layout.

The following example creates a figure and axes, then sets an axes title, a x-axis label, 
and removes the ticklabels and tick marks from the vertical axis.

::

    from matplotlib import pyplot
    # Pre-process some figure variables
    fig_handle=pyplot.figure(figsize=(6,2))
    ax=fig_handle.add_subplot(111)
    ax.set_title('Pre-formatted figure')
    ax.set_xlabel('$t$ (ms)') # Note LaTeX
    ax.set_yticks([])
    
    # Now pass the figure handle to SpikePlot.
    # The spike_axes will be set to the first axes object assigned to the figure
    sp=spikeplot.SpikePlot(savefig=True, fig=fig_handle)
    sp.plot_spikes(spikes)

Well, the title is clipped and the xlabel is not even visible. Adjust the axes size.

::

    fig_handle=pyplot.figure(figsize=(6,2))
    ax=fig_handle.add_subplot(111)
    ax.set_title('Pre-formatted figure')
    ax.set_xlabel('$t$ (ms)') # Note LaTeX
    ax.set_yticks([])
    
    #### Next lines are new
    pos=ax.get_position()
    ax.set_position([pos.xmin, pos.ymin+.1, pos.width, pos.height-.15])
    
    # Now pass the figure handle to SpikePlot.
    # The spike_axes will be set to the first axes object assigned to the figure
    sp=spikeplot.SpikePlot(savefig=True, fig=fig_handle)
    sp.plot_spikes(spikes)

That's better.

We can also work backwards by plotting the spikes and then doing some post-processing 
formatting. This requires getting the figure handle and spike_axes from the SpikePlot 
object and manipulating them. After any manipulation to the axes, the SpikePlot object 
needs to be told so that it can adjust the spike rasters properly. Additionally, we do not 
draw the figure to a file when we call 
:py:func:`~neuronpy.graphics.spikeplot.SpikePlot.plot_spikes`, which normally writes a 
file. So we do not initialize SpikePlot with a ``savefig=True``, but then write the 
file later.

::

    sp=spikeplot.SpikePlot() # No need for SpikePlot to write a file yet
    sp.plot_spikes(spikes)
    
    # Post-processing
    fig_handle=sp.get_fig()
    fig_handle.set_size_inches(6,2)
    ax=sp.get_raster_axes()
    ax.set_title('Post-formatted figure')
    ax.set_xlabel('$t$ (ms)') # Note LaTeX
    ax.set_yticks([])
    pos=ax.get_position()
    ax.set_position([pos.xmin, pos.ymin+.1, pos.width, pos.height-.15])
    
    # After modifying the spike_axes, be sure to update the SpikePlot object
    sp.set_raster_axes(ax)
    
    # Actually draw and write the file
    fig_handle.savefig(sp.get_fig_name())

.. _shaded
Shaded regions
--------------

Another useful thing to do in post-processing the figure may be to add some shaded region 
as in the following example.

::

    from matplotlib import patches
    
    sp=spikeplot.SpikePlot() # No need for SpikePlot to write a file yet
    sp.plot_spikes(spikes)
    
    # Post-processing
    fig_handle=sp.get_fig()
    fig_handle.set_size_inches(6,2)
    ax=sp.get_raster_axes()
    ax.set_title('Post-formatted figure')
    ax.set_xlabel('$t$ (ms)') # Note LaTeX
    ax.set_yticks([])
    pos=ax.get_position()
    ax.set_position([pos.xmin, pos.ymin+.1, pos.width, pos.height-.15])
    
    #### Highlight
    left = 100
    bottom = 0
    width = 200
    ylim = ax.get_ylim()
    height = ylim[1] - ylim[0] + 1
    rect = patches.Rectangle( (left, bottom), width, height, linewidth=0, alpha=0.2, facecolor=(0,0,1))
    ax.add_patch(rect)
    
    # After modifying the spike_axes, be sure to update the SpikePlot object
    sp.set_raster_axes(ax)
    
    # Actually draw and write the file
    fig_handle.savefig(sp.get_fig_name())

Multiple trains
===============

We can write multiple trains by either overlaying a second set of spikes on top of the 
original set, or by stacking. This first example creates a second set of spikes and draws 
them red, overlaying the black train. Under the hood, spike data and drawing formats are 
overwritten with new rendering commands. This means if we called 
:py:func:`~neuronpy.graphics.spikeplot.SpikePlot.plot_spikes` with more spikes, it would 
erase the previous data. To get around this, we now call 
:py:func:`~neuronpy.graphics.spikeplot.SpikePlot.plot_spikes` with different labels.

::

    # Create a second list of spikes
    spikes2 = []
    num_cells = 10
    num_spikes_per_cell = 20
    frequency = 20
    
    # Make the spike data. Use a simple Poisson-like spike generator 
    # (just for illustrative purposes here. Better spike generators should 
    # be used in simulations).
    for i in range(num_cells):
        isi=numpy.random.poisson(frequency, num_spikes_per_cell)
        spikes2.append(numpy.cumsum(isi))

Plot with different labels.

::

    # Draw the first spikes as before, but set draw to False so that we do 
    # not draw to the screen with this plot_spikes call, but wait until 
    # later, when we have drawn all spike traces to draw to the screen.
    sp=spikeplot.SpikePlot(savefig=True)
    sp.plot_spikes(spikes, label='black spikes', draw=False)
    
    # Make subsequent marks red
    sp.set_markercolor('red')
    sp.plot_spikes(spikes2, label='red spikes')

To stack plots, you have to provide a ``cell_offset`` value on any subsequent sets.

::

    # Make the marker filled circles.
    sp=spikeplot.SpikePlot(savefig=True)
    sp.set_markerscale(0.5)
    sp.set_marker('.')
    
    # Set draw to false so that we do not draw to the screen now, but
    # wait until later, when we have drawn all spike traces.
    # Make new marks black
    sp.set_markercolor('black')
    sp.plot_spikes(spikes, label='black', draw=False)
    
    # Make subsequent marks red
    sp.set_markercolor('red')
    
    # Set refresh to False so that old marks are not erased.
    sp.plot_spikes(spikes2, label='red', cell_offset=len(spikes))


.. _largedata
Large Data and telescoping
--------------------------

In general, if you are navigating large data, you may try and load it all into the figure 
and then specify the subset of columns (a chunk of time) to see. This is possible using 
:py:func:`~neuronpy.graphics.spikeplot.SpikePlot.update_xlim` method. The following example 
illustrates this.

::

    sp=spikeplot.SpikePlot(savefig=True)
    sp.plot_spikes(spikes)
    sp.update_xlim((100, 200)

.. ifconfig:: sagebuild

    As a better example with large data, we can execute the following code that loads 
    spikes that have been pickled.
    
    ::
    
        import pickle
        with open('data/spikes.p', 'r') as pickle_file: # Open the file for reading
            large_spikes = pickle.load(pickle_file) # Load the pickled contents
    
    Plot that data and interact with it.    
    
    ::
    
        var('zoom')
        var('translation')
        zoom_list=[]
        for i in range(21):
            zoom_list.append(math.sqrt(2.)**i)
            
        sp_large = spikeplot.SpikePlot(savefig=True)
        sp_large.plot_spikes(large_spikes)
        
        @interact
        def _(zoom = slider(zoom_list), \
        center=slider(range(sp_large._axes_lim[1]),default=\
                (sp_large._axes_lim[1]-sp_large._axes_lim[0])/2+sp_large._axes_lim[0])):
            range = sp_large._axes_lim[1]-sp_large._axes_lim[0]
            window_width = range/zoom
            dim_x=int(window_width/2)
            x_min=center-dim_x
            x_max=center+dim_x
            sp_large.update_xlim((int(x_min),int(x_max)))

Spike time histograms
=====================

Adding a spike time histogram to an existing plot is quite easy.

::

    sp=spikeplot.SpikePlot(sth_ratio=0.2, savefig=True, figsize=(8,4))
    sp.plot_spikes(spikes)

Adding the argument ``sth_ratio=0.2`` in the code above creates a spike time histogram 
and sets it to occupy 20% of the vertical space. Try other values, such as 0.5. The bins 
are quantized by 1 ms by default. The code below grabs the spike time histogram object and 
sets it's bars' timestep (dt) to 10 ms.

::

    sp=spikeplot.SpikePlot(sth_ratio=0.2, savefig=True, figsize=(8,4))
    sth = sp.get_sth()
    sth.set_dt(10)
    sp.plot_spikes(spikes)

There are four types of bar styles for the histogram: 'bar' (default), 'stepfilled', 
'step', and 'lineto'.

::

    sp=spikeplot.SpikePlot(sth_ratio=0.2, savefig=True, figsize=(8,4))
    sth = sp.get_sth()
    sth.set_dt(10)
    sth.set_style('stepfilled')
    sp.plot_spikes(spikes)

::

    sp=spikeplot.SpikePlot(sth_ratio=0.2, savefig=True, figsize=(8,4))
    sth = sp.get_sth()
    sth.set_dt(10)
    sth.set_style('step')
    sp.plot_spikes(spikes)

::

    sp=spikeplot.SpikePlot(sth_ratio=0.2, savefig=True, figsize=(8,4))
    sth = sp.get_sth()
    sth.set_dt(10)
    sth.set_style('lineto')
    sp.plot_spikes(spikes)

::

    sp=spikeplot.SpikePlot(sth_ratio=0.2, savefig=True, figsize=(8,4))
    sth = sp.get_sth()
    sth.set_dt(10)
    sth.set_style('step')
    sp.plot_spikes(spikes, label='black spikes')
    sp.set_markercolor('red')
    sp.plot_spikes(spikes2, label='red spikes')

The histogram can also be considered a 1D vector of values. In this case, it can be 
filtered for various effect. This is useful in cases where a small time window (dt) is used 
for the histogram, but where you want to blur or smear the spikes in time with a gaussian 
or linear function, say. The mechanism used to filter is a 1D kernel. Kernels should 
sum to 1, but you can turn this flag off if you want. The following example makes a 
linearly decaying kernel that makes each spike reach 0 in 10 ms. This example also only 
uses a few spikes in one spike train so that you can see the effects of modifying dt and 
the kernel origin, which can be in the range :math:`\left[-\mathrm{len}(\mathrm{kernel})/2, 
\mathrm{len}(\mathrm{kernel})/2\right]`, or the values 'left', 'center', and 'right'.

::

    sp=spikeplot.SpikePlot(sth_ratio=0.2, savefig=True, figsize=(8,4))
    sp.set_markercolor('red')
    sth = sp.get_sth()
    sth.set_dt(.1) # Small time window
    kernel = numpy.linspace(1, 0., 10/sth._dt) # Linear ramp over 10 ms
    kernel = numpy.divide(kernel, numpy.sum(kernel)) # Normalize
    sth.set_kernel(kernel)
    sth.set_style('lineto')
    sth.set_origin('left')

    sp.plot_spikes([[5, 20, 35, 45]])

::

    sp=spikeplot.SpikePlot(sth_ratio=0.2, savefig=True, figsize=(8,4))
    sp.set_markercolor('red')
    sth = sp.get_sth()
    sth.set_dt(.1) # Small time window
    kernel = numpy.linspace(1, 0., 10/sth._dt) # Linear ramp over 10 ms
    kernel = numpy.divide(kernel, numpy.sum(kernel)) # Normalize
    sth.set_kernel(kernel)
    sth.set_style('lineto')
    sth.set_origin('left')
    
    sp.plot_spikes(spikes)

::

    from neuronpy.math import kernel
    sp=spikeplot.SpikePlot(sth_ratio=0.2, savefig=True, figsize=(8,4))
    sp.set_markercolor('red')
    sth = sp.get_sth()
    dt = .1
    sth.set_dt(dt) # Small time window
    k = kernel.gauss_1d(2, dt)
    sth.set_kernel(k)
    sth.set_style('lineto')
    sth.set_origin('center')
    
    sp.plot_spikes(spikes)

::

    sp=spikeplot.SpikePlot(sth_ratio=0.2, savefig=True, figsize=(8,4))
    sth = sp.get_sth()
    dt = .1
    sth.set_dt(dt) # Small time window
    k = kernel.gauss_1d(2, dt)
    sth.set_kernel(k)
    sth.set_style('lineto')
    sth.set_origin('center')
    sp.plot_spikes(spikes, label='black spikes')
    sp.set_markercolor('red')
    sp.plot_spikes(spikes2, label='red spikes')
