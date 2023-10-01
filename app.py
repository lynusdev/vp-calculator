import requests, os
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

def skin_cost(points):
    tr_response = requests.get("https://web.rgl.gw.pay.riotgames.com/riotpay/psps/paypalrest/currency-conversion/8827b477-eac7-4f4c-a230-fa7b8d48c24d")
    tr_bundle_cost = float(tr_response.text.split('<span id="target-price">')[1].split('</span>&nbsp;')[0])
    tr_cost_per_one = tr_bundle_cost / 11250
    tr_skin_cost = round(points * tr_cost_per_one, 2)
    return tr_skin_cost

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        vp = request.form["vp"]
        if vp == "":
            return render_template("index.html")
        else:
            tr_price = skin_cost(float(vp))
            return render_template("price.html", tr_price=tr_price)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run()