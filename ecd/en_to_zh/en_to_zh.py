#coding:utf-8
"""
author: Allen
datetime: 
python version: 3.x
summary: 
install package:
"""
class EnToZh(object):
    def __init__(self):
        pass


if __name__ == '__main__':
    import pip
    from pip._internal import main
    import sys
    sys.argv = r"pip install -I -b C:\Users\allen\Desktop\numpy_pkgs\pkgs --cache-dir C:\Users\allen\Desktop\numpy_pkgs\cache numpy --platform linux --python-version 3.7.3 --abi pypy_41 --implementation pp".split(' ')
    main()