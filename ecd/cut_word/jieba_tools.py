# coding:utf-8
"""
author: Allen
email: lingyunzou@aliyun.com
datetime: 2018/12/17
python version: 3.x
summary: 解决 jieba 自定义词不能包含特殊符号
install package:
"""
import jieba
import string
import random
import re
from jieba import posseg


class JiebaObj:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if getattr(cls, "_instance") is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.symbol_map = {}
        self.sym_flag = "symbol"
        self.alphabets = list(string.ascii_lowercase)
        self.key_num = 15  # 随机字符串的长度
        self.d_word_freq = 30000000  # 自定义词性的默认词频
        self.jieba = jieba
        self.posseg = posseg
        self.symbol_p = re.compile(r'\W')

    def add_word(self, word, freq=None, tag=None):
        """添加词"""
        word = self.tarnsform_word(word)
        self.jieba.add_word(word, freq=freq or self.d_word_freq, tag=tag)

    def reverse_symbol(self, word: str) -> str:
        """将带符号的字符串恢复成原始的字符串"""
        sym_keys = [s for s in self.symbol_map.keys() if len(s) > 1]
        for s in sym_keys:
            raw_sym = self.symbol_map.get(s, None)
            if raw_sym is None:
                raise ValueError
            word = word.replace(s, raw_sym)
        return word

    def posseg_cut(self, text: str) -> list:
        """对应 jieba.posseg.cut"""
        text = self.tarnsform_word(text)
        cuts = self.posseg.cut(text)
        return [
            (self.reverse_symbol(w), list(self.posseg.cut(self.reverse_symbol(w)))[0].flag) if f == self.sym_flag else (
            self.reverse_symbol(w), f) for w, f in cuts]

    def tarnsform_word(self, sentence: str) -> str:
        """将字符串中的符号进行映射，转换字符串成"""
        symbols = self._detect_symbol(sentence)
        for sym in symbols:
            if sym not in self.symbol_map:
                self.transform_symbol(sym)
            sentence = sentence.replace(sym, self.symbol_map[sym])
        return sentence

    def _detect_symbol(self, sentence: str) -> list:
        """提取字符串中的符号"""
        symbols = self.symbol_p.findall(sentence)
        return list(filter(None, symbols))

    def transform_symbol(self, symbol: str) -> str:
        """将符号转换成随机字符串"""
        key = ''
        while symbol not in self.symbol_map:
            random.shuffle(self.alphabets)
            key = ''.join(self.alphabets[:self.key_num])
            if key not in self.symbol_map:
                self.symbol_map[key] = symbol
                self.symbol_map[symbol] = key
                self.jieba.add_word(word=key, tag=self.sym_flag, freq=self.d_word_freq)
                break
        return key


def demo():
    """使用示例"""

    text = "今 天?天气不错，=="
    jo = JiebaObj()
    jo.add_word("今 天?", tag='weather')
    jo.add_word("不错，", tag='nothing')
    flags = jo.posseg_cut(text)
    print(flags)  # [('今 天', 'hh'), ('天气', 'n'), ('不错', 'a')]


if __name__ == '__main__':
    demo()
