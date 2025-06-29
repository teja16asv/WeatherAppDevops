from flask import Flask, jsonify, request, render_template
import requests, datetime

app = Flask(__name__)
API_KEY = "1bd12b45b2f1c67073f09ca94002244f"  # paste your valid key here

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city", "Hyderabad")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url).json()

    if res.get("cod") != 200:
        return render_template("index.html", error=res.get("message", "API failed"))

    temp = res["main"]["temp"]
    log = f"{datetime.datetime.now()} | {city} | {temp}°C\n"
    with open("logs.txt", "a") as f:
        f.write(log)

    return render_template("index.html", city=city, temp=temp)

@app.route("/logs")
def show_logs():
    with open("logs.txt", "r") as f:
        lines = f.readlines()[-10:]
    return jsonify({"logs": lines})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

