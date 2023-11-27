import psycopg2
import datetime
from typing import List, Tuple


class WeatherDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="weather",
            user='postgres',
            password='3858nima',
            host='127.0.0.1',
            port='5432')
        # Creating a cursor object using the cursor() method
        self.cursor = self.conn.cursor()
        self.conn.autocommit = True

    def create_tables(self):
        create_table_query1 = """
            CREATE TABLE IF NOT EXISTS requests (
                requestid SERIAL PRIMARY KEY,
                city_name VARCHAR(100),
                datetime TIMESTAMP DEFAULT current_timestamp
            );
        """
        create_table_query2 = """
            CREATE TABLE IF NOT EXISTS response (
                responseid SERIAL PRIMARY KEY,
                requestid INT,
                temperature INT,
                city_name VARCHAR(100),
                FOREIGN KEY (requestid) REFERENCES requests (requestid)
            );
        """
        self.cursor.execute(create_table_query1)
        self.cursor.execute(create_table_query2)
        self.conn.commit()

    def save_request_data(self, city_name: str, request_time: str) -> None:

        try:
            insert_query = "INSERT INTO requests (datetime, city_name) VALUES (%s, %s);"
            self.cursor.execute(insert_query, (city_name, request_time))
            self.conn.commit()
            print("Request data saved successfully.")
        except Exception as e:
            print(f"Error saving request data: {str(e)}")

    def save_response_data(self, city_name: str, response_data: dict) -> None:

        try:
            # Insert request data
            insert_request_query = "INSERT INTO requests DEFAULT VALUES RETURNING requestid;"
            self.cursor.execute(insert_request_query)
            request_id = self.cursor.fetchone()[0]

            # Insert response data
            insert_response_query = "INSERT INTO response (requestid, temperature, city_name) VALUES (%s, %s, %s);"
            temperature = response_data["temp"]
            self.cursor.execute(insert_response_query,
                                (request_id, temperature, city_name))

            self.conn.commit()
            print("Response data saved successfully.")
        except Exception as e:
            print(f"Error saving response data: {str(e)}")

    def get_request_count(self) -> int:
        try:
            count_query = "SELECT COUNT(*) FROM requests;"
            self.cursor.execute(count_query)
            count = self.cursor.fetchone()[0]
            return count
        except Exception as e:
            print(f"Error retrieving request count: {str(e)}")

    def get_successful_request_count(self) -> int:
        try:
            count_query = "SELECT COUNT(*) FROM response WHERE temperature IS NOT NULL;"
            self.cursor.execute(count_query)
            count = self.cursor.fetchone()[0]
            return count
        except Exception as e:
            print(f"Error retrieving request count: {str(e)}")

    def get_last_request(self) -> Tuple[str, str]:
        try:
            query = "SELECT city_name, datetime FROM requests ORDER BY datetime DESC LIMIT 1;"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if result:
                city_name = result[0]
                datetime_str = result[1].isoformat()
                return city_name, datetime_str

        except Exception as e:
            print(f"Error retrieving last request: {str(e)}")

    def get_city_request_count(self) -> List[Tuple[str, int]]:
        try:
            query= "SELECT city_name, COUNT(*) FROM requests GROUP BY city_name "
            self.cursor.execute(query)
            resault=self.cursor.fetchall()
            counting=[(city_name,count) for city_name, count in resault]
            return counting
        except Exception as e:
            print(f"Error retrieving counting request: {str(e)}")

ct = WeatherDatabase()
ct.create_tables()
