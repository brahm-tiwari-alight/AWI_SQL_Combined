import pandas as pd
import os

# Specify the Excel file name
excel_file = 'AWS QuickSight SQL Query Repository.xlsx'

# Load the Excel file
xls = pd.ExcelFile(excel_file)

# Create a directory for the CSV files if it doesn't exist
if not os.path.exists('csv_files'):
    os.makedirs('csv_files')

# Iterate through each sheet and convert to CSV
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name)
    csv_file_path = os.path.join('csv_files', f'{sheet_name}.csv')
    df.to_csv(csv_file_path, index=False)
    print(f'Converted {sheet_name} to {csv_file_path}')