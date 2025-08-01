import os
from datetime import datetime

def create_output_dir(model_dir:str = r'C:\Users\g.varvounis\Documents\RiskQuantification\runner\outputs'):
    # Create a 'results' directory if it doesn't exist
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Create a new directory with a timestamped name inside the 'results' directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    new_directory = os.path.join(model_dir, timestamp)
    os.makedirs(new_directory)

    return new_directory

