from bokeh.plotting import figure, output_notebook, show
from bokeh.layouts import column
from bokeh.palettes import Dark2_5 as palette
from control import *

def bode_overlay (freq_df, gain_df, phase_df, tflist, tfnames, **kwargs):
    
    #default colors assignment
    colors = palette
    
    if 'line_dash' not in kwargs.keys():
        line_dashes = ['0']*len(tflist)
        
    if 'line_dash' not in kwargs.keys():
        line_widths = [1]*len(tflist)
    
    # change styles if keywords exist
    for arg, value in kwargs.items():
        if arg == 'colors':
            colors = value
        if arg == 'line_dash':
            line_dashes = value
        if arg == 'line_width':
            line_widths = value
            
    
    mag = figure(width=600,height=200,x_axis_type='log', 
                background_fill_color="#fafafa",
                x_axis_label='Frequency [Hz]', y_axis_label='Gain [Ratio]',)

    mag.circle(freq_df,gain_df,color='black')
    mag.toolbar.logo = None
    mag.toolbar_location = None
    
    ph = figure(width=600,height=200,x_axis_type='log', 
                background_fill_color="#fafafa",
                x_axis_label='Frequency [Hz]', y_axis_label='Phase [deg]',)

    ph.circle(freq_df,phase_df,color='black')
    ph.toolbar.logo = None
    ph.toolbar_location = None

    for i, tf in enumerate(tflist):
        bm,bp,bf = bode_plot(tf,dB=True,Hz=True,omega_limits=(0.1,1000),margins=True,plot=False);
        # Convert phase from radians to degrees:
        bp = bp*180/np.pi
        # Convert magnitude to ratio:
        bm = bm
        # Convert freq from rad/s to Hz
        bf = bf/(2*np.pi)
        # Make the lines
        mag.line(bf,bm,legend_label=tfnames[i],color=colors[i], line_dash=line_dashes[i], line_width=line_widths[i])
        ph.line(bf,bp,color=colors[i], line_dash=line_dashes[i], line_width=line_widths[i])
    
    mag.legend.location = "bottom_left"
    mag.legend.label_text_font_size = "8pt"
    mag.legend.spacing = 1
    output_notebook()
    show(column(mag,ph))
    