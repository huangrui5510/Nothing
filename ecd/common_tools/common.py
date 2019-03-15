# coding:utf-8
"""
author: Allen
datetime: 
python version: 3.x
summary: 
install package:
"""
import random
from typing import List

from colorama import Fore


class GenData(object):
    def __init__(self):
        pass

    @staticmethod
    def random_list(start: int = 0, end: int = 10, step: int = 1):
        """generate random list"""
        seq = list(range(start, end, step))
        random.shuffle(seq)
        return seq


class ConsolePrint(object):
    @staticmethod
    def annotation_seq(seq: List, index: int):
        """use color swagger index data"""
        return ' '.join([Fore.RESET + str(d) if i != index else Fore.RED + str(d) for i, d in enumerate(seq)])

    @staticmethod
    def cover_print(data):
        print("\r\r{d}".format(d=str(data).strip()), end='')


if __name__ == '__main__':
    pass
