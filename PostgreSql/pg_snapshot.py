import copy
from typing import List

import psycopg2


def create_snapshot(connection_info, snapshot_name):
    pg_cursor = get_pg_cursor(connection_info)

    terminate_db_connection(pg_cursor, connection_info.dbname)

    create_db_from_template(pg_cursor, db_name=snapshot_name, template_name=connection_info.dbname)

    close_cursor_and_connection(pg_cursor)


def restore_snapshot(connection_info, snapshot_name):
    pg_cursor = get_pg_cursor(connection_info)

    terminate_db_connection(pg_cursor, connection_info.dbname)

    drop_db(pg_cursor, connection_info.dbname)
    create_db_from_template(pg_cursor, db_name=connection_info.dbname, template_name=snapshot_name)

    close_cursor_and_connection(pg_cursor)


def delete_snapshot(connection_info, snapshot_name):
    pg_cursor = get_pg_cursor(connection_info)
    drop_db(pg_cursor, snapshot_name)


def get_pg_cursor(connection_info):
    pg_connection_info = copy.deepcopy(connection_info)
    pg_connection_info.dbname = "postgres"

    pg_connection = psycopg2.connect(
        dbname=pg_connection_info.dbname,
        user=pg_connection_info.user,
        password=pg_connection_info.password,
        host=pg_connection_info.host,
        port=pg_connection_info.port,
    )

    pg_connection.autocommit = True
    pg_cursor = pg_connection.cursor()

    return pg_cursor


def terminate_db_connection(pg_cursor, dbname):
    pg_cursor.execute(
        f"SELECT pg_terminate_backend(pg_stat_activity.pid) "
        f"FROM pg_stat_activity "
        f"WHERE pg_stat_activity.datname = '{dbname}'"
    )


def create_db_from_template(pg_cursor, db_name, template_name):
    pg_cursor.execute(f"CREATE DATABASE {db_name} TEMPLATE {template_name}")


def close_cursor_and_connection(cursor):
    cursor.close()
    cursor.connection.close()


def drop_db(pg_cursor, db_name):
    pg_cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")


def list_databases(connection_info) -> List[str]:
    pg_cursor = get_pg_cursor(connection_info)
    pg_cursor.execute("SELECT datname FROM pg_database")
    databases = pg_cursor.fetchall()

    return databases
