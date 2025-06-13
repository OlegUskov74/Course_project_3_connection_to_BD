from typing import Any

import psycopg2


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных PostgreSQL."""
    conn = None

    try:
        # Подключение
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {database_name}") # Удаление БД
            cur.execute(f"CREATE DATABASE {database_name}") #Создание БД
        print (f"База {database_name} успешно создана")

    except psycopg2.Error as e:
        print(f"Ошибка создания БД: {e}")
        raise

    finally:
        if conn:
            conn.close() # Закрытие соединения



def create_tables(conn) -> None:
    """Создание таблиц employers и vacancies"""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE employers (
                            employers_id SERIAL PRIMARY KEY, 
                            name_employers VARCHAR (225) NOT NULL, 
                            city TEXT,
                            url_employers TEXT
                        )
                        """)

            cur.execute(
                        """
                        CREATE TABLE vacancies(
                            vacancies_id SERIAL PRIMARY KEY,
                            employers_id INTEGER REFERENCES employers (employers_id),
                            name_vacancies VARCHAR (100) NOT NULL,
                            salary_from INTEGER,
                            salary_to INTEGER,
                            currency VARCHAR (5),
                            requirement TEXT,
                            responsibility TEXT,
                            url_vacancies VARCHAR (225) NOT NULL
                        )
                        """)

        conn.commit()
        print("Создание таблиц employers и vacancies успешно")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"ошибка при создании таблиц: {e}")
        raise
    finally:
        conn.close()

def save_data_to_database(data: list[dict[str, Any]], conn) -> None:
    """Сохранение данных в базу данных."""
    try:
        with conn.cursor() as cur:
            for item in data:
                employers_data = item['employer']['name'] # name, alternate_url
                area = item ['area']
                employers_address = area['name'] if 'name' else None

                if 'employer' in item:
                    if 'alternate_url' in item:
                        url_employers = item['alternate_url']
                else:
                    url_employers = "Нет данных"

                cur.execute(
                    """
                    INSERT INTO employers (name_employers, 
                                            city,
                                            url_employers
                                            )
                    VALUES (%s, %s, %s)
                    RETURNING employers_id
                    """,
                    (employers_data,
                     employers_address,
                     url_employers
                    )
                )

                employers_id = cur.fetchone()[0] # возвращаем employers_id SERIAL

                vacancies_name = item['name']
                vacancies_data = item['snippet'] # requirement, responsibility

                if item['salary'] != None:
                    salary_from = item['salary']['from']
                    salary_to = item['salary']['to']
                    salary_currency = item['salary']['currency']

                if 'alternate_url' in item:
                    url_vacancies = item['alternate_url']
                else:
                    url_vacancies = "Нет данных"

                cur.execute(
                    """
                    INSERT INTO vacancies (employers_id,
                                            name_vacancies,
                                            salary_from,
                                            salary_to,
                                            currency,
                                            requirement,
                                            responsibility,
                                            url_vacancies
                                            )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (employers_id,
                     vacancies_name,
                     salary_from,
                     salary_to,
                     salary_currency,
                     vacancies_data['requirement'],
                     vacancies_data['responsibility'],
                     url_vacancies
                     )
                )

            conn.commit()
            print("Заполнение таблиц employers и vacancies успешно")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"ошибка при создании таблиц: {e}")
        raise
    finally:
        conn.close()
