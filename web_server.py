from flask import Flask, request
from resources import EntryManager, Entry

app = Flask(__name__)
FOLDER = '.'


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/entries/")
def get_entries():
    entry = EntryManager(FOLDER)
    entry.load()
    entry_list = []
    for en in entry.entries:
        entry_list.append(en.json())
    return entry_list


@app.route("/api/save_entries/", methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER)
    entry_list = request.get_json()
    for single_entry in entry_list:
        entry = Entry.from_json(single_entry)
        entry_manager.entries.append(entry)
        entry_manager.save()
    return {'status': 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False)