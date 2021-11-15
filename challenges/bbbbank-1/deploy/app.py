from flask import Flask
from flask import request
from bs4 import BeautifulSoup

app = Flask(__name__, static_url_path='', 
            static_folder='static')

coins = {"Balleons":0, "Bickles":1, "Bnuts":2}
houses = {"Bryffindor": [100, 100, 100], "Bavenclaw": [100, 100, 100], "Bufflepuff": [100, 100, 100], "Blytherin": [100, 100, 100]}

@app.route('/', methods = ['GET'])
def index1(bbbtag=None):
    with open("src/index.html", 'r') as index:
        html = index.read()
        soup = BeautifulSoup(html, 'html.parser')
        scores = soup.find(id="score")
        if bbbtag != None:
            scores.append(bbbtag)
        for house, score in houses.items():
            new_tag = soup.new_tag("p")
            new_tag.string = house + ": " + str(score[0]) + " Balleons, " + str(score[1]) + " Bickles, and " + str(score[2]) + " Bnuts."
            scores.append(new_tag)
        return(str(soup))

@app.route('/barry-botter-and-the-bransfer-of-boney', methods = ['POST'])
def transfer():
    data = request.form
    
    if not data["amt"].isnumeric():
        data = "Amount to transfer must be an integer."
    elif data["fhouse"] not in houses.keys():
        data = "Invalid From House."
    elif data["thouse"] not in houses.keys():
        data = "Invalid To House."
    elif houses[data["fhouse"]][coins[data["cointype"]]] < int(data["amt"]):
        data = "Not enough money in the original house"
    elif data["cointype"] not in coins.keys():
        data = "Invalid coin type"
    else:
        houses[data["fhouse"]][coins[data["cointype"]]] -= int(data["amt"])
        houses[data["thouse"]][coins[data["cointype"]]] += int(data["amt"])
        data = "Success!"
    with open("src/index.html", 'r') as index:
        html = index.read()
        soup = BeautifulSoup(html, 'html.parser')
        new_tag = soup.new_tag("p")
        new_tag.string = str(data)
        return index1(bbbtag=new_tag)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')