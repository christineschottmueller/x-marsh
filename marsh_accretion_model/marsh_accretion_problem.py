"""
Evaluates marsh elevation trajectories under selected sea level rise scenarios and sediment dynamics.

Calculates critical marsh failure timing and growth trends using tidal and nourishment inputs.
Returns key outcomes for scenario analysis and decision support.
"""

from marsh_model import marsh_elevation_model  # core model functions
from data_loader import DataLoader

def marsh_accretion_problem(
    slr_select, z_init, c_flood, fd, rho_deposit, s_subsidence,
    nourishment_frequency, c_flood_nourishment, loader, **kwargs
):
    """
    Main function that computes marsh elevation changes and returns critical outcomes.
    """
    tides_per_year = loader.tides_per_year.copy()
    data = loader.data
    year_data = tides_per_year['year'].unique()
    tides_per_year['slr'] = 0.0  # Initialize 'slr' column with zeros

    # Select SLR scenario
    slr_options = {
        1: {'delta_slr': 'delta_min_slr', 'slr': 'min_slr'},
        2: {'delta_slr': 'delta_mean_slr', 'slr': 'mean_slr'},
        3: {'delta_slr': 'delta_max_slr', 'slr': 'max_slr'}
    }
    delta_col, slr_col = slr_options[slr_select].values()
    slr_data = data[['year', delta_col, slr_col]].rename(columns={delta_col: 'slr', slr_col: 'msl'})

    # Populate SLR values into seasonal dataset
    tides_per_year = tides_per_year.merge(slr_data[['year', 'slr']], on='year', how='left')

    # Run accretion model
    acc = marsh_elevation_model(
        z_init, c_flood, c_flood_nourishment, fd, rho_deposit,
        s_subsidence, nourishment_frequency, loader
    )
    acc_df = pd.DataFrame({'year': acc[1], 'elevation': acc[0], 'dz_dt': acc[2]})
    acc_df = acc_df.merge(slr_data, on='year').rename(columns={'slr': 'dslr_dt'})

    # Normalized elevation difference
    acc_df['norm_diff'] = (
        (acc_df['elevation'] - acc_df['msl']) /
        (acc_df['elevation'].iloc[0] - acc_df['msl'].iloc[0])
    )

    # Total growth over time
    growth_total = acc_df['dz_dt'].sum()

    # Check for critical year (elevation below mean sea level)
    crit_df = acc_df[acc_df['elevation'] <= acc_df['msl']]
    not_crit_df = acc_df[acc_df['elevation'] > acc_df['msl']]

    if not crit_df.empty:
        # Critical year reached
        crit_year = crit_df['year'].iloc[0]
        slope_norm_10 = None
        offset = 20

        while offset > 0:
            if len(not_crit_df) >= offset + 10:
                segment = not_crit_df.iloc[-offset:-offset + 10]
                slope_norm_10 = lineregress(segment['year'], segment['norm_diff'])
                break
            offset -= 1

        if slope_norm_10 is None:
            slope_norm_10 = np.finfo(float).eps
            est_time = crit_year - acc_df['year'].iloc[0]
        else:
            # Estimate time until critical state (fallback if early critical year)
            idx = not_crit_df.index[-offset + 9]
            est_time = abs(not_crit_df.loc[idx, 'norm_diff'] / slope_norm_10)

        est_crit_year = crit_year

    else:
        # No critical year reached during simulation
        crit_year = acc_df['year'].max() + 1
        tail = not_crit_df.tail(10)
        slope_norm_10 = lineregress(tail['year'], tail['norm_diff'])

        if slope_norm_10 >= 0:
            est_time = 70  # Marsh is gaining elevation
            est_crit_year = crit_year + est_time
        else:
            est_time = abs(tail['norm_diff'].iloc[-1] / slope_norm_10)
            est_crit_year = crit_year + est_time

    return crit_year, growth_total, slope_norm_10, est_time, est_crit_year




def x_marsh(rcp, site, slr_select, z_init, c_flood, fd, rho_deposit, s_subsidence, nourishment_frequency, c_flood_nourishment):

    # Load data for the given RCP and site
    loader = DataLoader(rcp=rcp, site=site)

    # Run the core marsh accretion problem with loaded data
    crit_year, growth_total, slope_norm_10, est_time, est_crit_year = marsh_accretion_problem(
        slr_select=slr_select,
        z_init=z_init,
        c_flood=c_flood,
        fd=fd,
        rho_deposit=rho_deposit,
        s_subsidence=s_subsidence,
        nourishment_frequency=nourishment_frequency,
        c_flood_nourishment=c_flood_nourishment,
        loader=loader
    )

    return {
        'crit_year': crit_year,
        'growth_total': growth_total,
        'slope_norm_10': slope_norm_10,
        'est_time': est_time,
        'est_crit_year': est_crit_year
    }

