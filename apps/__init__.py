from .banners import BANNERS
from .colors import Colors
from random import choice


ABOUT = """
nuclipy - Template based vulnerability scanner inspired by Nuclei
https://github.com/prasant-paudel/nuclei-python
"""
COLORS = [Colors.RED, Colors.GREEN, Colors.BLUE, Colors.MAGENTA, Colors.CYAN]

print(
    choice(COLORS) 
    + choice(BANNERS.split('---split---'))
    + '\n' + ABOUT
    + Colors.RESET)

