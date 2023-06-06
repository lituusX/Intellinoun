import pandas as pd

# This function converts a CSV file to an XLSX file.
# The `filename_csv` parameter is the path to the input CSV file.
# The `filename_xlsx` parameter is the path to the output XLSX file.
# To modify the paths, simply change the values of these parameters.
def csv_to_xlsx(filename_csv: str = '../data_raw/enriched/voteswithReason_Sentiment_raw.csv', filename_xlsx: str = '../data_raw/enriched/voteswithReason_Sentiment_raw.xlsx'):
    # Reads the CSV file from the specified path
    df = pd.read_csv(filename_csv)
    # Writes the DataFrame to an XLSX file at the specified path
    df.to_excel(filename_xlsx, index=False)

if __name__ == '__main__':
    # Calls the csv_to_xlsx function with default paths
    # To use different paths, call the function with the paths as arguments like so:
    # csv_to_xlsx('path/to/input.csv', 'path/to/output.xlsx')
    csv_to_xlsx()
    