import os

import mysql.connector
from dotenv import load_dotenv

from logger_config import logger


load_dotenv()


def get_mysql_connection():

    try:

        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            database=os.getenv("MYSQL_DATABASE"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD")
        )

        logger.info("MySQL connection successful")

        return connection

    except mysql.connector.Error as error:

        logger.error(f"MySQL connection failed: {error}")

        raise