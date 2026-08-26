from mysql_connection import get_mysql_connection


connection = get_mysql_connection()


cursor = connection.cursor()

cursor.execute("SELECT DATABASE();")

result = cursor.fetchone()

print("Connected database:", result[0])


cursor.close()
connection.close()