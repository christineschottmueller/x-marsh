.. code:: ipython3

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import savgol_filter
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch, FancyArrowPatch, Rectangle, Ellipse
    from matplotlib.gridspec import GridSpec
    import seaborn as sns

Figure 3 - top row
------------------

Simulated marsh-accretion trajectories for different sea level rise rates
-------------------------------------------------------------------------

Illustration of the effects of two management strategies (L) — marsh
conservation (top) and marsh restoration (bottom) for a fixed set of
categorical input parameters and the high and low emissions sea level
rise scenarion RCP8.5 and RCP2.6 (X) on marsh accretion rates.

Load plotting data
~~~~~~~~~~~~~~~~~~

Plotting data: Simulated time-series (6 accretion models) of annual
growth rate in the pioneer zone in focus area S15 with **fixed
categorical parameter set**. The simulations were performed using inputs
from the high and low emissions sea level rise scenarios RCP2.6 and
RCP8.5. The applied policy is conservation.

Categorical Parameter Set Used
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``z_init = 0.7``
- ``c_flood = 0.05``
- ``fd = 0.6``
- ``s_subsidence = 0.003``
- ``rho_deposit = 400``
- ``c_flood_nourishment = 0.0``
- ``nourishment_frequency = 1``

The **data** used in figure 3 is contained in the folder
**figure_3_data**.

.. code:: ipython3

    result_low_26 = pd.read_csv('../data/figure_3_data/fig_3_top_result_low_26.txt', sep='\t')
    result_mean_26 = pd.read_csv('../data/figure_3_data/fig_3_top_result_mean_26.txt', sep='\t')
    result_high_26 = pd.read_csv('../data/figure_3_data/fig_3_top_result_high_26.txt', sep='\t')

.. code:: ipython3

    result_low_85 = pd.read_csv('../data/figure_3_data/fig_3_top_result_low_85.txt', sep='\t')
    result_mean_85 = pd.read_csv('../data/figure_3_data/fig_3_top_result_mean_85.txt', sep='\t')
    result_high_85 = pd.read_csv('../data/figure_3_data/fig_3_top_result_high_85.txt', sep='\t')

.. code:: ipython3

    rcp_data = pd.read_csv('../data/figure_3_data/regional_slr_ar5.txt', sep='\t')

.. code:: ipython3

    df = pd.read_csv('../data/figure_3_data/bars_top.txt', sep='\t')

Smoothen time-series for plotting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    # Apply Savitzky-Golay filter
    window_size = 10  # Window size must be odd
    poly_order = 1
    smoothed_mean_26 = savgol_filter(result_mean_26['dz_dt'], window_size, poly_order)
    smoothed_high_26 = savgol_filter(result_high_26['dz_dt'], window_size, poly_order)
    smoothed_low_26 = savgol_filter(result_low_26['dz_dt'], window_size, poly_order)
    
    smoothed_mean_85 = savgol_filter(result_mean_85['dz_dt'], window_size, poly_order)
    smoothed_high_85 = savgol_filter(result_high_85['dz_dt'], window_size, poly_order)
    smoothed_low_85 = savgol_filter(result_low_85['dz_dt'], window_size, poly_order)
    
    

Plot command
~~~~~~~~~~~~

