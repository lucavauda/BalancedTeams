# BalancedTeams
⚽ A fun Python script that lets you build balanced 7v7 football teams based on player strength ratings and positions.

## Overview

This script helps football/soccer organizers create two evenly matched teams from a pool of players. It:

1. Takes player data with name, strength ratings (1-10), and positions (ATT, DEF, GK, or ATT/DEF)
2. Generates the best 5 combinations
3. Filters for teams that satisfy formation requirements (e.g., 3 attackers, 3 defenders, 1 goalkeeper)
4. Ranks combinations by how balanced they are (minimal strength difference)
5. Visualizes the top balanced team setups on a football pitch using matplotlib

## Features

- **Smart Team Balancing**: Finds the most balanced teams based on player strength
- **Position Awareness**: Ensures each team has the correct number of players in each position
- **Flexible Player Handling**: Accommodates players who can play multiple positions (ATT/DEF)
- **Team Visualization**: Draws the balanced teams on a football pitch with player names and strengths
- **Multiple Options**: Shows several balanced team configurations so you can choose your preference

## Requirements

- Python 3.6+
- Libraries: 
  - matplotlib
  - itertools (standard library)
  - math (standard library)
  - random (standard library)
  - copy (standard library)

## Installation

1. Clone or download this script
2. Install the required packages:
   ```
   pip install matplotlib
   ```

## Usage

1. Edit the `players_data` list in the script to include your players:
   ```python
   players_data = [
       {'name': 'Player1', 'strength': 7, 'position': 'ATT'},
       {'name': 'Player2', 'strength': 8, 'position': 'GK'},
       # Add all your players here
   ]
   ```

2. Customize the configuration variables if needed:
   ```python
   NUM_SIMULATIONS_TO_SHOW = 5  # How many team combinations to display
   TARGET_FIELD_FORMATION = {'ATT': 3, 'DEF': 3}  # Formation (3 attackers, 3 defenders)
   ```

3. Run the script:
   ```
   python team_balancer.py
   ```

4. The script will display:
   - Text output showing several balanced team combinations
   - A matplotlib visualization of the most balanced team configuration

## Player Data Format

- **name**: Player's name (string)
- **strength**: Player's skill level from 1-10 (integer)
- **position**: One of:
  - 'ATT' - Attacker
  - 'DEF' - Defender
  - 'GK' - Goalkeeper
  - 'ATT/DEF' - Flexible player who can play either position

## Requirements

- 14 players (for 7v7 format)
- 2 goalkeepers
- Enough players of each position to satisfy the formation

## Example Output

```
--- Simulation 1 (Rank 1 overall viable) ---
Strength Balance Difference: 0

Team A (Strength: 43, Viable: Yes)
  Alin (6-ATT/DEF), Giano (6-ATT/DEF), Leo (8-GK), Lorenzo (6-DEF), Osmi (4-ATT), Pie (6-DEF), Weste (6-ATT/DEF)

Team B (Strength: 43, Viable: Yes)
  Greg (6-DEF), Luca (6-ATT), Matti (7-ATT), Scarpe (6-DEF), Shimo (8-ATT), Ste (8-GK), Vale (4-ATT)
------------------------------
```

The script will also display a football pitch visualization showing the optimal team placement.

## Customization

You can modify these parameters:

- **TARGET_FIELD_FORMATION**: Change the formation (e.g., `{'ATT': 4, 'DEF': 2}` for 4 attackers, 2 defenders)
- **NUM_SIMULATIONS_TO_SHOW**: Change how many team combinations to display


Designed with the help of Gemini 2.5 Pro, ChatGPT and Claude.
