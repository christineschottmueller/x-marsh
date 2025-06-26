"""
Evaluates marsh elevation trajectories under selected sea level rise scenarios and sediment dynamics.

Calculates critical marsh failure timing and growth trends using tidal and nourishment inputs.
Returns key outcomes for scenario analysis and decision support.
"""

from marsh_accretion_model import marsh_elevation_model
from helper_function import lineregress  
from data_loader import DataLoader
import numpy as np
import pandas as pd

def x_marsh_function(slr_select, z_init, c_flood, fd, rho_deposit, s_subsidence, 
                              nourishment_frequency, c_flood_nourishment, rcp, site, loader=None, **kwargs):

    """
    Main function that computes marsh elevation changes and returns critical outcomes.
    """
    if loader is None:
        loader = DataLoader(rcp=rcp, site=site)
    tides_per_year = loader.tides_per_year
    data = loader.data
    year_data = tides_per_year['year'].unique()
    tides_per_year['slr'] = 0  # Initialize 'slr' column with zeros

    # Select SLR data based on slr_select
    slr_options = {
        1: {'delta_slr': 'delta_min_slr', 'slr': 'min_slr'},
        2: {'delta_slr': 'delta_mean_slr', 'slr': 'mean_slr'},
        3: {'delta_slr': 'delta_max_slr', 'slr': 'max_slr'}
    }
    delta_col, slr_col = slr_options[slr_select].values()
    slr_data = data[['year', delta_col, slr_col]].rename(columns={delta_col: 'slr', slr_col: 'msl'})

    # Populate tides_per_year with SLR values
    for year in year_data:
        year_tides = tides_per_year[tides_per_year['year'] == year]
        slr_value = slr_data.loc[slr_data['year'] == year, 'slr'].values[0]
        tides_per_year.loc[year_tides.index, 'slr'] = slr_value

    # Calculate marsh elevation change
    #acc = marsh_elevation_model_1(z_init, c_flood, c_flood_nourishment, fd, rho_deposit, s_subsidence, nourishment_frequency, rcp, site, loader=None)
    acc = marsh_elevation_model(z_init=z_init, c_flood=c_flood, c_flood_nourishment=c_flood_nourishment, fd=fd,
    rho_deposit=rho_deposit, s_subsidence=s_subsidence, nourishment_frequency=nourishment_frequency, tides_per_year=tides_per_year)
    acc_df = pd.DataFrame({'year': acc[1], 'elevation': acc[0], 'dz_dt': acc[2]}).sort_values('year')
    accretion_df = acc_df.merge(slr_data, on='year').rename(columns={'slr': 'dslr_dt'})

    # Calculate normalized values
    accretion_df['norm_diff'] = (accretion_df['elevation'] - accretion_df['msl']) / (accretion_df['elevation'][0] - accretion_df['msl'][0])
    
    # Calculate outcome 1
    growth_total = accretion_df['dz_dt'].sum()
    
    # Separate critical and non-critical data
    crit_df = accretion_df[accretion_df['elevation'] <= accretion_df['msl']]
    not_crit_df = accretion_df[accretion_df['elevation'] > accretion_df['msl']]

    
    if not crit_df.empty:
        # CRITICAL STATE REACHED
        crit_year = crit_df['year'].iloc[0]
        
        slope_norm_10 = None
        offset = 20
        
        while offset > 0:
            if len(not_crit_df) >= offset + 10:
                segment = not_crit_df.iloc[-offset:-offset + 10]
                slope_norm_10 = lineregress(segment['year'], segment['norm_diff'])
                break
            offset = -1

        if slope_norm_10 is None:
            slope_norm_10 = np.finfo(float).eps  
            est_time = crit_year - 2041  # fallback based on crit_year
        else:
            est_time = abs(not_crit_df['norm_diff'].iloc[-offset + 10]/ slope_norm_10)

        est_crit_year = crit_year

    else:
        # NO CRITICAL YEAR REACHED
        crit_year = 2101
        slope_norm_10 = lineregress(not_crit_df.tail(10)['year'], not_crit_df.tail(10)['norm_diff'])

        if slope_norm_10 >= 0:
            est_time = 70  # Guaranteed Class IV membership
            est_crit_year = crit_year + est_time
        else:
            est_time = abs(not_crit_df['norm_diff'].iloc[-1] / slope_norm_10)
            est_crit_year = crit_year + est_time
            
    return crit_year, growth_total, slope_norm_10, est_time, est_crit_year
