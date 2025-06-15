import psycopg2
import os

from config import config
from src.api_request_HH import HeadHunterAPI
from src.utils import create_database, create_tables, save_data_to_database
from src.bd_manager import DBManager
from dotenv import load_dotenv


load_dotenv()
bd_con = DBManager(
    database=os.getenv("DTBASE_NAME"),
    password=os.getenv("DTBASE_PASSWORD"),
    user=os.getenv("DTBASE_USER"),
    host=os.getenv("DTBASE_HOST"),
    port=os.getenv("DTBASE_PORT")
)


def main() -> None:
    params = config()                                           # получение параметров для подключения БД postgres
    database_name = os.getenv("DTBASE_NAME")                    # название свое БД в postgres
    create_database( database_name, params)                     # создания свое БД в postgres
    conn = psycopg2.connect(dbname=database_name, **params)     # подключение к своей БД
    create_tables(conn)                                         # создание таблиц в БД

    text = "Экономист"
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.load_vacancies(text)                  # получение данных с HeadHunter

    conn = psycopg2.connect(dbname=database_name, **params)
    save_data_to_database(hh_vacancies, conn)                   # заполнение таблиц данными
    bd_con.connect_db()
    print(bd_con.get_companies_and_vacancies_count())
    print(bd_con.get_all_vacancies())
    print(bd_con.get_avg_salary())
    print(bd_con.get_vacancies_with_higher_salary())
    print(bd_con.get_vacancies_with_keyword('Бухгалтер'))


if __name__ == "__main__":
    main()
