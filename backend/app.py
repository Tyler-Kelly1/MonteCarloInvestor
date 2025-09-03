from flask import Flask, request, jsonify
from flask_cors import CORS  # allow React (different port) to access
from utils.engine import SimulationConditions

app = Flask(__name__)
CORS(app)  # enable cross-origin requests

@app.route('/calculate', methods=['POST'])
def calculate():
    
    data = request.get_json()
    principle = data.get('principle')
    monthly = data.get('monthly')
    duration = data.get('duration')
    simCount = data.get('simCount')
    
    if simCount < 1 or duration < 1:
        return jsonify({"Error": True})
    
    base = SimulationConditions(principle, monthly, 0)
    
    result = base.monteCarloSim(simCount, duration)
    stats = base.calcStats(result,duration)
        
    # Example calculation
    return base.JSONFY(result, stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
