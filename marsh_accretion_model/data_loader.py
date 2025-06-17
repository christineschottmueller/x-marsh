import os
import pandas as pd

class DataLoader:
    """
    DataLoader class to load tidal and sea level rise data for different climate scenarios and sites.

    Parameters:
    -----------
    rcp : str
        Representative Concentration Pathway identifier, 'rcp26', 'rcp45', 'rcp85'.
    site : str
        Site identifier, 'S33', 'S35'.

    Attributes:
    -----------
    tides_per_year : pandas.DataFrame
        Tidal projection data for the specified RCP scenario and site.
    data : pandas.DataFrame
        Regional sea level rise projections for the specified RCP scenario.

    """
    def __init__(self, rcp='rcp26', site='S33'):
        # Locate repo root (1 level up)
        module_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.abspath(os.path.join(module_dir, '..'))

        # Build paths to input files
        tides_path = os.path.join(repo_root, 'model_input_X_L', 'tidal_projections', f'tides_{rcp}_{site}.tsv')
        slr_path = os.path.join(repo_root, 'model_input_X_L', 'regional_slr_single_rcp', f'slr{rcp[3:]}.csv')

        # Load the files
        self.tides_per_year = pd.read_csv(tides_path, sep='\t')
        self.data = pd.read_csv(slr_path)