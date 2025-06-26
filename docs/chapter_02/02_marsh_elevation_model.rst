Model Relation R
=================================================
The core of this data-driven modeling approach is the representation of marsh accretion dynamics through a parametrisized equation linking main system components. Uncertainty in natural components and the effects of selected policies are represented through the sets the parameter values are sampled from.

.. math::

	\begin{equation}\label{eqn:timestepping}
		\frac{dE}{dt} = \sum_{s \in \text{S}} \sum_{T \in TC_{s}} \frac{((H_T + slr_t) - E_{t-1}) \cdot  C_{s,t} \cdot f_{d_s}}{\rho} - \frac{slr}{dt} - \frac{s_{sub}}{dt} 
	\end{equation}

The module ``data_loader.py`` manages loading the tidal and sea level time series for different RCP's and focus areas.

.. code-block:: python

    class DataLoader:
    """
    DataLoader class to load tidal and sea level rise data for different climate scenarios and sites.

    Parameters:
    -----------
    rcp : str
        Representative Concentration Pathway identifier, 'rcp26', 'rcp45', 'rcp85'.
    site : str
        Site identifier, 'S15', 'S33'.

    Attributes:
    -----------
    tides_per_year : pandas.DataFrame
        Tidal projection data merged with SLR data for the specified RCP scenario and site.
    """
    def __init__(self, rcp, site):
        import os
        import pandas as pd

        # Locate repo root (1 level up)
        module_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.abspath(os.path.join(module_dir, '..'))

        # Build paths to input files
        tides_path = os.path.join(repo_root, 'model_input_X_L', 'tidal_projections', f'tides_{rcp}_{site}.tsv')
        slr_path = os.path.join(repo_root, 'model_input_X_L', 'regional_slr_single_rcp', f'slr{rcp[3:]}.csv')

        # Load the files
        #tides_df = pd.read_csv(tides_path, sep='\t')
        #slr_df = pd.read_csv(slr_path)

        self.tides_per_year = pd.read_csv(tides_path, sep='\t')
        self.data = pd.read_csv(slr_path)       



The Marsh Accretion Model
^^^^^^^^^^^^^^^^^^^^^
Here we provide the core functions for simulating vertical marsh elevation change. ``marsh_elevation_rate`` is a straightforward computational implementation
of the equation above for computing yearly elevation change. As plant characteristics like height and canopy structure vary with their growth phase, we apply seasonal 
weights to the sediment trapping efficiency ``fd``. The following cases are implemented in our calculations.

.. math ::

	f_{d_s} = f_d \cdot \begin{cases} 
	0.5 & \text{if } s \text{ is spring}, \\
	1   & \text{if } s \text{ is summer}, \\
	0.6 & \text{if } s \text{ is autumn}, \\
	0.2 & \text{otherwise.}
	\end{cases}
	


Since we are using time-series inputs (sea level rise and tidal data), it's important that changes 
are correctly assigned to the corresponding year. We use the first year’s data, here 2041, to compute the elevation change over that year, anchoring the model to the pre-2041 
state as the baseline. This setup ensures that forward projections are properly aligned in time. ``calculate_initial_dz_dt`` performs the computation for the first year of the modeling period.

.. code-block:: python

	def marsh_elevation_rate(z_init, h_HW, n_events, c_flood, fd, rho_deposit, s_subsidence, slr, **kwargs):
		"""
		Calculates the rate of change of marsh elevation with seasonal parameters.
		"""
		seasonal_deposit = fd * sum(n_events[i] * c_flood * (h_HW[i] + slr - z_init) if (h_HW[i] + slr - z_init) > 0 else 0 for i in range(len(n_events)))  
		dz_dt = (seasonal_deposit / rho_deposit) - (s_subsidence + slr) * 0.25  # Adjusted for season
		return dz_dt
 


.. code-block:: python

	def calculate_initial_dz_dt(initial_year_data, z_init, c_flood, fd, rho_deposit, s_subsidence, **kwargs):
		"""
		Calculates the initial rate of change of marsh elevation for the first year.
		"""
		h_HW = initial_year_data['high_water_height'].tolist()
		n_events = initial_year_data['num_tides'].tolist()
		slr = initial_year_data['slr'].unique()[0]
	   
		initial_dz_dt = marsh_elevation_rate(z_init, h_HW, n_events, c_flood, fd, rho_deposit, s_subsidence, slr) - 0.75 * (s_subsidence + slr)
		return initial_dz_dt

Finally, the function ``marsh_elevation_model`` runs the full simulation over the whole modeling period. It simulates yearly marsh elevation change by aggregating seasonal sedimentation 
dynamics and adjusting for subsidenceand for sea level rise in constraining growth on the presence of a water column above ground: 

.. math ::

	\frac{dE}{dt}  = - \frac{slr}{dt} - \frac{s_{sub}}{dt} \quad  \text{for } (H_T + \text{slr}_t) - E_{t-1} < 0
	
implements the nourishment policy conditioned on the amount and frequency of nourishment, 

.. math::

	C_{s,t} =
	\begin{cases}
	C_s + C_{s,\mathcal{N}} & \text{if } t \text{ is a nourishment year,} \\
	C_s & \text{otherwise.}
	\end{cases}
	

while considering the decreasing effect of nourishment concentration in autumn and winter by

.. math ::

	C_{s,\mathcal{N}} = C_{\mathcal{N}}\cdot \begin{cases} 
	0.6 & \text{if } s \text{ is autumn}, \\
	0.0   & \text{if } s \text{ is winter}, \\
	1 & \text{otherwise.}
	\end{cases}
	


.. code-block:: python

	def marsh_elevation_model(z_init, c_flood, c_flood_nourishment, fd, rho_deposit, s_subsidence, nourishment_frequency,
								tides_per_year,  **kwargs):    
		
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
