from app import create_app

app = create_app() # import the app i.e calling __init__.py in app folder

if __name__ == '__main__':
    app.run(debug=False) # debug is true while development and testing 
