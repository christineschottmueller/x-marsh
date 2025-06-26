Cleaning Raw Output Data for physical plausibility
======================================================

.. code:: ipython3

    from ema_workbench import ema_logging, save_results, load_results
    import pandas as pd
    import os


The use of a full factorial design for scenario generation, while
comprehensive, inevitably results in a subset of parameter combinations
that are implausible or infeasible under real-world conditions. To
maintain the analytical integrity and interpretability of the results,
these non-viable scenarios must be systematically identified and
excluded from the dataset.

I Exclusion of Cases with High Nourishment Frequency and Volume but Low Dry Bulk Density
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sand nourishments are known to elevate the concentration of suspended
mineral sediments in the water column, thereby promoting mineral
sediment deposition. In scenarios characterized by frequent nourishment
interventions and high volumes of sand input, it is implausible for the
resulting sediment deposits to exhibit low dry bulk density values
:math:`\rho=400`. Such combinations likely reflect unrealistic or
inconsistent model behavior. Therefore, cases exhibiting both high
nourishment frequency and quantity :math:`C_{\mathcal{N}}`, coupled with
low dry bulk density, are excluded from the analysis to ensure the
physical plausibility and integrity of the modeled outcomes.

The following combinations of parameters are excluded due to their
physical implausibility, as described above:

+-----------------------+------------------------+---------------------+
| N. concentration      | N. frequency           | Dry bulk density    |
+=======================+========================+=====================+
| 0.3                   | 1                      | 400                 |
+-----------------------+------------------------+---------------------+
| 0.5                   | 1                      | 400                 |
+-----------------------+------------------------+---------------------+
| 0.5                   | 5                      | 400                 |
+-----------------------+------------------------+---------------------+

II Exclusion of Cases with Implausible Sediment Deposition Fractions and Vegetation States
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The parameter :math:`f_d` represents the fraction of sediment retained
and reflects both vegetation-mediated trapping and management
interventions. On mudflats (:math:`E_0=0.4`), high values of
:math:`f_d \in (0.6, 0.8)` imply strong sediment trapping, which is
unrealistic for unvegetated or sparsely vegetated areas, and are
therefore excluded. In the pioneer zone (:math:`E_0=0.7`), extreme
values (:math:`f_d=0.2` and :math:`f_d=0.8`) are removed, as they do not
plausibly reflect vegetation structure under either conservation or
restoration conditions.

For the low marsh (:math:`E_0=1.2`) and high marsh (:math:`E_0=1.7`),
values of :math:`f_d=0.4`, :math:`f_d=0.4`, and :math:`f_d=0.8` are
retained, corresponding to management strategies such as no restoration,
conservation, and active restoration in the low marsh, and excessive
grazing, grazing, and no grazing in the high marsh. In both zones,
:math:`f_d=0.2` is excluded due to incompatibility with the expected
sediment trapping under vegetated conditions. These constraints help
ensure the physical plausibility of modeled scenarios across the
elevation gradient.

The following combinations of parameters are excluded due to their
physical implausibility, as described above: \| Elevation \| Depositing
fraction \| \|:—————————-:\|:—————————–:\| \| 0.4 \| 0.6, 0.8 \| \| 0.7
\| 0.2, 0.8 \| \| 1.2 \| 0.2 \| \| 1.7 \| 0.2 \|

III Exclusion of Cases with Nourishment Frequency but No Input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cases with a non-zero nourishment frequency but zero nourishment amount
(:math:`C_{\mathcal{N}} = 0`) are excluded, as they imply sediment input
events without actual material added—an implausible scenario.

The following combinations of parameters are excluded due to their
physical implausibility, as described above: \| N. concentration \| N.
frequency \| \|:—————————-:\|:—————————–:\| \| 0.0 \| 5 \| \| 0.0 \|10
\|

