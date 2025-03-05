import sys

print('Список параметров, переданных скрипту')
print(sys.argv)

print([arg for arg in sys.argv if arg[0] != '-'])
