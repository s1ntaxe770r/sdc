from flask import Flask,render_template


app = Flask(__name__)



@app.route('/',methods=['GET'])
def index():
	render_template('index.html')



