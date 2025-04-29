import itertools
import random
import matplotlib.pyplot as plt
import math
from copy import deepcopy # Might be needed for complex assignments

# --- Player Data ---
players_data = [
    {'name': 'Weste', 'strength': 6, 'position': 'ATT/DEF'},
    {'name': 'Ste', 'strength': 8, 'position': 'GK'},
    {'name': 'Osmi', 'strength': 4, 'position': 'ATT'},
    {'name': 'Greg', 'strength': 6, 'position': 'DEF'},
    {'name': 'Vale', 'strength': 4, 'position': 'ATT'},
    {'name': 'Pie', 'strength': 6, 'position': 'DEF'},
    {'name': 'Matti', 'strength': 7, 'position': 'ATT'},
    {'name': 'Leo', 'strength': 8, 'position': 'GK'},
    {'name': 'Luca', 'strength': 6, 'position': 'ATT'},
    {'name': 'Scarpe', 'strength': 6, 'position': 'DEF'},
    {'name': 'Lorenzo', 'strength': 6, 'position': 'DEF'},
    {'name': 'Shimo', 'strength': 8, 'position': 'ATT'},
    {'name': 'Giano', 'strength': 6, 'position': 'ATT/DEF'},
    {'name': 'Alin', 'strength': 6, 'position': 'ATT/DEF'},
]

# --- Configuration ---
NUM_SIMULATIONS_TO_SHOW = 5 # How many top results to display
TARGET_FIELD_FORMATION = {'ATT': 3, 'DEF': 3} # 3 attackers, 3 defenders

# --- Helper Functions ---
def get_team_strength(team):
    """Calculates the total strength of a list of players."""
    return sum(player['strength'] for player in team)

def format_team(team):
    """Formats a team list for printing."""
    return ", ".join(f"{p['name']} ({p['strength']}-{p['position']})"
                     for p in sorted(team, key=lambda x: x['name']))

def check_positional_viability(team, target_formation):
    """
    Checks if a team *can* field the target number of attackers and defenders,
    using flexible players where needed. Excludes the GK.
    """
    field_players = [p for p in team if p['position'] != 'GK']
    target_att = target_formation.get('ATT', 0)
    target_def = target_formation.get('DEF', 0)
    target_total_field = target_att + target_def

    if len(field_players) != target_total_field:
        # print(f"Warning: Team size mismatch. Expected {target_total_field} field players, got {len(field_players)}")
        return False # Or handle differently if variable team sizes are allowed

    pure_att = sum(1 for p in field_players if p['position'] == 'ATT')
    pure_def = sum(1 for p in field_players if p['position'] == 'DEF')
    flexible = sum(1 for p in field_players if p['position'] == 'ATT/DEF')

    # Can we reach the target number of attackers?
    min_possible_att = pure_att
    max_possible_att = pure_att + flexible
    att_possible = (min_possible_att <= target_att <= max_possible_att)

    # Can we reach the target number of defenders?
    min_possible_def = pure_def
    max_possible_def = pure_def + flexible
    def_possible = (min_possible_def <= target_def <= max_possible_def)

    # Crucially, ensure the flexible players aren't double-counted beyond their limit
    needed_att_from_flex = max(0, target_att - pure_att)
    needed_def_from_flex = max(0, target_def - pure_def)

    total_flex_needed = needed_att_from_flex + needed_def_from_flex

    return att_possible and def_possible and (total_flex_needed <= flexible)


def assign_positions_for_plot(team, target_formation):
    """
    Assigns players to specific ATT/DEF slots for plotting, prioritizing pure roles.
    Returns a dictionary: {'GK': [player], 'DEF': [players], 'ATT': [players]}
    """
    assignment = {'GK': [], 'DEF': [], 'ATT': []}
    field_players = sorted(
        [p for p in team if p['position'] != 'GK'],
        key=lambda x: x['strength'], reverse=True # Assign stronger players first potentially
    )
    gk = [p for p in team if p['position'] == 'GK']
    assignment['GK'] = gk

    target_att = target_formation.get('ATT', 0)
    target_def = target_formation.get('DEF', 0)

    assigned_names = set()

    # 1. Assign pure DEF
    pure_defs = [p for p in field_players if p['position'] == 'DEF']
    for p in pure_defs:
        if len(assignment['DEF']) < target_def:
            assignment['DEF'].append(p)
            assigned_names.add(p['name'])

    # 2. Assign pure ATT
    pure_atts = [p for p in field_players if p['position'] == 'ATT']
    for p in pure_atts:
        if len(assignment['ATT']) < target_att:
            assignment['ATT'].append(p)
            assigned_names.add(p['name'])

    # 3. Assign flexible players (ATT/DEF)
    flexible_players = [p for p in field_players if p['position'] == 'ATT/DEF']
    # Fill remaining DEF slots
    for p in flexible_players:
        if p['name'] not in assigned_names and len(assignment['DEF']) < target_def:
            assignment['DEF'].append(p)
            assigned_names.add(p['name'])
    # Fill remaining ATT slots
    for p in flexible_players:
         if p['name'] not in assigned_names and len(assignment['ATT']) < target_att:
            assignment['ATT'].append(p)
            assigned_names.add(p['name'])

    # Sanity check - if logic is correct and viable, counts should match
    if len(assignment['ATT']) != target_att or len(assignment['DEF']) != target_def:
         print(f"Warning: Could not assign exact formation for team: {format_team(team)}")
         # Fallback: just put remaining players somewhere if lists are short
         remaining = [p for p in field_players if p['name'] not in assigned_names]
         while len(assignment['DEF']) < target_def and remaining:
             assignment['DEF'].append(remaining.pop(0))
         while len(assignment['ATT']) < target_att and remaining:
             assignment['ATT'].append(remaining.pop(0))


    return assignment


