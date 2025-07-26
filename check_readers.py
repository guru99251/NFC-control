# check_readers.py
from smartcard.System import readers

r = readers()
print("Detected PC/SC readers:", r)
