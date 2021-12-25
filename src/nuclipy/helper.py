from .colors import Colors
from functools import lru_cache
from os import get_terminal_size
from re import compile
from requests import get as _get
from typing import Pattern
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class Helper:

    @staticmethod
    @lru_cache(maxsize=50)
    def get(url: str, redirects:bool=False) -> str:
        try:
            with _get(url, allow_redirects=redirects) as resp:
                if resp.status_code == 200:
                    return resp.text
                return f"[!] Status: {resp.status_code}"
        except Exception as e:
            return f"[!] Connectioin Error: {e}"


    @staticmethod
    @lru_cache(maxsize=10)
    def checkPattern(string: str, regex: Pattern) -> bool:
        return regex.findall(string).__len__() > 0


    @staticmethod
    @lru_cache(maxsize=10)
    def re_compile(pattern:str) -> Pattern:
        '''Cached function to compile regex patterns'''
        return compile(pattern)


    @staticmethod
    def check_and_patterns(string:str, patterns:list[Pattern]) -> bool:
        '''
        Check a string for multiple regex patterns with AND condition
        '''
        __results:list[bool] = [Helper.checkPattern(string, _) for _ in patterns]
        return not (False in __results)


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


    @staticmethod
    def chunkify(iterable, thread_count):
        chunksize = int(len(iterable) / thread_count)
        if chunksize <= 1:
            return [[_] for _ in iterable]
        return [iterable[_:_+chunksize] for _ in range(0, len(iterable), chunksize)]