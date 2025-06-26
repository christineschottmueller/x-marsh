"""
marsh_accretion_model.py

Contains the core functions for simulating vertical marsh elevation change:

- marsh_elevation_rate: computes yearly elevation change based on sediment inputs.
- calculate_initial_dz_dt: estimates initial elevation change.
- marsh_elevation_model: runs the full simulation over time.

This file captures the physical processes of marsh accretion and is imported by 
higher-level scripts for scenario analysis. No file I/O or data loading is done here.
"""
import numpy as np
import pandas as pd

def marsh_elevation_rate(z_init, h_HW, n_events, c_flood, fd, rho_deposit, s_subsidence, slr, **kwargs):
    """
    Calculates the rate of change of marsh elevation with seasonal parameters.
    """
    seasonal_deposit = fd * sum(n_events[i] * c_flood * (h_HW[i] + slr - z_init) if (h_HW[i] + slr - z_init) > 0 else 0 for i in range(len(n_events)))  
    dz_dt = (seasonal_deposit / rho_deposit) - (s_subsidence + slr) * 0.25  # Adjusted for season
    return dz_dt

def calculate_initial_dz_dt(initial_year_data, z_init, c_flood, fd, rho_deposit, s_subsidence, **kwargs):
    """
    Calculates the initial rate of change of marsh elevation for the first year.
    """
    h_HW = initial_year_data['high_water_height'].tolist()
    n_events = initial_year_data['num_tides'].tolist()
    slr = initial_year_data['slr'].unique()[0]
   
    initial_dz_dt = marsh_elevation_rate(z_init, h_HW, n_events, c_flood, fd, rho_deposit, s_subsidence, slr) - 0.75 * (s_subsidence + slr)
    return initial_dz_dt

def marsh_elevation_model(z_init, c_flood, c_flood_nourishment, fd, rho_deposit, s_subsidence, nourishment_frequency,
                            tides_per_year,  **kwargs):    
    """
    Calculates yearly marsh elevation and rate of change of elevation.
    """
    years_list = tides_per_year['year'].unique()
    start_year = years_list[0]
    z_values, dz_dt_values = [], []

    # Calculate the nourishment years
    nourishment_years = set(range(start_year, start_year + len(years_list) * nourishment_frequency, nourishment_frequency))

    for year in years_list:
        year_data = tides_per_year[tides_per_year['year'] == year]
        
        # Divide year data by season
        data_spring = year_data[year_data['season'] == 'spring']
        data_summer = year_data[year_data['season'] == 'summer']
        data_autumn = year_data[year_data['season'] == 'autumn']
        data_winter = year_data[year_data['season'] == 'winter']
        
        # Extract high water heights and event counts per season
        h_HW_spring, n_events_spring = data_spring['high_water_height'].tolist(), data_spring['num_tides'].tolist()
        h_HW_summer, n_events_summer = data_summer['high_water_height'].tolist(), data_summer['num_tides'].tolist()
        h_HW_autumn, n_events_autumn = data_autumn['high_water_height'].tolist(), data_autumn['num_tides'].tolist()
        h_HW_winter, n_events_winter = data_winter['high_water_height'].tolist(), data_winter['num_tides'].tolist()

        if year == start_year:
            # Calculate initial rate of change for the first year
            initial_dz_dt = calculate_initial_dz_dt(year_data, z_init, c_flood, fd, rho_deposit, s_subsidence)
            z_init += initial_dz_dt
            z_values.append(z_init)
            dz_dt_values.append(initial_dz_dt)
        else:
            slr = year_data['slr'].unique()[0]
            # Apply nourishment concentration adjustments per season
            if year in nourishment_years:
                c_flood_spring = c_flood + c_flood_nourishment
                c_flood_summer = c_flood + c_flood_nourishment
                c_flood_autumn = (c_flood + c_flood_nourishment* 0.6) 
                c_flood_winter = c_flood
            else:
                c_flood_spring = c_flood
                c_flood_summer = c_flood
                c_flood_autumn = c_flood
                c_flood_winter = c_flood

            # Seasonal sedimentation fraction adjustments
            fd_spring, fd_summer, fd_autumn, fd_winter = fd * 0.6, fd, fd * 0.5, fd * 0.2

            # Calculate dz/dt for each season and aggregate
            dz_dt_spring = marsh_elevation_rate(z_init, h_HW_spring, n_events_spring, c_flood_spring, fd_spring, rho_deposit, s_subsidence, slr)
            dz_dt_summer = marsh_elevation_rate(z_init, h_HW_summer, n_events_summer, c_flood_summer, fd_summer, rho_deposit, s_subsidence, slr)
            dz_dt_autumn = marsh_elevation_rate(z_init, h_HW_autumn, n_events_autumn, c_flood_autumn, fd_autumn, rho_deposit, s_subsidence, slr) 
            dz_dt_winter = marsh_elevation_rate(z_init, h_HW_winter, n_events_winter, c_flood_winter, fd_winter, rho_deposit, s_subsidence, slr)

            # Aggregate seasonal dz/dt and update elevation
            dz_dt = dz_dt_spring + dz_dt_summer + dz_dt_autumn + dz_dt_winter
            z_init += dz_dt

            z_values.append(z_init)
            dz_dt_values.append(dz_dt)

    return z_values, years_list, dz_dt_values
