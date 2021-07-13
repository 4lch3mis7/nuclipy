from functools import cache, lru_cache
from os import listdir, get_terminal_size
from os.path import exists
from sys import argv
from requests import get as _get
from re import compile, template
from typing import Pattern
from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class Colors:
    BLACK =  "\u001b[30m"
    RED =  "\u001b[31m"
    GREEN =  "\u001b[32m"
    YELLOW =  "\u001b[33m"
    ORANGE = "\u001b[38;5;208m"
    ORNAGE_YELLOW = "\u001b[38;5;184m"
    BLUE =  "\u001b[34m"
    MAGENTA =  "\u001b[35m"
    CYAN =  "\u001b[36m"
    WHITE =  "\u001b[37m"
    RESET =  "\u001b[0m"



class Expose:

    def __init__(self) -> None:
        self.all_templates = listdir("templates/")


    def check_all(self, hostname:str) -> None:
        for _ in listdir('templates/'):
            self.__check("templates/"+_, hostname)


    def check_one(self, template:str, hostname:str) -> None:
        if not exists(template):
            template = f"templates/{template.strip('templates/').strip('.yaml')}.yaml"
            if not exists(template):
                return
        print(template)
        self.__check(template, hostname)


    def __check(self, template_path:str, hostname:str):
        template = Template(template_path)

        Helper.clear_line()
        # print(Colors.GREEN + "[+] Checking: " + template.name + Colors.RESET, end='\r')
        print(Colors.GREEN + "[+] Checking: " + template.name + Colors.RESET)

        for req in template.requests:
            for path in req.paths:
                path = 'http://'+path.strip().replace('HOSTNAME', hostname)
                __condition = False
                for pattern in req.patterns:
                    __condition = Helper.checkPattern(Helper.get(path, req.redirects), pattern)

                    if pattern.findall(Helper.get(path, req.redirects)).__len__() > 0:
                        Helper.clear_line()
                        Helper.color_display(f"[+][{template.severity.upper()}] {template.name}: {path}")
                        break


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


class Helper:
    @staticmethod
    @lru_cache(maxsize=128)
    def get(url: str, redirects:bool=False) -> str:
        try:
            with _get(url, allow_redirects=redirects) as resp:
                if resp.status_code == 200:
                    return resp.text
                return f"[!] Status: {resp.status_code}"
        except Exception as e:
            return f"[!] Connectioin Error: {e}"

    @staticmethod
    @lru_cache(maxsize=5)
    def checkPattern(string: str, regex: Pattern) -> bool:
        return regex.findall(string).__len__() > 0

    def check_and_patterns(string:str, patterns:list[Pattern]) -> bool:
        '''
        Check a string for multiple regex patterns with AND condition
        '''
        __results:list[bool] = [Helper.checkPattern(string, _) for _ in patterns]
        return not (False in __results)




    @staticmethod
    @cache
    def re_compile(pattern:str) -> Pattern:
        '''
        Cached function to compile regex patterns
        '''
        return compile(pattern)

    @staticmethod
    def read_yaml(file_path: str) -> dict:
        with open(file_path) as f:
            return load(f.read(), Loader)
    
    @staticmethod
    def color_display(string:str) -> None:
        if string[4:7] == "INF":
            print(Colors.BLUE + string + Colors.RESET)
        elif string[4:7] == "LOW":
            print(Colors.CYAN + string + Colors.RESET)
        elif string[4:7] == "MED":
            print(Colors.ORANGE + string + Colors.RESET)
        elif string[4:7] == "HIG":
            print(Colors.RED + string + Colors.RESET)
        else:
            print(string)
    
    @staticmethod
    def clear_line() -> None:
        '''
        Clear the current line but do not move cursor to the nex line
        '''
        print(f"{get_terminal_size()[0] * ' '}\r", end="", flush=True)





if __name__ == '__main__':
    x =  Expose()
    x.check_all(argv[1])

    
