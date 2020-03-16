import pymysql.cursors
import conf.settings as env
import traceback
_connection = None

def connect():
    connection = _connection or pymysql.connect(**env.mysql)
    return connection

def write_interfaces(interfaces):
    # Connect to the database
    connection = connect()
    safe_create_interface_table(connection)
    for interface in interfaces:
        write_interface(connection, interface)
    connection.close()

def write_interface(connection, interface):
    try:
        with connection.cursor() as cursor:
            # Create a new record
            keys = ', '.join(f"'{x}'" for x in interface.keys())
            values = ', '.join(f"'{x}'"  for x in interface.values())
            print(keys, values)
            sql = f"INSERT INTO " \
                  f"interface (ifid, name, in_octects) " \
                  f"VALUES ( {interface['ifid']}, '{interface['name']}', '{interface['in_octects']}' )"
            cursor.execute(sql)
        connection.commit()

        # with connection.cursor() as cursor:
        #     # Read a single record
        #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        #     cursor.execute(sql, ('webmaster@python.org',))
        #     result = cursor.fetchone()
        #     print(result)
    except Exception as e:
        traceback.print_exc()

def check_table_exist(connection, tablename):
    connection = connect()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT count(*) FROM information_schema.tables WHERE table_name = '{tablename}'"
            cursor.execute(sql)
            return True
    except Exception as e:
        traceback.print_exc()
        return False

def safe_create_table(connection, tablename, columns):
    is_table = check_table_exist(connection, tablename)
    if is_table:
        try:
            with connection.cursor() as cursor:
                # Create a new record
                columns = ', '.join([ f'{name} {type}' for name, type in columns.items()])
                sql = f"CREATE TABLE IF NOT EXISTS {tablename} ({columns})"
                # print(sql)
                cursor.execute(sql)
            connection.commit()
        except Exception as e:
            traceback.print_exc()


def safe_create_interface_table(connection):
    safe_create_table(
        connection,
        'interface',
        {
            'ifid': 'INT',
            'name': 'VARCHAR(256)',
            'in_octects': 'VARCHAR(256)'
        }
    )