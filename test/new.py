import sqlite3

import pandas as pd

# открываем файл и создаем дату в виде пандас
file_name = "../test_data.xlsx"
sheet_name = "depo_data"
data = pd.read_excel(file_name, sheet_name=sheet_name)

# разделяем колонки и убираем основную
data[['issuer_name', 'country']] = data['issuer_name_country'].str.rsplit(';', expand=True)
data = data.drop('issuer_name_country', axis=1)

# фильтруем данные и убираем даты которые не подходят под июль
data['report_date'] = pd.to_datetime(data['report_date'])
filtered_data = data[(data['report_date'] >= "2023-07-01") & (data['report_date'] <= "2023-07-31")]
data = filtered_data

# создаем список из дат июля
isin_names = set(data['isin'])
dates = [(f"2023-07-{x + 1}") for x in range(0, 31)]
updated_columns = []
for date in dates:
    parts = date.split('-')
    if len(parts[2]) == 1:
        parts[2] = '0' + parts[2]
    updated_date = "-".join(parts)
    updated_columns.append(updated_date)
dates = updated_columns

# конечная функция которая суммирует или просто вставляет данные
result = pd.DataFrame(columns=dates, index=list(isin_names))
for isin in isin_names:
    last_quantity = 0
    for date in dates:
        data_row = data[(data['isin'] == isin) & (data['report_date'].dt.strftime('%Y-%m-%d') == date)]
        if not data_row.empty:
            last_quantity += data_row['quantity'].sum()
        result.at[isin, date] = last_quantity

print(result)

file_name = "result.xlsx"
result.to_excel(file_name, index=True)