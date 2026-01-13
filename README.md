# First_repository
Мой первый репозиторий созданный в рамках курса cs50 Web

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

# venv
cd tg1
python -m venv venv #Создание

venv\Scripts\activate #Активация (Windows)
source venv/bin/activate #Активация (Linux)

deactivate #Деактивация

# Migrations
flask db init # Создаст migrations/
flask db migrate -m "Add Chat model" # Генерирует скрипт изменений
flask db upgrade # Применить

flask db downgrade # Откат
flask db show # Список миграций