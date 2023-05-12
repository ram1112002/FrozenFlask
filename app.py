from flask import Flask, render_template, request, redirect
from flask_frozen import Freezer
import requests
import os


app = Flask(__name__)
freezer = Freezer(app)
output_folder = os.path.join(app.config['FREEZER_DESTINATION'], 'p')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/I.html')
def redirects():
    return render_template('index.html')

@app.route('/p/<user_input>.html')
def redirected_page(user_input):
    temp = render_template('redirect_page.html', user_input=user_input)
    return temp

@freezer.register_generator
def redirected_page():
    api_endpoint = "https://biodata.fastgen.com/get-user"
    headers = {}
    response = requests.get(api_endpoint,headers  = headers)
    if response.status_code == 200:
        result = response.json()
        data = result["dataHere"]
        res = data['Result']
        name = []
        if(res != None):
            for i in res:
                name.append(i.get("name"))
            print(name)
            for j in name:
                yield {'user_input': j}
    else:
        print("Error occurred:", response.status_code)
    
if __name__ == '__main__':
    app.config['FREEZER_DESTINATION'] = 'build'
    freezer.freeze()
    app.run()