from abc import ABC, abstractmethod
from typing import Dict, List

import requests


class BaseHeadHunterAPI(ABC):
    """Базовый класс для взаимодействия с платформой HH.ru"""

    @abstractmethod
    def load_vacancies(self, text: str) -> List[Dict]:
        pass


class HeadHunterAPI(BaseHeadHunterAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self) -> None:
        """Метод для инициализации экземпляра класса"""
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params: dict = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies: list = []

    def load_vacancies(self, keyword: str) -> list:
        """Метод для получения списка вакансий"""

        self.__params["text"] = keyword
        self.__params["page"] = 0
        while self.__params.get("page") != 2:

            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            if response.status_code == 200:
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
                self.__params["page"] += 1

        return self.__vacancies

# if __name__ == '__main__':
#     hh_api = HeadHunterAPI()
#     hh_vacancies = hh_api.load_vacancies("Python")
#     print(hh_vacancies)