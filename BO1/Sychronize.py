import os
import pika
import json
import mysql.connector as MC
from pymysql import MySQLError



def export_product_sales_changes_to_script():
    # Connect to MySQL database
    mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Saboua@2002',
    'database': 'BO1_database'
    }
    connection = MC.connect(**mysql_config)



    # Create cursor
    cursor = connection.cursor()

    # Query to fetch data from product_sales_changes_log
    query = "SELECT query FROM product_sales_changes_log"

    try:
        # Execute query
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Initialize script content
        script_content = ""

        # Iterate over rows and append queries to script content
        for row in rows:
            script_content += row[0] + '\n'
        
        script_dir = os.path.dirname(os.path.abspath(__file__))

        file_path = os.path.join(script_dir, 'product_sales_changes.sql')

        # Write script content to file
        with open(file_path, 'w') as f:
            f.write(script_content)

        print("Captured changes exported to script: product_sales_changes.sql")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()


export_product_sales_changes_to_script()