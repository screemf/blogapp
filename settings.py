import os
import sys

# Безопасность
SECRET_KEY = '4x9ok*2gtk)+h)qu!178pv38t675j3dx%@a1*ju+j95&u7lktp'  # Ваш ключ (32+ символов)
DEBUG = True  # Для разработки
ALLOWED_HOSTS = ['*']  # Для тестов

# Отключение HTTPS-настроек (для локальной разработки)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Статические файлы
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]