.. code:: ipython3

    from matplotlib.gridspec import GridSpec
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D  # Import for custom legend entries
    import seaborn as sns
    
    # Create two subplots (row, 2 columns)
    fig,(ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6), gridspec_kw={'width_ratios': [1, 1, 0.2]})
    
    ##########################################################
    #######        First Plotting Window       ###############
    # Plot accretion rate vs year
    #ax1.set_title('Sedimentation rate for yearly timestep')
    
    
    ### RCP 2.6
    ### marsh-growth
    p1_26 = ax1.plot(result_low_26['year'],smoothed_mean_26, linestyle='--', color='#79BCFF')
    ax1.fill_between(rcp_data['year'], smoothed_low_26, smoothed_high_26, color='#DDA63A', alpha=0.4)
    
    ### RCP 8.5
    ### marsh-growth
    p1_85 = ax1.plot(result_mean_85['year'], smoothed_mean_85, linestyle='--', color='#FF0000')
    ax1.fill_between(rcp_data['year'], smoothed_low_85, smoothed_high_85, color='#8C6518', alpha=0.4)
    
    ax1.set_xlim(2044, 2100)
    ax1.set_ylim(-0.006, 0.008)
    ###############    Customize legend    ####################
    #Create an invisible fill to use in the legend.
    p2_26 = ax1.fill(np.NaN, np.NaN,  color='#DDA63A', alpha=0.4)
    p2_85= ax1.fill(np.NaN, np.NaN,  color='#8C6518', alpha=0.4)
    
    
    handles = [(p1_26[0], p2_26[0]), (p1_85[0], p2_85[0])]
    labels = [r'Growth rate $_{RCP 2.6}$', r'Growth rate$_{RCP 8.5}$']
    
    
    ax1.legend(handles, labels, handleheight=1, loc='best',frameon=False, prop={'size': 14})
    
    ax1.set_ylabel('increment [meter]')
    ax1.grid(True)
    
    ax1.annotate(
        r'a)', 
        xy=(2047, -0.0050), 
        xytext=(2047, -0.0055),  # Position of text slightly above and to the right
        ha='center',fontsize=22
    )
    
    
    ###########################################################
    #######        Second Plotting Window       ###############
    # Plot elevation above sea level versus year
    
    ### RCP 2.6
    ### marsh-growth
    p1_26_E = ax2.plot(rcp_data['year'], result_mean_26['elevation'], label=r'$z_{marsh}$',  linestyle='--', color='#79BCFF')
    ax2.fill_between(rcp_data['year'], result_low_26['elevation'], result_high_26['elevation'], color='#DDA63A', alpha=0.4)
    
    ax2.plot(rcp_data['year'], result_high_85['elevation'], label=r'$z_{marsh}$',linestyle='dotted', color='black')
    
    ### sea-level-rise
    p1_26_slr = ax2.plot(rcp_data['year'], rcp_data['mean_26'], linestyle='-', color='#79BCFF',linewidth=2)
    ax2.fill_between(rcp_data['year'], rcp_data['min_26'], rcp_data['max_26'], color='#79BCFF', alpha=0.2)
    
    
    
    #### RCP 8.5
    ### marsh-growth
    p1_85_E = ax2.plot(rcp_data['year'], result_mean_85['elevation'], label=r'$z_{marsh}$',linestyle='--', color='#FF0000')
    ax2.plot(rcp_data['year'], result_high_85['elevation'], label=r'$z_{marsh}$',linestyle='dotted', color='black')
    ax2.fill_between(rcp_data['year'], result_low_85['elevation'], result_high_85['elevation'], color='#8C6518', alpha=0.4)
    
    ### sea-level-rise
    p1_85_slr = ax2.plot(rcp_data['year'], rcp_data['mean_85'],  linestyle='-', color='#FF0000',linewidth=2)
    ax2.fill_between(rcp_data['year'], rcp_data['min_85'], rcp_data['max_85'], color='#FF0000', alpha=0.2)
                     
                     
    ax2.set_xlim(2044, 2100)
    ax2.set_ylim(0.17, 1.2)
    
    ###############    Customize legend    ####################
    #Creates an invisible fill to use in the legend.
    ### Elevation
    p2_26_E = ax1.fill(np.NaN, np.NaN,  color='#DDA63A', alpha=0.4)
    p2_85_E= ax1.fill(np.NaN, np.NaN,  color='#8C6518', alpha=0.4)
    
    ### SLR
    p2_26_slr = ax2.fill(np.NaN, np.NaN,  color='#79BCFF', alpha=0.2)
    p2_85_slr = ax2.fill(np.NaN, np.NaN,  color='#FF0000', alpha=0.4)
    
    
    vertical_line_handle = Line2D([0], [0], color='black', linestyle='dotted', linewidth=1.3)  # Explicitly create the handle
    handles = [(p1_26_slr[0], p2_26_slr[0]), (p1_85_slr[0], p2_85_slr[0]), vertical_line_handle, (p1_26_E[0], p2_26_E[0]), (p1_85_E[0], p2_85_E[0])]
    labels = [r'Sea level $_{RCP 2.6}$', r'Sea level $_{RCP 8.5}$', r'Most critical', r'Elevation $_{RCP 2.6}, conservation$',
              r'Elevation $_{RCP 8.5}, conservation$' ]
    ax2.legend(handles, labels, ncol=2, handleheight=1, prop={'size': 14},loc='upper left',frameon=False )
    
    ax2.set_ylabel('[meter]')
    ax2.grid(True)
    
    
    # Add text annotation at the year 2095 on the x-axis
    ax2.annotate(
        r'$C_y[8.5, mean]$', 
        xy=(2093, 0.20), 
        xytext=(2093, 0.25),  # Position of text slightly above and to the right
        ha='center'
    )
    fat_line_width = 0.25 # Thickness of the line
    fat_line_length = 0.4 # Length of the line
    x_position = 2093  # X-axis position
    y_position = 0.1  # Adjust to align with the x-axis
    
    # Add a central rectangle for the fat line
    central_rect = Rectangle(
        (x_position - fat_line_length / 2, y_position - fat_line_width / 2),  # Bottom-left corner
        fat_line_length, fat_line_width,  # Width and height
        linewidth=0, color="black", zorder=10
    )
    ax2.add_patch(central_rect)
    
    
    # Add text annotation at the year 2071 on the x-axis
    ax2.annotate(
        r'$C_y[8.5, high]$', 
        xy=(2070, 0.20), 
        xytext=(2070, 0.25),  # Position the text slightly above and to the right
        ha='center', color="black"
    )
    
    fat_line_width = 0.25 # Thickness of the line
    fat_line_length = 0.4 # Length of the line
    x_position = 2070  # X-axis position
    y_position = 0.1  # Adjust to align with the x-axis
    
    # Add a central rectangle for the fat line
    central_rect = Rectangle(
        (x_position - fat_line_length / 2, y_position - fat_line_width / 2),  # Bottom-left corner
        fat_line_length, fat_line_width,  # Width and height
        linewidth=0, color="black", zorder=10
    )
    ax2.add_patch(central_rect)
    
    
    ###############    Highlight Critical_year outcome I ########
    year_2095 = 2093
    y_95 = rcp_data.loc[rcp_data['year'] == year_2095, 'mean_85'].values[0]
    
    # Add a vertical line with arrows at both ends
    arrow = FancyArrowPatch(
        (year_2095, 0.3), (year_2095, y_95),
        mutation_scale=10, color='black', linestyle='-',
        arrowstyle='-', linewidth=0.6
    )
    ax2.add_patch(arrow)
    
    marker_properties = dict(
        marker='o', color='white',
        s=90,  edgecolor='black', linewidth=1.5
    )
    ax2.scatter(year_2095, y_95, **marker_properties, zorder=2)
    ###############    Highlight Critical_year outcome II ########
    year_2071 = 2071-1
    y_71 = rcp_data.loc[rcp_data['year'] == year_2071, 'max_85'].values[0]
    
    
    # Add a vertical line with arrows at both ends
    arrow = FancyArrowPatch(
        (year_2071, 0.3), (year_2071, y_71),
        mutation_scale=10, color='black', linestyle='-',
        arrowstyle='-', linewidth=0.6
    )
    ax2.add_patch(arrow)
    
    marker_properties = dict(
        marker='o', color='gainsboro',
        s=90,  edgecolor='black', linewidth=1.5
    )
    ax2.scatter(year_2071, y_71, **marker_properties, zorder=2)
    
    ax2.annotate(
        r'b)', 
        xy=(2047, 0.3), 
        xytext=(2047, 0.2),  # Position the text slightly above and to the right
        ha='center',fontsize=22
    )
    ax2.grid(axis='x', visible=False)
    ###########################################################
    #######        Third Plotting Window       ###############
    # Plot elevation above sea level versus year
    #ax3.set_title('2100')
    stats = df.agg(['min', 'max']).T
    
    
    x_labels = stats.index
    x_positions = range(len(x_labels))
    colors = ['#DDA63A', '#79BCFF', '#8C6518', '#FF0000']
    cols = ['#79BCFF', '#79BCFF', '#FF0000', '#FF0000']
    
    # Plot rectangles
    for i, label in enumerate(x_labels):
        min_val = stats.loc[label, 'min']
        max_val = stats.loc[label, 'max']
        mean_val = df.loc[1, label]  # Use the value in the second row as the mean value
        height = max_val - min_val
        
        
        ax3.add_patch(plt.Rectangle((i - 0.25, min_val), 0.6, height, facecolor=colors[i], alpha=0.3))
        
        # Add line for the second row's value
        ax3.plot([i - 0.25, i + 0.25], [mean_val, mean_val], color=cols[i], linewidth=2, linestyle ='--')
    
    
    # Set x-axis
    ax3.set_xticks(x_positions)
    ax3.set_xticklabels([])
    ax3.text(0.2, -0.05, 'RCP 2.6', ha='center', transform=ax3.transAxes)
    ax3.text(0.8, -0.05, 'RCP 8.5', ha='center', transform=ax3.transAxes)
    
    ax3.set_ylabel('[meter]')
    
    ax3.annotate(
        r'c)', 
        xy=(0.2, 0.3), 
        xytext=(0.2, 0.2),  # Position the text slightly above and to the right
        ha='center',fontsize=22
    )
    
    
    # Set y-axis limits of ax3 to be the same as ax2
    ax3.set_ylim(ax2.get_ylim())
    ax3.grid(False)
    
    # Set the context to increase overall font size
    sns.set_context("talk", font_scale=0.7)
    
    # Adjust layout to prevent overlapping
    plt.tight_layout()
    
    plt.show()



.. image:: figure_3_top_python_nb_files%5Cfigure_3_top_python_nb_12_0.png


