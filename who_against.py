

from generate_matchup_table import (
    get_all_pairings_per_round,
    get_players_decklist_infos_from_tournament_url,
)

RK9_TOURNAMENT_URL = "https://rk9.gg/pairings/LA01mwu6ugCwMEJxWT2H"



def main():
    player_database = get_players_decklist_infos_from_tournament_url(RK9_TOURNAMENT_URL)
    player_list = player_database.keys()
    pairing_list = get_all_pairings_per_round(RK9_TOURNAMENT_URL)
    match_history_per_player = dict.fromkeys(player_list, value={})
    for round_n, round_pairings in enumerate(pairing_list):
        print(round_pairings)
        exit()


if __name__ == "__main__":
    main()
