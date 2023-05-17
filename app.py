from flask import Flask, render_template, request, redirect,send_from_directory
from flask_frozen import Freezer
from flask_sitemap import Sitemap
import requests
import os

app = Flask(__name__)
freezer = Freezer(app)
ext = Sitemap(app=app)
output_folder = os.path.join(app.config['FREEZER_DESTINATION'], 'p')
@app.route('/')
def index():
    return render_template('Auth.html')

@app.route('/dashboard.html')
def redirects():
    return render_template('index.html')

@app.route('/p/<user_input>.html')
def redirected_page(user_input):
    temp = render_template('redirect_page.html', user_input=user_input)
    return temp

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory('build', 'robots.txt')


@app.route('/S.html')
def Success():
    return render_template('Success.html')

@app.route('/E.html')
def Edit():
    return render_template('Edit.html')

@freezer.register_generator
@ext.register_generator
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
    app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True
    freezer.freeze()