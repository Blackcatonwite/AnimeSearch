from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GOOGLE_API_KEY = "AIzaSyBGPwE8_LuPsbc6cLLJ9BRKaX2jSMW0Si8"
CSE_ID = "379d83b15180c4058"

def search_google_cse(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": 5,
        "hl": "ru"
    }

    response = requests.get(url, params=params)
    data = response.json()
    results = []
    for item in data.get("items", []):
        results.append({
            "title": item.get("title"),
            "description": item.get("snippet"),
            "link": item.get("link")
        })
    return results

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"results": []})
    results = search_google_cse(query)
    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)
