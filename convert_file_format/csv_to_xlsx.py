import pandas as pd

def csv_to_xlsx(filename_csv: str = 'data_raw/voteswithReason_raw.csv', filename_xlsx: str = 'data_raw/voteswithReason_raw.xlsx'):
    df = pd.read_csv(filename_csv)
    df.to_excel(filename_xlsx, index=False)

if __name__ == '__main__':
    csv_to_xlsx()
