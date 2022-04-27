from flask import Flask
from flask import render_template
from flask import request
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('./index.html', test='')  # index.html


@app.route('/res', methods=['POST', 'GET'])  # res.html
def res():
    search = request.form['search']

    url = 'https://api.hatchways.io/assessment/blog/posts?tag=tech' + search
    try:
        res = requests.get(url).json()
        res = res['posts']
        ilist = []
        for i in res:
            ilist.append(i)
        option = request.form['order']
        if option == 'asc':
            ilist.sort(key=lambda x: x.get('tags'))
        elif option == 'dsc':
            ilist.sort(key=lambda x: x.get('tags'), reverse=True)

        if not ilist:
            output = '{<br>'
            output = output + '"error": "Tags parameter is required" <br>'
            output = output + '}'
            return output

        return render_template('./res.html', test=ilist)

    except requests.ConnectionError:
        return "Connection Error"


if __name__ == '__main__':
    app.run(debug=True)
