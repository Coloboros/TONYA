import os

templates_path = os.path.join(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3]), 'templates')
static_path = os.path.join(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3]), 'static')

from flask import Flask

app = Flask(__name__, template_folder=templates_path, static_folder=static_path)

from source.db.database import DataBase
db = DataBase()

routes_dir_name = 'routes'
routes_path = os.path.join(os.path.dirname(__file__), routes_dir_name)



for module in os.listdir(routes_path):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__('source.server.' + routes_dir_name + '.' + module[:-3], locals(), globals())
    del module

if __name__ == "__main__":
    app.run(host='0.0.0.0')