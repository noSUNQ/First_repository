# project/run.py

from app import create_app

app = create_app()

# Delete
print("Роуты Flask:")
for rule in app.url_map.iter_rules():
    print(f"  {rule.endpoint} → {rule}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)