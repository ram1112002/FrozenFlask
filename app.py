from flask import Flask, render_template, request, redirect
from flask_frozen import Freezer
import requests
import os


app = Flask(__name__)
freezer = Freezer(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/p', methods=['POST'])
def redirect_page():
    user_name = request.form['user_input']
    user_email = request.form['user_email'].lower()
    user_edu = request.form['user_edu']
    user_dob = request.form['user_dob']
    data = {
            "name": user_name,
            "email": user_email,
            "qualification": user_edu,
            "date_of_birth": user_dob
        }
    headers = {}
    api_endpoint = "https://biodata.fastgen.com/create-user"
    response = requests.post(api_endpoint,headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        print("Data sent successfully")
    else:
        print("Error occurred", response.status_code)
    return redirect('/p/' + user_name)


def StaticFile(user_input):
    template = render_template('redirect_page.html', user_input=user_input)
    
    output_filename = f"{user_input}.html"

    with open(os.path.join(app.static_folder, output_filename), 'w') as file:
        file.write(template)

@app.route('/p/<user_input>')
def redirected_page(user_input):
    temp = render_template('redirect_page.html', user_input=user_input)
    StaticFile(user_input)
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
                StaticFile(j)
                yield {'user_input': j}
    else:
        print("Error occurred:", response.status_code)
    
if __name__ == '__main__':
    freezer.freeze()
    app.run()
