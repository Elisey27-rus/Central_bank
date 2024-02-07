import sqlite3

import pandas as pd

file_name = "../test_data.xlsx"
sheet_name = "depo_data"
data = pd.read_excel(file_name, sheet_name=sheet_name)

data[['issuer_name', 'country']] = data['issuer_name_country'].str.rsplit(';', expand=True)
data = data.drop('issuer_name_country', axis=1)

data['report_date'] = pd.to_datetime(data['report_date'])
filtered_data = data[(data['report_date'] >= "2023-07-01") & (data['report_date'] <= "2023-07-31")]
data = filtered_data


conn = sqlite3.connect("db.sqlite3")
data.to_sql('banks_info', conn, if_exists='replace')
with sqlite3.connect("db.sqlite3") as connect:
    cursor = connect.cursor()
    cursor.execute("DROP TABLE IF EXISTS info_by_day")
    sql = """
        CREATE TABLE IF NOT EXISTS info_by_day(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isin TEXT,
        issuer_name TEXT,
        country TEXT,
        quantity INTEGER,
        date TEXT)
    """
    cursor.execute(sql)




for _, row in data.iterrows():
    with (sqlite3.connect("db.sqlite3") as connect):
        cursor=connect.cursor()
        sql = """
            INSERT INTO info_by_day(isin, issuer_name, country, quantity, date)
            VALUES(?,?,?,?,?)
        """
        date_str = row['report_date'].strftime('%Y-%m-%d')
        params=(row['isin'], row['issuer_name'], row['country'], row['quantity'], date_str)
        cursor.execute(sql, params)
        connect.commit()

print("#"*100)

#
isin_names=set(data['isin'])
dates = [(f"2023-07-{x + 1}") for x in range(0, 31)]
updated_columns = []
for date in dates:
    parts = date.split('-')
    if len(parts[2]) == 1:
        parts[2] = '0' + parts[2]
    updated_date = "-".join(parts)
    updated_columns.append(updated_date)
dates = updated_columns

result=pd.DataFrame(0, columns=dates, index=list(isin_names))

for isin in isin_names:
    last_quantity = 0
    for date in dates:
        data_row = data[(data['isin'] == isin) & (data['report_date'].dt.strftime('%Y-%m-%d') == date)]
        if not data_row.empty:
            last_quantity += data_row['quantity'].sum()
        result.at[isin, date] = last_quantity

print(result)

file_name="result.xlsx"
result.to_excel(file_name, index=True)




