import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

def read_risk_register_lite(register_dir: str = r'C:\Users\g.varvounis\Documents\RiskQuantification\runner\inputs',
                            file_name: str = r'risk register lite.xlsx', sheet: str = 'RR Lite'):
    """Reads & Imports Risk Register Lite for risks' quantification."""
    path = os.path.join(register_dir, file_name)

    df_register = pd.read_excel(path, sheet_name=sheet)

    return df_register

if __name__ == "__main__":

    print("Under Construction...")

    df_temp_1 = read_risk_register_lite()

    print(df_temp_1.info())
    print(df_temp_1.head(2))
    print(df_temp_1.shape)

