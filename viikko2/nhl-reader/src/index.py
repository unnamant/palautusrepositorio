from player import PlayerReader, PlayerStats
from rich.console import Console
from rich.table import Table

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    season = input("Season: ")
    nationality = input("Nationality: ")

    players = stats.top_scorers_by_nationality(nationality)
    
    console = Console()

    table = Table(title=f"{season} players from {nationality}")
    table.add_column("Released", style="cyan")
    table.add_column("Team", style="magenta")
    table.add_column("Goals", justify="right", style="yellow")
    table.add_column("Assists", justify="right", style="yellow")
    table.add_column("Points", justify="right", style="yellow")

    for player in players:
        table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.goals + player.assists))

    console.print(table)

if __name__ == "__main__":
    main()
