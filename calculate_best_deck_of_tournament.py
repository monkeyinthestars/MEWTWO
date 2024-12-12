from collections import Counter

from generate_matchup_table import get_matchup_table_from_tournament_url, get_players_infos_from_tournament_url


RK9_URL = "https://rk9.gg/pairings/NA01wsS5yrQoQIs3mDtB" # NAIC

WIN_POINTS  = 3
TIE_POINTS  = 1
LOSE_POINTS = 0
NO_MATCH_POINTS = 0


def get_archetype_counter(url):
    players_infos = get_players_infos_from_tournament_url(url)
    archetype_list = [", ".join(infos["archetype"]) for infos in players_infos.values()]
    return Counter(archetype_list)
    # return {'chien-pao': 10,
    # 'roaring-moon, koraidon': 5,
    # 'great-tusk': 2,
    # 'comfey, iron-hands': 20,
    # 'raging-bolt, ogerpon': 20,
    # 'gholdengo': 10,
    # 'dragapult, pidgeot': 10,
    # 'charizard, pidgeot': 10,
    # 'dialga-origin, metang': 5,
    # 'gardevoir, drifloon': 30,
    # 'dragapult, xatu': 5,
    # 'iron-thorns': 5,
    # 'iron-hands, iron-crown': 10,
    # 'snorlax': 7,
    # 'unown': 0,
    # 'lugia, cinccino': 30,
    # 'miraidon': 10,
    # 'dragapult, comfey': 10,
    # 'pidgeot, rotom': 7,
    # 'giratina-origin, comfey': 9}

def get_repartition_of_archetypes(url_list):
    archetype_repartition = {}
    archetype_counter = Counter()
    for url in url_list:
        archetype_counter_of_the_tournament = get_archetype_counter(url)
        archetype_counter += archetype_counter_of_the_tournament

    number_of_archetypes = sum(nb_occurence for nb_occurence in archetype_counter.values())
    archetype_repartition = {archetype: number_of_occurences/number_of_archetypes for archetype, number_of_occurences in archetype_counter.items()}
    return archetype_repartition


def main():
    
    print("Getting archetype repartition...")
    archetype_repartition = get_repartition_of_archetypes(RK9_URL_LIST)
    print("Getting matchup table...")
    matchup_table = get_matchup_table_from_tournament_url(RK9_URL)
    print(matchup_table)
    
    score_per_archetype = {}
    for archetype, matchup_data in matchup_table.items():
        archetype_score = 0
        for archetype_opponent, results in matchup_data.items():
            nb_wins, nb_ties, nb_loss = results
            number_of_matches = nb_wins + nb_ties + nb_loss
            if number_of_matches == 0:
                average_points = NO_MATCH_POINTS
            else:
                average_points = ((nb_wins*WIN_POINTS) + (nb_ties*TIE_POINTS) + (nb_loss*LOSE_POINTS)) / number_of_matches
            repartition_in_the_tournament = archetype_repartition[archetype_opponent]
            archetype_score += (repartition_in_the_tournament * average_points)
        score_per_archetype[archetype] = archetype_score
    
    archetype_counter = get_archetype_counter(RK9_URL)
    archetype_counter["comfey, iron-hands"] = 15
    
    score_per_archetype = list(score_per_archetype.items())
    score_per_archetype.sort(key=lambda x: x[1], reverse=True)
    
    print("archetype                 | score  | number in the tournament")
    for archetype, score in score_per_archetype:
        print(f"{archetype:25} |  {score:.2f}  | {archetype_counter[archetype]}")
    
    

if __name__ == "__main__":
    main()