def plot_formation(team_a_assigned, team_b_assigned, config):
    """Plots the two teams on a pitch representation."""
    fig, ax = plt.subplots(figsize=(7, 10))

    # Field dimensions (simple representation)
    pitch_length = 100
    pitch_width = 60
    ax.set_xlim(0, pitch_width)
    ax.set_ylim(0, pitch_length)
    ax.set_xticks([])
    ax.set_yticks([])

    # Pitch markings (basic)
    ax.plot([0, pitch_width], [pitch_length / 2, pitch_length / 2], color="grey", linestyle="--") # Halfway line
    center_circle = plt.Circle((pitch_width / 2, pitch_length / 2), radius=10, fill=False, color="grey")
    ax.add_patch(center_circle)
    # Simple Goal areas
    ax.add_patch(plt.Rectangle((pitch_width*0.3, 0), pitch_width*0.4, pitch_length*0.1, fill=False, color="grey"))
    ax.add_patch(plt.Rectangle((pitch_width*0.3, pitch_length*0.9), pitch_width*0.4, pitch_length*0.1, fill=False, color="grey"))


    # --- Define Formation Coordinates (approximate) ---
    # Team A (bottom half)
    coords_a = {
        'GK': [(pitch_width / 2, pitch_length * 0.05)],
        'DEF': [(pitch_width * 0.2, pitch_length * 0.25),
                (pitch_width / 2, pitch_length * 0.25),
                (pitch_width * 0.8, pitch_length * 0.25)],
        'ATT': [(pitch_width * 0.25, pitch_length * 0.4),
                (pitch_width / 2, pitch_length * 0.45),
                (pitch_width * 0.75, pitch_length * 0.4)]
    }
    # Team B (top half)
    coords_b = {
        'GK': [(pitch_width / 2, pitch_length * 0.95)],
        'DEF': [(pitch_width * 0.2, pitch_length * 0.75),
                (pitch_width / 2, pitch_length * 0.75),
                (pitch_width * 0.8, pitch_length * 0.75)],
        'ATT': [(pitch_width * 0.25, pitch_length * 0.6),
                (pitch_width / 2, pitch_length * 0.55),
                (pitch_width * 0.75, pitch_length * 0.6)]
    }

    # --- Plot Players ---
    teams_data = [
        {'assigned': team_a_assigned, 'coords': coords_a, 'color': 'blue', 'marker': 'o', 'name': 'Team A'},
        {'assigned': team_b_assigned, 'coords': coords_b, 'color': 'red', 'marker': 's', 'name': 'Team B'}
    ]

    for team_info in teams_data:
        assigned = team_info['assigned']
        coords = team_info['coords']
        color = team_info['color']
        marker = team_info['marker']
        name = team_info['name']
        plotted_count = {'GK': 0, 'DEF': 0, 'ATT': 0}

        for role in ['GK', 'DEF', 'ATT']:
            players_in_role = assigned.get(role, [])
            available_coords = coords.get(role, [])
            for i, player in enumerate(players_in_role):
                if i < len(available_coords):
                    x, y = available_coords[i]
                    ax.plot(x, y, marker=marker, color=color, markersize=35, label=f"{name}" if i==0 and role=='GK' else "") # Label once per team
                    ax.text(x, y, f"{player['name'].split()[0]}\n({player['strength']})",
                            ha='center', va='center', fontsize=8, color='white', fontweight='bold')
                    plotted_count[role] += 1
                else:
                    print(f"Warning: Not enough coordinates defined for role {role} in {name}")

    ax.legend()
    plt.title(f"Best Balanced Teams (Diff: {config['difference']})\n"
              f"Team A (Str: {config['strength_a']}) vs Team B (Str: {config['strength_b']})",
              fontsize=12)
    plt.show()


# --- Main Logic ---

# 1. Prepare Data
# Add is_goalkeeper flag based on position for consistency
for p in players_data:
    p['is_goalkeeper'] = (p['position'] == 'GK')

