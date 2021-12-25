from .helper import Helper
from typing import Pattern

class Template:
    def __init__(self, template:str) -> None:
        self.__data = Helper.read_yaml(template)

        self.id:str = self.__data['id']
        self.name:str = self.__data['name']
        self.severity:str = self.__data['severity']
        self.requests = [self.R(_) for _ in self.__data['requests']]

    class R:
        def __init__(self, data:dict) -> None:
            self.method:str = data['method']
            self.paths:list[str] = data['paths']
            self.patterns:list[Pattern] = [Helper.re_compile(_.strip()) for _ in data['patterns']]
            try:
                self.redirects:bool = data['redirect']
            except KeyError:
                self.redirects:bool = False