import os
import pika
import json
import mysql.connector as MC
from pymysql import MySQLError

# MySQL connection configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Saboua@2002',
    'database': 'BO2_database'
}

# Establish MySQL connection

try :

    ho_db_connection = MC.connect(**mysql_config)
    cursor = ho_db_connection.cursor()
    req= 'SELECT * FROM product_sales'
    cursor.execute(req)
    listproducts=cursor.fetchall()
    for l in listproducts :
        print('produit {}'.format(l[1]))

except MC.Error as err :
    print(err) 


# Establish connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue for this branch office
channel.queue_declare(queue='ho_queue')

script_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(script_dir, 'product_sales_changes.sql')

with open(file_path, 'r') as file:
    # Read the contents of the file
    script_content = file.read()

# Now, the variable script_content contains the contents of the script.sql file
print(script_content)

channel.basic_publish(exchange='', routing_key='ho_queue', body=script_content)

print("Sent SQL script to Head Office")

connection.close()




