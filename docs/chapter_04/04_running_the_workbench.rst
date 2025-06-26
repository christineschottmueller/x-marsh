Running the workbench
=================================================
We are now ready to connect the **x_marsh_function** to the EMA Workbench and generate instances of uncertain yet plausible future salt marsh states. Each uncertain function parameter defines a dimension within uncertainty space, while each policy lever defines a corresponding dimension in decision space. The dimensionality of these spaces is determined by the number of uncertain parameters and policy levers specified within the function. An **experiment** is defined as a tuple consisting of one realization from uncertainty space and one from decision space—that is, a specific combination of uncertain factors (X) and policy interventions (L). Each experiment thus represents a single, internally consistent future state of the world. Along each dimension, parameters may take on user-defined values from either a continuous interval or a discrete set, constrained by e.g. physical feasibility or expert judgement. In this study, we use the ``CategoricalParameter`` class for the defintion of discrete sets, discrete representations of continuous parameters. 

 This choice has two main reasons:
- **Simplicity in interpretation**: Results are easier to analyze and communicate when inputs represent meaningful, discrete conditions, rather than abstract numerical ranges.

- **Efficient experimental design**: Categorical inputs enable a straightforward full factorial design across scenarios and policies, avoiding unnecessary complexity while ensuring coverage of all relevant combinations.

Our experiment setup includes 10 parameters in total. Of these, 7 define uncertainties related to environmental conditions and system characteristics outside of the control of decision makers. The remaining 3 parameters are decision levers, representing policy choices. 




.. code:: ipython3
    from ema_workbench import (Model, CategoricalParameter, ScalarOutcome)
    
Import wrapper function from x_marsh.py

.. code:: ipython3

   from x_marsh import x_marsh_function

Instantiate a model object with the use of ``Model`` object. 

.. code:: ipython3
	
    model = Model('marshaccretion', function=x_marsh_function)
    model.uncertainties = uncertainties
    model.outcomes = outcomes

The uncertainties and outcomes are attributes of the ``Model`` object. Here the sets of their possible values are specified.

.. code:: ipython3

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
    
In the ``x_marsh_function`` we defined outcomes of interest for each function evaluation, each experiment. 

.. code:: ipython3

    outcomes = [
        ScalarOutcome('crit_year'),
        ScalarOutcome('growth_total'),
        ScalarOutcome('slope_norm_10'),
        ScalarOutcome('est_crit_year')
    ]



.. code:: ipython3

	from ema_workbench import perform_experiments, MultiprocessingEvaluator
	from ema_workbench.em_framework.samplers import FullFactorialSampler                               
	from ema_workbench import ema_logging, save_results, load_results   
     
Run the experiments using full factorial sampling design. Thereby ensure that all parameter combinations are represented in the output.

.. code:: ipython3

    with MultiprocessingEvaluator(model, n_processes=-1) as evaluator:
        experiments, outcomes = perform_experiments(model,  scenarios=7776*6, uncertainty_sampling=FullFactorialSampler())
    
Store the results in the folder ``model_output_M`` in your ``marsh_tutorial/`` folder.

.. code:: ipython3

    results=experiments,outcomes
    save_results(results, 'model_output_M\model_output_raw.tar.gz')
	
