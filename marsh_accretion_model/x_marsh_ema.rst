.. code:: ipython3

    import os

.. code:: ipython3

    from ema_workbench import (Model, CategoricalParameter, ScalarOutcome, MultiprocessingEvaluator)
    from ema_workbench import perform_experiments
    from ema_workbench.em_framework.samplers import FullFactorialSampler                               
    from ema_workbench import ema_logging, save_results, load_results


.. parsed-literal::

    C:\Users\cschott\AppData\Roaming\Python\Python311\site-packages\ema_workbench\em_framework\evaluators.py:58: UserWarning: ipyparallel not installed - IpyparalleEvaluator not available
      warnings.warn("ipyparallel not installed - IpyparalleEvaluator not available")
    

.. code:: ipython3

    # Import wrapper function from marsh_accretion_problem.py
    from marsh_accretion_problem import marsh_accretion_problem

.. code:: ipython3

    # Define your uncertainties, including RCP and site as categorical
    uncertainties = [
        CategoricalParameter('rcp', ['rcp26', 'rcp45', 'rcp85']),
        CategoricalParameter('site', ['S15', 'S33']),
        CategoricalParameter('slr_select', [1, 2, 3]),
        CategoricalParameter('z_init', [0.4, 0.7, 1.2, 1.7]),
        CategoricalParameter('s_subsidence', [0.0027, 0.005]),
        CategoricalParameter('rho_deposit', [400, 800, 1200]),
        CategoricalParameter('c_flood', [0.05, 0.1, 0.2]),
        CategoricalParameter('fd', [0.2, 0.4, 0.6, 0.8]),
        CategoricalParameter('nourishment_frequency', [1, 5, 10]),
        CategoricalParameter('c_flood_nourishment', [0, 0.3, 0.5]),
    ]
    
    # Define your outcomes
    outcomes = [
        ScalarOutcome('crit_year'),
        ScalarOutcome('growth_total'),
        ScalarOutcome('slope_norm_10'),
        ScalarOutcome('est_time'),
        ScalarOutcome('est_crit_year')
    ]
    
    # Create the model object with your wrapper as the function
    model = Model('marshaccretion', function=marsh_accretion_problem)
    model.uncertainties = uncertainties
    model.outcomes = outcomes
    
    # Run experiments with sampled scenarios
    with MultiprocessingEvaluator(model, n_processes=-1) as evaluator:
        experiments, outcomes = perform_experiments(model,  scenarios=4)#7776*6, uncertainty_sampling=FullFactorialSampler())
    
    # Print the results
    print(outcomes)


.. parsed-literal::

    100%|████████████████████████████████████████████| 4/4 [00:01<00:00,  2.33it/s]
    

.. parsed-literal::

    {'crit_year': array([2101, 2101, 2101, 2060]), 'growth_total': array([ 0.13330032,  1.43734875, -0.47811771, -0.63765167]), 'slope_norm_10': array([-4.24454111e-03, -1.49333000e-02, -6.72019657e-03,  2.22044605e-16]), 'est_time': array([218.66588549, 268.54171836,  65.3091869 ,  19.        ]), 'est_crit_year': array([2319.66588549, 2369.54171836, 2166.3091869 , 2060.        ])}
    

.. code:: ipython3

    results=experiments,outcomes
    save_results(results, '..\..\model_output_M\model_output_S33_raw/S33_rcp26_full_factorial.tar.gz')


