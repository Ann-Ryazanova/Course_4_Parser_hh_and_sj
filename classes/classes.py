from abc import ABC, abstractmethod


class Engine(ABC):
    """
    Абстрактный метод от, которого наследуются HeadHunterAPI() и SuperJobAPI()
    """

    @abstractmethod
    def get_request(self):
        pass
