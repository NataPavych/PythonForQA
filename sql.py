import sqlite3



# response = requests.get('https://api.exchangeratesapi.io/latest')
# response.status_code
# response.raise_for_status()
# exchangerate = response.json()
# print(exchangerate)
# print(exchangerate(keys))
# if exchangerate.key == 'rates':
#     current_rate = {exchangerate.value}




with sqlite3.connect('forex.sqlite3') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rates')
    column_names = [element[0] for element in cursor.description]
    for row in cursor.fetchall():
        print(row)
        print(dict(zip(column_names, row)))
    print(column_names)

