import math, random
from random import randint

# function to generate OTP
def generateOTP(n=4):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)