# test_import.py

import os
import sys

logapp_path = os.path.abspath(r'D:\Users\scree\PycharmProjects\djangoProject\blogapp')
if blogapp_path not in sys.path:
    sys.path.append(blogapp_path)

try:
    import blogapp

    print('Импорт успешен:', blogapp)
except ModuleNotFoundError as e:
    print('Ошибка импорта:', e)