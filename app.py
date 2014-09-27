from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    pass

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug=True)
