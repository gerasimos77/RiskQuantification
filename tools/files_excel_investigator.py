import pandas as pd

def are_excel_files_identical(file1_path, file2_path):
    # Load both Excel files
    xls1 = pd.ExcelFile(file1_path, engine='openpyxl')
    xls2 = pd.ExcelFile(file2_path, engine='openpyxl')

    # Compare sheet names
    if xls1.sheet_names != xls2.sheet_names:
        return False

    # Compare each sheet's content
    for sheet in xls1.sheet_names:
        df1 = xls1.parse(sheet)
        df2 = xls2.parse(sheet)

        # Check if dataframes are equal
        if not df1.equals(df2):
            return False

    return True
