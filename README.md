# Описание заданий

## Задание 1: SQL-запросы

### Обзор
Работа с данными профессиональных участников рынка из таблицы `pt_data`. Данные включают ИНН, название организации, код и название лицензии.

### Требования
- **Таблица данных:** `pt_data`
- **Источник данных:** `test_data.xlsx`, лист `pt_data`
- **Поля:**
  - `inn` - ИНН
  - `name` - Название организации
  - `lic_code` - Код лицензии
  - `lic_name` - Название лицензии

### Задачи

Некредитной организацией - депозитарием (НФО) называется проф. участник рынка, у которого есть депозитарная лицензия (PT_DP), но нет банковской лицензии (KGR_BANK).
Кредитной организацией - депозитарием (КО) называется проф. участник рынка, у которого есть депозитарная лицензия (PT_DP), а также есть банковская лицензия (KGR_BANK)

Нужно написать два SQL-скрипта (стандарт SQL-92).
Первый скрипт выбирает все некредитные финансовые организации - депозитарии (НФО), нужно выводить поля "inn" и "name".
Второй скрипт выбирает все кредитные финансовые организации - депозитарии (КО), нужно выводить поля "inn" и "name".



## Задание 2: Анализ данных с Python

### Обзор
Обработка и анализ данных о ценных бумагах из депозитарного отчета, хранящегося в файле `test_data.xlsx` на листе `depo_data`.

### Требования
- **Таблица данных:** `depo_data`
- **Источник данных:** `test_data.xlsx`, лист `depo_data`
- **Поля:**
  - `isin` - Код ценной бумаги
  - `issuer_name_country` - Название эмитента и код страны
  - `quantity` - Количество ценных бумаг на отчетную дату
  - `report_date` - Отчетная дата

### Задачи
Разработка Python скрипта для выполнения следующих действий:
1. Чтение данных о ценных бумагах из файла `test_data.xlsx`.
2. Создание таблицы, отражающей количество ценных бумаг на счету за каждый рабочий день в июле 2023 года.
3. Разделение поля `issuer_name_country` на два отдельных поля:
   - `issuer_name` - Название эмитента, выпустившего ценную бумагу.
   - `country` - Код страны эмитента.
4. Запись итоговой таблицы в новый файл `result.xlsx`.

### Пример Python скрипта
```python
# Примерный код Python скрипта для выполнения задачи


