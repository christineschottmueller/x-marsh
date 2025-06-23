Running the workbench
=================================================

Semantics: A scenario is a single point in the uncertainty space. A policy is a single point in the decision space. An experiment is the combination of one scenario and one policy.

Our experiment setup includes 10 parameters in total. Of these, 7 define uncertainties related to environmental conditions and system characteristics, such as climate scenario, site location, sea-level rise pathway, initial elevation, subsidence rate, sediment properties, and background sediment concentration.

The remaining 3 parameters are decision levers, representing policy choices. These include the frequency of sediment nourishment, the concentration of sediment added during nourishment, and the efficiency of sediment trapping.

Both the uncertainty and decision spaces are defined here using the ``CategoricalParameter``, in essence discrete rather than continuous ranges. 
This choice offers several advantages:

- **Scenario-based structure**: Many uncertainties—such as climate scenario, site location, or sea-level rise trajectory—are inherently discrete and defined by externally developed scenarios. Modeling them categorically maintains their integrity.

- **Realistic representation of decisions**: Decision levers like nourishment frequency or sediment concentration are typically selected from a limited set of practical options. Representing them as categorical values reflects how such choices are actually made.

- **Nonlinear system behavior**: The system may exhibit threshold effects or nonlinear responses to changes. Categorical parameters help capture these shifts without implying smooth transitions where none exist.

- **Simplicity in interpretation**: Results are easier to analyze and communicate when inputs represent meaningful, discrete conditions, rather than abstract numerical ranges.

- **Efficient experimental design**: Categorical inputs enable a straightforward full factorial design across scenarios and policies, avoiding unnecessary complexity while ensuring coverage of all relevant combinations.

