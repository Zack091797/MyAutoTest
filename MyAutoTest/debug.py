import random


def get_random():
    num = random.randint(1, 100)
    return num


def get_name_and_age(name):
    return name, get_random()