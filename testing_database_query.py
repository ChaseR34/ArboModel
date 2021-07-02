# import django
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArboModelData.settings')
#
# django.setup()
#
# from Databases.Clients.models import Client
#
# query = Client.objects.first()

import psycopg2
import json

from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from django.core.serializers.json import DjangoJSONEncoder

db_name = "authentication_db"
db_user = "dis"
db_password = "M0nk3y!"
db_host = "192.168.0.9"
db_port = 5432

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_read_query(connection, query):
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")

connection = create_connection(db_name, db_user, db_password, db_host, db_port)

query = 'select * from "Clients_client";'

output = execute_read_query(connection, query)

# print(output)
x = json.dumps(output,
             cls=DjangoJSONEncoder
            )
print(x[1])
