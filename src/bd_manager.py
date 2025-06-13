import psycopg2


class DBManager:
    """Класс для подключения к БД PostgreSQL"""

    def __init__(self, user, password, host, database, port):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.conn = None
        self.cur = None


    def connect_db(self):
        """Метод подключения к БД"""

        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port
        )

    def get_companies_and_vacancies_count(self):
        """Метод получения списка всех компаний и количество вакансий у каждой компании."""

        cur = self.conn.cursor()
        cur.execute(
            """
             SELECT name_employers, COUNT(*)
             FROM employers
             JOIN vacancies on employers.employers_id = vacancies.employers_id
             GROUP BY name_employers
             """
        )
        result = cur.fetchall()
        cur.close()
        return result

    def get_all_vacancies(self):
        """Метод получения списка всех вакансий
        с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""

        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT 
            name_employers, name_vacancies, salary_from || '-' || salary_to, url_vacancies
            FROM employers
            JOIN vacancies on employers.employers_id = vacancies.employers_id
        """
        )
        result = cur.fetchall()
        cur.close()
        return result

    def get_avg_salary(self):
        """Метод получения средней зарплаты по вакансиям."""

        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT 
            (AVG(vacancies.salary_from + vacancies.salary_to)) / 2 as average_salary
            FROM 
            vacancies
            WHERE 
            salary_from > 0
            AND 
            salary_to > 0
            """
        )
        result = cur.fetchone()
        cur.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """Метод получения списка всех вакансий,
        у которых зарплата выше средней по всем вакансиям."""

        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT *
            FROM
            vacancies
            WHERE
            salary_to > (SELECT 
            (AVG(vacancies.salary_from + vacancies.salary_to)) / 2 as average_salary
            FROM 
            vacancies
            WHERE 
            salary_from > 0
            AND 
            salary_to > 0)
            """
        )
        result = cur.fetchall()
        cur.close()
        return result

    def get_vacancies_with_keyword(self, search_word=None):
        """Метод получения списка всех вакансий,
        в названии которых содержатся переданные
        в метод слова."""

        cur = self.conn.cursor()

        if not search_word:
            cur.execute(
                """
                      SELECT *
                      FROM
                      vacancies                      
                      """
            )
            result = cur.fetchall()
            cur.close()
            return result

        cur.execute(
            f"""
            SELECT * FROM vacancies
            WHERE name_vacancies iLIKE '%{search_word}%'
            """
        )

        result = cur.fetchall()
        cur.close()
        return result