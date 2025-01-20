def format_game_data(game):
    """Format game data into a human-readable message."""
    status = game['Status']
    away_team = game['AwayTeam']['Name']
    home_team = game['HomeTeam']['Name']
    away_score = game['AwayTeamScore']
    home_score = game['HomeTeamScore']

    if status == "Final":
        return f"{away_team} vs {home_team}: {away_score}-{home_score}"
    elif status == "InProgress":
        return f"{away_team} vs {home_team} is currently in progress."
    else:
        return "Details are unavailable at this time for this game."