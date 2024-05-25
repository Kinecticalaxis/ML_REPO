from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load IPL dataset
ipl_data = pd.read_csv('IPL_2019.csv')

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req.get('queryResult').get('intent').get('displayName')

    if intent == 'Match Information Intent':
        match_date = req.get('queryResult').get('parameters').get('match_date')
        response = get_match_info(match_date)
    # Add more intent handling as needed

    return jsonify({'fulfillmentText': response})

def get_match_info(date):
    match = ipl_data[ipl_data['date'] == date]
    if match.empty:
        return 'No match found for the specified date.'
    # Construct response from match data
    return f"On {date}, {match['team1'].values[0]} played against {match['team2'].values[0]} and the winner was {match['winner'].values[0]}."

if __name__ == '__main__':
    app.run(debug=True)
