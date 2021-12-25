from .banners import BANNERS
from .colors import Colors
from random import choice

ABOUT = """nuclipy - Template Based Vulnerability Scanner inspired by Nuclei
https://github.com/prasant-paudel/nuclipy
"""
COLORS = [Colors.RED, Colors.GREEN, Colors.BLUE, Colors.MAGENTA, Colors.CYAN]

print(
    choice(COLORS) 
    + choice(BANNERS.split('---split---'))
    + '\n' + ABOUT
    + Colors.RESET)