1. Define filter code
^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    def apply_filters(df):
        filter_I = [
            (0.3, 1, 400),
            (0.5, 1, 400),
            (0.5, 5, 400),
        ]
        mask_I = df[['c_flood_nourishment', 'nourishment_frequency', 'rho_deposit']].apply(tuple, axis=1).isin(filter_I)
        df_I = df[~mask_I]
    
        filter_II = [
            (0.4, 0.6),
            (0.4, 0.8),
            (0.7, 0.2),
            (0.7, 0.8),
            (1.2, 0.2),
            (1.7, 0.2),
        ]
        mask_II = df_I[['z_init', 'fd']].apply(tuple, axis=1).isin(filter_II)
        df_II = df_I[~mask_II]
    
        filter_III = [
            (0.0, 10),
            (0.0, 5),
        ]
        mask_III = df_II[['c_flood_nourishment', 'nourishment_frequency']].apply(tuple, axis=1).isin(filter_III)
        return df_II[~mask_III]

2. Load dataset
^^^^^^^^^^^^^^^

.. code:: ipython3

    # RCP 8.5 dataset
    #experiments, outcomes=load_results('model_output_M/model_output_raw.tar.gz')
    experiments, outcomes=load_results('model_output_raw.tar.gz')
    outcomes = pd.DataFrame(outcomes)
    out_raw=pd.concat([experiments, outcomes], axis = 1)

3. Apply filter and store filtered dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    # Apply filters and store results with names
    filtered_dataset = apply_filters(out_raw) 
    
    # Store in predefined output folder
    filtered_dataset.to_csv("model_output_clean.txt", sep='\t', index=False)

