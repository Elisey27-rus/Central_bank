import pandas as pd
import sqlite3

exel_file_name = "../test_data.xlsx"
sheet_name = "pt_data"
data = pd.read_excel(exel_file_name, sheet_name=sheet_name)

conn = sqlite3.connect("db.sqlite3")
data.to_sql('banks_info', conn, if_exists='replace')
print('#' * 100)
with sqlite3.connect("db.sqlite3") as connect:
    cursor = connect.cursor()
    sql = """
    SELECT *
    FROM banks_info b1
    WHERE b1.lic_code = 'PT_DP'
    AND NOT EXISTS (
        SELECT 1
        FROM banks_info b2
        WHERE b1.inn = b2.inn
        AND b2.lic_code = 'KGR_BANK'
)

    """
    cursor.execute(sql)
    result = cursor.fetchall()
    print("Банки у которых есть у которого есть депозитарная лицензия (PT_DP), но нет банковской лицензии (KGR_BANK): \n")
    for x in result:
        print(f"Инн:{x[1]}, Имя банка: {x[2]}")

print('#' * 100)
with sqlite3.connect("db.sqlite3") as connect:
    cursor = connect.cursor()
    sql = """
        SELECT *
        FROM banks_info b1
        WHERE b1.lic_code = 'PT_DP'
        AND EXISTS (
            SELECT 1
            FROM banks_info b2
            WHERE b1.inn = b2.inn
            AND b2.lic_code = 'KGR_BANK'
    )

    """
    cursor.execute(sql)
    result = cursor.fetchall()
    print("Банки у которых есть у которого есть депозитарная лицензия (PT_DP) и банковской лицензии (KGR_BANK): \n")
    for x in result:
        print(f"Инн:{x[1]}, Имя банка: {x[2]}")
print('#' * 100)


