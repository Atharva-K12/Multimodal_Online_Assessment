from app import Create_app

app = Create_app('../config.py')

if __name__ == '__main__':
    app.run()