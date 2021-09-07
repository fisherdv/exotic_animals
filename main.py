from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<int:id>')
def post(id: int):
    return render_template('post.html')


@app.route('/edit')
@app.route('/edit/<int:id>')
def edit(id: int = None):    
    return render_template('edit.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")