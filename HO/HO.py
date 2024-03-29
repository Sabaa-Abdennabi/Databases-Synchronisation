import pika
import json
import mysql.connector as MC

# MySQL connection configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Saboua@2002',
    'database': 'HO_database'
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

def callback(ch, method, properties, body):
    # Received migration script from branch office
    # Received migration script from branch office
    script = body.decode('utf-8')  # Assuming the script is sent as a string
    print("Received script:", script)

    # Split the script into individual queries
    queries = script.split(';')
    queries = [query.strip() for query in queries if query.strip()]  # Remove empty queries

    # Execute the queries on HO database
    for query in queries:
        try:
            cursor.execute(query)
            ho_db_connection.commit()
            print("Query executed successfully:", query)
        except Exception as e:
            print("Error executing query:", query, "Error:", e)

        # Send acknowledgment to branch office
    channel.basic_ack(delivery_tag=method.delivery_tag)

# Consume messages from queue
channel.basic_consume(queue='ho_queue', on_message_callback=callback)

print('Waiting for data changes from Branch Office...')
channel.start_consuming()