.. code:: ipython3

    filtered_dataset




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>c_flood</th>
          <th>c_flood_nourishment</th>
          <th>fd</th>
          <th>nourishment_frequency</th>
          <th>rcp</th>
          <th>rho_deposit</th>
          <th>s_subsidence</th>
          <th>site</th>
          <th>slr_select</th>
          <th>z_init</th>
          <th>scenario</th>
          <th>policy</th>
          <th>model</th>
          <th>crit_year</th>
          <th>growth_total</th>
          <th>slope_norm_10</th>
          <th>est_time</th>
          <th>est_crit_year</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>0.05</td>
          <td>0.0</td>
          <td>0.2</td>
          <td>1</td>
          <td>rcp26</td>
          <td>400</td>
          <td>0.0027</td>
          <td>S15</td>
          <td>1</td>
          <td>0.4</td>
          <td>4</td>
          <td>NaN</td>
          <td>marshaccretion</td>
          <td>2101</td>
          <td>0.171807</td>
          <td>-9.898503e-03</td>
          <td>98.660792</td>
          <td>2199.660792</td>
        </tr>
        <tr>
          <th>4</th>
          <td>0.05</td>
          <td>0.0</td>
          <td>0.2</td>
          <td>1</td>
          <td>rcp26</td>
          <td>400</td>
          <td>0.0027</td>
          <td>S15</td>
          <td>2</td>
          <td>0.4</td>
          <td>8</td>
          <td>NaN</td>
          <td>marshaccretion</td>
          <td>2101</td>
          <td>0.082943</td>
          <td>-1.916339e-02</td>
          <td>0.280064</td>
          <td>2101.280064</td>
        </tr>
        <tr>
          <th>8</th>
          <td>0.05</td>
          <td>0.0</td>
          <td>0.2</td>
          <td>1</td>
          <td>rcp26</td>
          <td>400</td>
          <td>0.0027</td>
          <td>S15</td>
          <td>3</td>
          <td>0.4</td>
          <td>12</td>
          <td>NaN</td>
          <td>marshaccretion</td>
          <td>2058</td>
          <td>-0.011490</td>
          <td>2.220446e-16</td>
          <td>17.000000</td>
          <td>2058.000000</td>
        </tr>
        <tr>
          <th>12</th>
          <td>0.05</td>
          <td>0.0</td>
          <td>0.2</td>
          <td>1</td>
          <td>rcp26</td>
          <td>400</td>
          <td>0.0027</td>
          <td>S33</td>
          <td>1</td>
          <td>0.4</td>
          <td>16</td>
          <td>NaN</td>
          <td>marshaccretion</td>
          <td>2101</td>
          <td>0.377851</td>
          <td>-1.682433e-03</td>
          <td>964.912963</td>
          <td>3065.912963</td>
        </tr>
        <tr>
          <th>16</th>
          <td>0.05</td>
          <td>0.0</td>
          <td>0.2</td>
          <td>1</td>
          <td>rcp26</td>
          <td>400</td>
          <td>0.0027</td>
          <td>S33</td>
          <td>2</td>
          <td>0.4</td>
          <td>20</td>
          <td>NaN</td>
          <td>marshaccretion</td>
          <td>2101</td>
          <td>0.289847</td>
          <td>-7.383435e-03</td>
          <td>127.420968</td>
          <td>2228.420968</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>46647</th>
          <td>0.20</td>
          <td>0.5</td>
          <td>0.8</td>
          <td>10</td>
          <td>rcp85</td>
          <td>1200</td>
          <td>0.0050</td>
          <td>S33</td>
          <td>1</td>
          <td>1.7</td>
          <td>46651</td>
          <td>NaN</td>
          <td>marshaccretion</td>
          <td>2101</td>
          <td>-0.048469</td>
          <td>-5.145372e-03</td>
          <td>143.501122</td>
          <td>2244.501122</td>
        </tr>
        <tr>
          <th>46650</th>
          <td>0.20</td>
          <td>0.5</td>
          <td>0.8</td>
          <td>10</td>
          <td>rcp85</td>
          <td>1200</td>
          <td>0.0050</td>
          <td>S33</td>
          <td>2</td>
          <td>1.2</td>
          <td>46654</td>
          <td>NaN</td>
          <td>marshaccretion</td>
          <td>2101</td>
          <td>0.350695</td>
          <td>-1.439202e-02</td>
          <td>50.063334</td>
          <td>2151.063334</td>
        </tr>
        <tr>
          <th>46651</th>
          <td>0.20</td>
          <td>0.5</td>
          <td>0.8</td>
          <td>10</td>
          <td>rcp85</td>
          <td>1200</td>
          <td>0.0050</td>
          <td>S33</td>
          <td>2</td>
          <td>1.7</td>
          <td>46655</td>
          <td>NaN</td>
          <td>marshaccretion</td>
          <td>2101</td>
          <td>-0.133335</td>
          <td>-1.061966e-02</td>
          <td>48.034785</td>
          <td>2149.034785</td>
        </tr>
        <tr>
          <th>46654</th>
          <td>0.20</td>
          <td>0.5</td>
          <td>0.8</td>
          <td>10</td>
          <td>rcp85</td>
          <td>1200</td>
          <td>0.0050</td>
          <td>S33</td>
          <td>3</td>
          <td>1.2</td>
          <td>46658</td>
          <td>NaN</td>
          <td>marshaccretion</td>
          <td>2101</td>
          <td>0.254902</td>
          <td>-2.604880e-02</td>
          <td>11.261905</td>
          <td>2112.261905</td>
        </tr>
        <tr>
          <th>46655</th>
          <td>0.20</td>
          <td>0.5</td>
          <td>0.8</td>
          <td>10</td>
          <td>rcp85</td>
          <td>1200</td>
          <td>0.0050</td>
          <td>S33</td>
          <td>3</td>
          <td>1.7</td>
          <td>46659</td>
          <td>NaN</td>
          <td>marshaccretion</td>
          <td>2101</td>
          <td>-0.231710</td>
          <td>-1.816963e-02</td>
          <td>11.397365</td>
          <td>2112.397365</td>
        </tr>
      </tbody>
    </table>
    <p>19440 rows × 18 columns</p>
    </div>


