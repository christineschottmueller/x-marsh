This README.txt file was generated on 2026-07-31 by Christine Schottmüller


GENERAL INFORMATION
1. Title of dataset: Exploratory Marsh Accretion Model Data
2. Creator information:
   Christine Schottmüller, Landscape Ecology and Environmental System Analysis, Institute of Geoecology, Technische Universität Braunschweig, Germany
   Email: [c.schottmueller@tu-braunschweig.de](mailto:c.schottmueller@tu-braunschweig.de)
3. Supporting data and code for submission:
   Schottmüller, C., & David, G. 'Growing Up With Sea Level Rise - Perspectives on Marsh Adaptation in the Wadden Sea', Technische Universität Braunschweig, submitted to AGU Earth's Future.
4. Funding sources:

   * BMBF (METAscales project, FKZ 03F0955-A)
   * DAM mission mareXtreme
   * DFG Junior Research Group (Future Urban Coastlines)

ABSTRACT
This dataset supports simulations of salt marsh resilience under sea level rise scenarios. We modeled 12,960 scenarios across two mainland marshes (S15, S33), exploring natural and managed adaptation strategies. 
Data includes model inputs, outputs, and figure reproduction material.

SHARING/ACCESS INFORMATION
1. License: Creative Commons Attribution 4.0 (CC-BY 4.0)

2. Data from other sources:

  * Tidal Elevation Data: Sourced from the Global Tide and Surge Model (GTSMv3.0), available through the Climate Data Store (CDS) using IPCC scenarios RCP4.5
    and RCP8.5 for the European coastline.
    Citation: Muis et al. (2020). A High-Resolution Global Dataset of Extreme Sea Levels, Tides, and Storm Surges, Including Future Projections
    Online Resource: https://cds.climate.copernicus.eu/datasets?q=water+level+projections&limit=30
  * Regional Sea Level Rise Data: Projections from the AR5 scenario, provided by the Integrated Climate Data Center (ICDC) at the University of Hamburg.
    Citation: Church et al. (2013). Sea level change
    Online Resource: https://www.cen.uni-hamburg.de/icdc/data/ocean/ar5-slr.html

METHODOLOGICAL INFORMATION
1. Data Generation:
   Exploratory modeling of marsh accretion dynamics under uncertain environmental conditions and policy interventions.
2. Data Processing:
   Input preparation and analysis in R, Python, and SQL.
   Model simulations and outputs aggregated for figure generation.
3. Instruments / Software:

   * R 4.4.2 with packages: tidyverse, openair, leaflet, openxlsx
   * JupyterLab (optional, for reproducing figures)

DATA & FILE OVERVIEW
1. File List:

  ```
📁 Exploratory_Marsh_Accretion_Model/
├── 📂 figures/
├── 📂 data/                       📄 (CSV files for Figures 3–6)
├── 📂 notebooks/                  📄 (Jupyter notebooks in Python and R)
├── 📂 literature/                 📄 (Citing literature for data sources)
├── 📂 model_code/
│   ├── 📂 S15_east_frisian/       📄 (Python modules + notebook for S15)
│   └── 📂 S33_weser_elbe/         📄 (Python modules + notebook for S33)
├── 📂 model_input_X_L/
│   ├── 📂 tidal_projections/
│   │   ├── 📄 tides_rcp26_S15.csv
│   │   ├── 📄 tides_rcp45_S15.csv
│   │   └── 📄 tides_rcp85_S33.csv
│   ├── 📂 regional_slr_ar5/
│   ├── 📂 categorical_inputs/
│   └── 📂 literature/
├── 📂 model_output_M/
│   ├── 📂 model_output_S15_raw/
│   ├── 📂 model_output_S33_raw/
│   ├── 📂 model_output_S15_clean/
│   ├── 📂 model_output_S33_clean/
│   └── 📄 clean_output_M_raw.ipynb
├── 📂 pioneer_zone_DAPP/
│   └── 📂 model_output_S15_raw/
└── 📄 readme.md
```



2. Relationships: Figures depend on processed outputs from model runs.
3. Filename Conventions: Self-descriptive, using scenario type and site ID.
4. Formats: .zip, .tsv, .csv, .Rmd, .ipynb, .md
5. Requirements: To run the modeling workflow and reproduce figures, the following software and packages are required:
    - Python (version = 3.8):			(Used for the marsh accretion model and exploratory modeling notebooks)
    - Jupyter Notebook or JupyterLab:	Required for running the notebooks provided in both Python and R.
    - EMA Workbench (ema_workbench):	Essential for exploratory modeling, scenario discovery, and adaptive policy evaluation
    - R and IRKernel:					Required to run the R-based notebooks included for figure reproduction.
    - Common Python and R packages Includes standard libraries for data handling, visualization(e.g., pandas, matplotlib, scikit-learn in Python; tidyverse, dplyr in R).


DATA-SPECIFIC INFORMATION
1. Variables:
   * Tidal projections: year, number of tides, high water height
   * Model outputs: elevation change, marsh zone shifts
2. Units: Elevations in meters relative to mean sea level.
3. Missing Data Codes: NA (Not Available)
4. Abbreviations:

   * SLR:  Sea Level Rise
   * RCP:  Representative Concentration Pathway
   * DAPP: Dynamic Policy Adaptation Pathway
   

NOTES
For inquiries, contact Christine SchottmÃ¼ller ([c.schottmueller@tu-braunschweig.de](mailto:c.schottmueller@tu-braunschweig.de)).


