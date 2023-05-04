from flask import Flask, request,render_template,jsonify
from sudokusolver import startSolver

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return render_template("index.html")
@app.route('/solvesudoku', methods=['POST'])
def solve_sudoku_route():
    data = request.get_json()
    
    sudoku = data['data']
    puzzle = startSolver(sudoku)
   
    return puzzle


app.run()