goalkeepers = [p for p in players_data if p['is_goalkeeper']]
field_players = [p for p in players_data if not p['is_goalkeeper']]
all_players_set = set(p['name'] for p in players_data)

if len(goalkeepers) != 2:
    print("Error: Exactly two goalkeepers are required.")
    exit()

total_players = len(players_data)
if total_players % 2 != 0:
    print("Error: Odd number of players. Cannot make two equal teams.")
    exit() # Or adjust logic for uneven teams if desired

team_size = total_players // 2
field_players_per_team = team_size - 1 # e.g., 7 total -> 6 field players

if sum(TARGET_FIELD_FORMATION.values()) != field_players_per_team:
     print(f"Warning: Target formation {TARGET_FIELD_FORMATION} requires "
           f"{sum(TARGET_FIELD_FORMATION.values())} field players, "
           f"but teams have {field_players_per_team} field players.")
     # Adjust target or proceed with caution
     # For 14 players -> 7 per team -> 6 field players. 3+3=6. OK.


# Assign goalkeepers (fixed assignment for calculation)
gk1 = goalkeepers[0]
gk2 = goalkeepers[1]

# 2. Generate Combinations and Evaluate
possible_team_configs = []

print(f"Generating combinations for {len(field_players)} field players, choosing {field_players_per_team}...")

for team_a_field_players_tuple in itertools.combinations(field_players, field_players_per_team):
    team_a_field_players = list(team_a_field_players_tuple)
    team_a_field_players_names = set(p['name'] for p in team_a_field_players)

    # Determine Team B's field players
    team_b_field_players = [p for p in field_players if p['name'] not in team_a_field_players_names]

    # Form the complete teams
    team_a = [gk1] + team_a_field_players
    team_b = [gk2] + team_b_field_players

    # Calculate strengths
    strength_a = get_team_strength(team_a)
    strength_b = get_team_strength(team_b)
    difference = abs(strength_a - strength_b)

    # Check positional viability
    viable_a = check_positional_viability(team_a, TARGET_FIELD_FORMATION)
    viable_b = check_positional_viability(team_b, TARGET_FIELD_FORMATION)

    # Store the result
    possible_team_configs.append({
        'team_a': list(team_a), # Store copies
        'team_b': list(team_b),
        'strength_a': strength_a,
        'strength_b': strength_b,
        'difference': difference,
        'positionally_viable': viable_a and viable_b # Store if *both* teams are viable
    })

print(f"Generated {len(possible_team_configs)} total combinations.")

# 3. Filter for Positional Viability and Sort
viable_configs = [config for config in possible_team_configs if config['positionally_viable']]
viable_configs.sort(key=lambda x: x['difference']) # Sort by strength difference

print(f"Found {len(viable_configs)} positionally viable combinations (for {TARGET_FIELD_FORMATION} field setup).")


# 4. Display the Top N Viable Simulations
print(f"\n--- Displaying the top {NUM_SIMULATIONS_TO_SHOW} most balanced & viable simulations ---")

# Avoid displaying the exact same pair of teams if strengths are identical
displayed_configs_set = set()
count_shown = 0

for i, config in enumerate(viable_configs):
    if count_shown >= NUM_SIMULATIONS_TO_SHOW:
        break

    # Create unique identifiers for the pair of teams (order doesn't matter)
    team_a_names = frozenset(p['name'] for p in config['team_a'])
    team_b_names = frozenset(p['name'] for p in config['team_b'])
    config_identifier = tuple(sorted((team_a_names, team_b_names)))

    if config_identifier not in displayed_configs_set:
        print(f"\n--- Simulation {count_shown + 1} (Rank {i+1} overall viable) ---")
        print(f"Strength Balance Difference: {config['difference']}")
        print(f"\nTeam A (Strength: {config['strength_a']}, Viable: Yes)")
        print(f"  {format_team(config['team_a'])}")
        print(f"\nTeam B (Strength: {config['strength_b']}, Viable: Yes)")
        print(f"  {format_team(config['team_b'])}")
        print("-" * 30)

        displayed_configs_set.add(config_identifier)
        count_shown += 1

if count_shown == 0:
    print("\nNo simulations found that satisfy both balance and positional viability criteria.")
elif count_shown < NUM_SIMULATIONS_TO_SHOW:
     print(f"\nNote: Only {count_shown} unique balanced and viable configurations found.")


# 5. Visualize the Best Simulation
if viable_configs:
    best_config = viable_configs[0]
    print("\n--- Visualizing the BEST balanced and viable teams ---")

    # Assign players to roles for plotting
    team_a_assigned = assign_positions_for_plot(best_config['team_a'], TARGET_FIELD_FORMATION)
    team_b_assigned = assign_positions_for_plot(best_config['team_b'], TARGET_FIELD_FORMATION)

    # Plot
    plot_formation(team_a_assigned, team_b_assigned, best_config)
else:
    print("\nCannot visualize - no viable team configurations were found.")