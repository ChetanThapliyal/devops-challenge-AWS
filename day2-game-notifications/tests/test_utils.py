from utils import format_game_data

def test_format_game_data_final():
    game = {
        'Status': 'Final',
        'AwayTeam': {'Name': 'Lakers'},
        'HomeTeam': {'Name': 'Warriors'},
        'AwayTeamScore': 102,
        'HomeTeamScore': 100,
    }
    
    result = format_game_data(game)
    
    assert result == "Lakers vs Warriors: 102-100"

def test_format_game_data_in_progress():
    game = {
        'Status': 'InProgress',
        'AwayTeam': {'Name': 'Celtics'},
        'HomeTeam': {'Name': 'Bulls'},
        'AwayTeamScore': None,
        'HomeTeamScore': None,
    }
    
    result = format_game_data(game)
    
    assert result == "Celtics vs Bulls is currently in progress."

def test_format_game_data_no_details():
    game = {
        'Status': '',
        'AwayTeam': {'Name': ''},
        'HomeTeam': {'Name': ''},
        'AwayTeamScore': None,
        'HomeTeamScore': None,
    }
    
    result = format_game_data(game)
    
    assert result == "Details are unavailable at this time for this game."