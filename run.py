from app import create_app

application = create_app()

for rule in application.url_map.iter_rules():
    print(rule)
    
if __name__ == "__main__":
    application.run(debug=True)