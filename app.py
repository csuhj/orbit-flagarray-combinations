from flask import Flask, render_template, request
from apteco import login_with_password
import apteco_api as aa
import sys
import time
import threading

app = Flask(__name__)

def request_cube_for_variable(variable_name):
    variable = session.variables[variable_name]
    table = variable.table
    cube = table.cube([variable])
    df = cube.to_df()
    return df

@app.route('/')
def index():
    return cubeForVariable('Income')

@app.route('/<variable_name>')
def cubeForVariable(variable_name):
    df = request_cube_for_variable(variable_name)
    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python app.py [API base url] [dataview] [systemname] [username] [password]')
        exit(1)
    
    apiUrl = sys.argv[1]
    dataView = sys.argv[2]
    systemName = sys.argv[3]
    username = sys.argv[4]
    password = sys.argv[5]

    session = login_with_password(apiUrl, dataView, systemName, username, password)
    app.run(debug=False, host='0.0.0.0', port=int('8081'))