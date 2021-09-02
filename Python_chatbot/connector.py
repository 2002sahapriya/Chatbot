import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'root',
    'password': 'Samika2004!',
    'host': 'localhost',
    'raise_on_warnings': True
}
# database connection
chatbot_connection = ''
chatbot_cursor = ''

# name of the database to be used
DB_NAME = 'ilantus_chatbot'

TABLES = {}
# User information table
TABLES['user_information'] = (
    "CREATE TABLE `USER_INFORMATION` ("
    "   `user_id` int(11) NOT NULL UNIQUE AUTO_INCREMENT,"
    "   `user_first_name` VARCHAR(255) NOT NULL UNIQUE,"
    "   `user_last_name` VARCHAR(255) NOT NULL UNIQUE,"
    "   `user_email` VARCHAR(255) NOT NULL UNIQUE,"
    "   `user_job_title` VARCHAR(255) NOT NULL,"
    "   `user_phone_number` VARCHAR(15) NOT NULL,"
    "   `user_geo_location` VARCHAR(255) NOT NULL,"
    "   `user_ip_address` VARCHAR(15) NOT NULL,"
    "   `date`  DATE NOT NULL,"
    "   `start_time` DATETIME NOT NULL,"
    "   `end_time` DATETIME NOT NULL,"
    "   `active_inactive` ENUM('active', 'inactive') NOT NULL,"
    "   PRIMARY KEY (`user_id`)"
    ")  ENGINE=InnoDB"

)

# Sales Person Information Table
TABLES['sales_person_information'] = (
    "CREATE TABLE `SALES_PERSON_INFORMATION` ("
    "   `sales_person_id` int(11) NOT NULL UNIQUE AUTO_INCREMENT,"
    "   `sales_person_first_name` VARCHAR(255) NOT NULL,"
    "   `sales_persion_last_name` VARCHAR(255) NOT NULL,"
    "   `sales_person_geo_location` VARCHAR(300) NOT NULL,"
    "   `sales_person_email` VARCHAR(255) NOT NULL UNIQUE,"
    "   `sales_person_contact_number` VARCHAR(15) NOT NULL,"
    "   PRIMARY KEY(`sales_person_id`)"
    ") ENGINE=InnoDB"

)


# Appointment tables
TABLES['appointment'] = (
    "CREATE TABLE `APPOINTMENT` ("
    "   `appointment_id` int(11) NOT NULL,"
    "   `user_id` int(11) NOT NULL,"
    "   `sales_person_id` int(11) NOT NULL,"
    "   `scheduled_date` DATE NOT NULL,"
    "   `scheduled_time` DATETIME NOT NULL,"
    "   `duration` ENUM('5', '10', '15', '30', '45', '60', '60+') NOT NULL,"
    "   `invite_mode` ENUM('phone call', 'teams meeting', 'zoom meeting', 'webex meeting') NOT NULL,"
    "   PRIMARY KEY(`appointment_id`),"
    "   FOREIGN KEY(`user_id`) REFERENCES `USER_INFORMATION`(`user_id`),"
    "   FOREIGN KEY(`sales_person_id`) REFERENCES `SALES_PERSON_INFORMATION`(`sales_person_id`)"
    ") ENGINE=InnoDB"
)


# Conversations table
TABLES['conversations'] = (
    "CREATE TABLE `CONVERSATIONS` ("
    "   `user_id` int(11) UNIQUE NOT NULL,"
    "   `conversation` JSON NOT NULL,"
    "   `date` DATE NOT NULL,"
    "   `conversation_id` int(11) NOT NULL UNIQUE AUTO_INCREMENT,"
    "   PRIMARY KEY(`conversation_id`),"
    "   FOREIGN KEY(`user_id`) REFERENCES `USER_INFORMATION`(`user_id`)"
    ") ENGINE=InnoDB"
)

# for creating database if it does not exist


def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))

# for creating the tables by iterating over the items of the table dictionary


def create_tables(tables, cursor, connection):
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table {} already exists.".format(table_name))
            else:
                print(err.msg)
        else:
            print('OK.')

# for selecting the database to be used


def select_database(cursor, database_name, chat_connection, tables):
    try:
        cursor.execute("USE {}".format(database_name))
        # create tables
        create_tables(tables, cursor, chat_connection)
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(database_name))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(database_name))
            chat_connection.database = database_name
            # create tables
            create_tables(tables, cursor, chat_connection)
        else:
            print(err)
            exit(1)

# for establishing connection with mysql database


def establish_connection():
    try:
        chatbot_connection = mysql.connector.connect(**config)
        chatbot_cursor = chatbot_connection.cursor()
        print("Database connected successfully.")
        # for selecting database to be used and create tables
        select_database(chatbot_cursor, DB_NAME, chatbot_connection, TABLES)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password!")
        else:
            print(err)
    else:
        chatbot_connection.close()


# calling the function
establish_connection()
