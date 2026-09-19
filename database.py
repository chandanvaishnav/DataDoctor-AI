import sqlite3
import pandas as pd


DATABASE_NAME = "datadoctor.db"


def create_database(df, database_name=DATABASE_NAME):
    """
    Create/replace the SQLite database from the dataframe.
    """

    connection = sqlite3.connect(database_name)

    try:
        df.to_sql(
            "dataset",
            connection,
            if_exists="replace",
            index=False
        )
    finally:
        connection.close()

    return database_name


def run_query(query, database_name=DATABASE_NAME):
    """
    Execute a SELECT query and return a pandas DataFrame.
    """

    connection = sqlite3.connect(database_name)

    try:
        result = pd.read_sql_query(
            query,
            connection
        )
    finally:
        connection.close()

    return result


def get_columns(database_name=DATABASE_NAME):
    """
    Return column names from the dataset table.
    """

    connection = sqlite3.connect(database_name)

    try:
        cursor = connection.execute(
            "PRAGMA table_info(dataset)"
        )

        columns = [
            row[1]
            for row in cursor.fetchall()
        ]

    finally:
        connection.close()

    return columns