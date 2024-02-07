import pandas as pd

# открываем файл Exel и переводим его в формат pandas
exel_file_name = "../test_data.xlsx"
sheet_name = "depo_data"
data = pd.read_excel(exel_file_name, sheet_name=sheet_name)

# делаем валидацию данных и сортируем данные только по июлю 2023 года
data['report_date'] = pd.to_datetime(data['report_date'])
min = pd.to_datetime("2023-07-01")
max = pd.to_datetime("2023-07-31")
new_data = data.loc[(data['report_date'] >= min) & (data['report_date'] <= max)]

# Делаем колонки из дат которые будут в таблицу от 1 до 31 июля в формате (2023-07-01)
columns = [(f"2023-07-{x + 1}") for x in range(0, 31)]
updated_columns = []
for date in columns:
    parts = date.split('-')
    if len(parts[2]) == 1:
        parts[2] = '0' + parts[2]
    updated_date = "-".join(parts)
    updated_columns.append(updated_date)
columns = updated_columns

# Делаем горизонталь по которой будут написаны коды ценной бумаги
rows = list(set([x for x in new_data["isin"]]))

# Создаем таблицу
table = pd.DataFrame(columns=columns, index=rows)


print(rows)
print(columns)
# Вставляем данные в таблицу, суммируя с предыдущими значениями
for isin in rows:
    last_quantity = 0
    for date in columns:
        # Инициализируем переменную для сбора данных
        quantity_sum = 0
        # Проходим по каждой строке в DataFrame
        for index, row in new_data.iterrows():
            # Проверяем, соответствует ли строка условиям
            if row['isin'] == isin and row['report_date'].strftime('%Y-%m-%d') == date:
                quantity_sum += row['quantity']
        # Если были найдены соответствующие строки, обновляем last_quantity
        if quantity_sum > 0:
            last_quantity += quantity_sum
        # Записываем итоговое значение в таблицу
        table.loc[isin, date] = last_quantity


# Добавляем код ценной бумаги
table.reset_index(inplace=True)
table.rename(columns={'index': 'ISIN'}, inplace=True)

print(new_data)
print(table)


# Разделяем столбец "issuer_name_country" на два столбца "issuer_name" и "country"
for isin in new_data['isin'].unique():
    issuer_name_country = new_data.loc[new_data['isin'] == isin, 'issuer_name_country'].iloc[0]
    issuer_name = issuer_name_country[:-4].strip()
    country = issuer_name_country[-2:].strip()
    table.loc[table['ISIN'] == isin, 'issuer_name'] = issuer_name
    table.loc[table['ISIN'] == isin, 'country'] = country

# Переупорядочиваем столбцы
new_columns_order = ['ISIN', 'issuer_name', 'country'] + columns
table = table[new_columns_order]

result_file_name = "result.xlsx"  # Имя файла для сохранения результатов
table.to_excel(result_file_name, index=False)
