
from ctypes import *

msvcrt = cdll.msvcrt

msvcrt.printf(b"Hello from c!\n")