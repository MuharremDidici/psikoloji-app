import os

directories = [
    'templates',
    'templates/admin',
    'static',
    'static/css',
    'static/js',
    'static/images'
]

for dir in directories:
    os.makedirs(dir, exist_ok=True)
