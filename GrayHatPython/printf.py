import os
from ctypes import *

if os.name == 'nt':
    msvcrt = cdll.msvcrt
    msvcrt.printf(b"Hello from the Windows c runtime!\n")
elif os.name == 'posix':
    libc = CDLL("libc.so.6")
    libc.printf(b"Hello from the Linux c runtime!\n")
else:
    print("Unsupported OS")
