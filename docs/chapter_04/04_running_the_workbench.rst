Running the workbench
=================================================
A scenario is a single point in the uncertainty space. A policy is a single point in the decision space. An experiment is the combination of one scenario and one policy.
Both the uncertainty and decision spaces are defined here using the ``CategoricalParameter``, in essence discrete rather than continuous ranges. 
This choice offers several advantages:

- **Simplicity in interpretation**: Results are easier to analyze and communicate when inputs represent meaningful, discrete conditions, rather than abstract numerical ranges.

- **Efficient experimental design**: Categorical inputs enable a straightforward full factorial design across scenarios and policies, avoiding unnecessary complexity while ensuring coverage of all relevant combinations.


- **Scenario-based structure**: Many uncertainties—such as climate scenario, site location, or sea-level rise trajectory—are inherently discrete and defined by externally developed scenarios. Modeling them categorically maintains their integrity.

- **Realistic representation of decisions**: Decision levers like nourishment frequency or sediment concentration are typically selected from a limited set of practical options. Representing them as categorical values reflects how such choices are actually made.

- **Nonlinear system behavior**: The system may exhibit threshold effects or nonlinear responses to changes. Categorical parameters help capture these shifts without implying smooth transitions where none exist.

Our experiment setup includes 10 parameters in total. Of these, 7 define uncertainties related to environmental conditions and system characteristics, such as climate scenario, site location, sea-level rise pathway, initial elevation, subsidence rate, sediment properties, and background sediment concentration. The remaining 3 parameters are decision levers, representing policy choices. These include the frequency of sediment nourishment, the concentration of sediment added during nourishment, and the efficiency of sediment trapping. 


.. code:: ipython3

    import os
    from ema_workbench import (Model, CategoricalParameter, ScalarOutcome)
    
Import wrapper function from marsh_accretion_problem.py

.. code:: ipython3

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
    
Define your outcomes

.. code:: ipython3
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

	from ema_workbench import perform_experiments, MultiprocessingEvaluator
	from ema_workbench.em_framework.samplers import FullFactorialSampler                               
	from ema_workbench import ema_logging, save_results, load_results   
     
Run experiments with sampled scenarios

.. code:: ipython3
    with MultiprocessingEvaluator(model, n_processes=-1) as evaluator:
        experiments, outcomes = perform_experiments(model,  scenarios=7776*6, uncertainty_sampling=FullFactorialSampler())
    
	
.. code:: ipython3