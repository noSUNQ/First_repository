# venv
cd tg1
python -m venv venv #Создание

venv\Scripts\activate #Активация (Windows)
source venv/bin/activate #Активация (Linux)

deactivate #Деактивация

#
"Python: Select Interpreter"

# git
git add <file>  #Добавить определенный файл/папку
git add .       #Добавить все кроме .gitignore
git commit -m "Примечание" 
git push 

# ngrok
ngrok http 127.0.0.1:5000

# requirements
pip freeze > requirements.txt   #Фиксирует все пакеты из вирт среды
pip install -r requirements.txt #Установка библиотек

# Migrations
flask db init # Создаст migrations/
flask db migrate -m "Add Chat model" # Генерирует скрипт изменений
flask db upgrade # Применить

flask db downgrade # Откат
flask db show # Список миграций

# .env

EMAIL
PASSWORD

# Structure
project/
├─ .vscode/     (скрыт)
|  ├─ settings.json
|
├─ app/
|  ├─ auth/             (blueprints)
|  |  ├─ templates/auth/index.html
|  |  ├─ static/auth/css/style.css
|  |  ├─ __init__.py
|  |  ├─ routes.py
|  | 
|  ├─ main/             (blueprints)
|  ├─ models/
|  |  ├─ __init__.py
|  |  ├─ chat.py        (tables)
|  |  └─ user.py        (tables)
|  | 
|  ├─ __init__.py
|  └─ extensions.py
|
├─ migrations/
├─ static/
|  ├─ css/
|  ├─ img/
|  └─ js
|
├─ templates/
├─ venv/    (скрыт)
├─ .env     (скрыт)
├─ .gitignore
├─ config.py
├─ requirements.txt
└─ wsgi.py