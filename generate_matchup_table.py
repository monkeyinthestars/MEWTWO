
from collections import Counter
from typing import Dict, List

from mlp.html_table import create_html_table

from archetype_parser import parse_decklist_into_archetype
from download_manager import get_soup_from_url

RK9_URL = "https://rk9.gg/pairings/ORL01mtNi5LV1IgmscGJ" # Orlando
RK9_URL = "https://rk9.gg/pairings/SAO01mt4psEefFM1ZHAx" # Sao Paulo
RK9_URL = "https://rk9.gg/pairings/NA01wsS5yrQoQIs3mDtB" # NAIC
RK9_URL = "https://rk9.gg/pairings/WCS01mIMYt8if4wVuaO0" # Worlds
RK9_URL_LIST = [
    # "https://rk9.gg/pairings/JO01md78IaKVf4h0TpoI", # Joinville
    # "https://rk9.gg/pairings/DO01me0AIjF9eliBRvM5", # Dortmund
    # "https://rk9.gg/pairings/LO01mZ7ppP5mQLSyxdbT", # Louisville
    # "https://rk9.gg/pairings/LI01majszra4hnrtxJST", # Lilles
    # "https://rk9.gg/pairings/LA01mwu6ugCwMEJxWT2H", # LAIC
    "https://rk9.gg/pairings/SG01meRA8mIYExcTihNU", # Stuttgart
]

def get_decklist_from_url(url: str):
    soup = get_soup_from_url(url)
    table = soup.findAll("table")[0]
    all_card_lines = table.findAll("li")

    decklist = {}
    for card in all_card_lines:
        card_name = card["data-cardname"]
        card_set = card["data-setnum"]
        quantity = int(card["data-quantity"])
        card_type = card["data-cardtype"]
        if card_type == "pokemon":
            card_name = card_name + " " + card_set
        if card_name in decklist.keys():
            decklist[card_name] += quantity
        else:
            decklist[card_name] = quantity
    decklist = list(decklist.items())
    number_of_card_in_deck = sum([quantity for card, quantity in decklist])
    if number_of_card_in_deck != 60:
        raise ValueError(f"The decklist doesn't count 60 cards! (Number of card found: {number_of_card_in_deck})")
    return decklist


def get_decklist_url_per_player(url: str) -> dict[str, str]:
    tournament_url_code = url.split("/")[-1]
    roster_url = f"https://rk9.gg/roster/{tournament_url_code}"
    soup = get_soup_from_url(roster_url)

    decklist_url_per_player = {}

    roster_table = soup.findAll("div", class_="card-body")[0].findAll("tbody")[0]
    table_row_list = roster_table.findAll("tr")
    for row in table_row_list:
        row_infos = row.findAll("td")
        first_name = row_infos[1].text.strip()
        last_name = row_infos[2].text.strip()
        country = row_infos[3].text.strip()
        division = row_infos[4].text.strip()
        decklist_slot = row_infos[5]
        decklist_status = decklist_slot.text.strip()
        if division != "Masters":
            continue
        if decklist_status == "View":
            decklist_url = "https://rk9.gg" + decklist_slot.findAll("a")[0]["href"]
            player_name_whole = f"{first_name} {last_name} [{country}]"
            decklist_url_per_player[player_name_whole] = decklist_url

    return decklist_url_per_player


# Returns a dict {"Player Name [COUNTRY]": {"decklist": [cards], "archetype": ["pokemon1", "pokemon2"]} }
def get_players_infos_from_tournament_url(url):
    player_database = {}
    decklist_url_per_player = get_decklist_url_per_player(url)

    for playername, decklist_url in decklist_url_per_player.items():
        decklist = get_decklist_from_url(decklist_url)
        archetype = parse_decklist_into_archetype(decklist)
        if archetype == ["unown"]:
            print(decklist_url)

        player_database[playername] = {"decklist": decklist, "archetype": archetype}
    return player_database


"""
Get the max number of round displayed so far
"""
def _max_round_from_soup(soup):
    round_number = 1
    while True:
        round_n_div = soup.find("div", {"id": f"P2R{round_number}"})
        if round_n_div == None:
            return round_number-1
        round_number += 1

def get_all_pairings_per_round(tournament_url):

    round_history = []
    max_number_of_rounds = 18
    for round_n in range(1, max_number_of_rounds+1):

        soup = get_soup_from_url(tournament_url+ "?pod=2&rnd=" + str(round_n))
        # round_n_div = soup.find("div", {"id": f"P2R{round_n}"})
        match_div_list = soup.findAll("div", class_="match")

        match_list_of_this_round = []
        print(f"Round number {round_n}, nb matchs = {len(match_div_list)}")
        for div_match in match_div_list:
            div_player1, div_table_number, div_player2 = div_match.findAll("div")
            if div_table_number.text == "Table #":
                continue
            player_name1 = div_player1.find("span").text
            if div_player2.text.strip() == "":
                player_name2 = ""
            else:
                player_name2 = div_player2.find("span").text
            if "winner" in div_player1["class"]:
                winner_tag = "P1"
            elif "tie" in div_player1["class"]:
                winner_tag = "TIE"
            elif "winner" in div_player2["class"]:
                winner_tag = "P2"
            else:
                raise KeyError("Winner not found while looking at the match div")
            match_list_of_this_round.append((player_name1, player_name2, winner_tag))
        round_history.append(match_list_of_this_round)
    return round_history


def get_matchup_table(url_list: List[str], from_round_n: int = 0) -> Dict[str, Dict[str, List]]:
    """Generate a matchup table from the RK9 tournament URL given

    Args:
        url_list (List[str]): List of RK9 URLs
        from_round_n (int, optional): The matchup table is going to be generated from the specified round onward.
        This way, you can accept only players from day2. Defaults to 0.

    Returns:
        Dict[Dict[List]]: The matchup table of all archetypes.
        You can use: wins, loses, ties = matchuptable[archetype1][archetype2]
    """
    archetype_list = []
    for url in url_list:
        players_infos = get_players_infos_from_tournament_url(url)

        for infos in players_infos.values():
            archetype = ", ".join(infos["archetype"])
            archetype_list.append(archetype)

    _archetype_counts = Counter(archetype_list)
    list_of_archetypes_appearing_only_once = [archetype for archetype, count in _archetype_counts.items() if count == 1]

    print(
        "The following archetypes are only played by one player, "
        "they are going to be labelled as 'unown': "
        f"{list_of_archetypes_appearing_only_once}"
    )
    archetype_list = list(set(archetype_list))
    archetype_list = [archetype for archetype in archetype_list if not archetype in list_of_archetypes_appearing_only_once]
    if list_of_archetypes_appearing_only_once != []:
        if not "unown" in archetype_list:
            archetype_list += ["unown"]
    print(f"List of archetypes processed: {archetype_list}")

    matchup_table = {}
    for archetype in archetype_list:
        archetype_matchup_scores = {}
        for opposing_archetype in archetype_list:
            archetype_matchup_scores[opposing_archetype] = [0, 0, 0]
        matchup_table[archetype] = archetype_matchup_scores

    for url in url_list:
        players_infos = get_players_infos_from_tournament_url(url)

        all_pairings_per_round = get_all_pairings_per_round(url)

        for round_n, match_list in enumerate(all_pairings_per_round):
            if round_n < from_round_n:
                for (player1_name, player2_name, winner) in match_list:
                    if player1_name in players_infos.keys() and player2_name in players_infos.keys():
                        archetype_p1 = ", ".join(players_infos[player1_name]["archetype"])
                        if archetype_p1 in list_of_archetypes_appearing_only_once:
                            archetype_p1 = "unown"
                        archetype_p2 = ", ".join(players_infos[player2_name]["archetype"])
                        if archetype_p2 in list_of_archetypes_appearing_only_once:
                            archetype_p2 = "unown"
                        if winner == "P1":
                            matchup_table[archetype_p1][archetype_p2][0] += 1
                            matchup_table[archetype_p2][archetype_p1][1] += 1
                        if winner == "P2":
                            matchup_table[archetype_p2][archetype_p1][0] += 1
                            matchup_table[archetype_p1][archetype_p2][1] += 1
                        if winner == "TIE":
                            matchup_table[archetype_p2][archetype_p1][2] += 1
                            matchup_table[archetype_p1][archetype_p2][2] += 1

    return matchup_table


def get_img_tags_for_archetype(archetype):
    result = ""
    for pokemon in archetype.split(", "):
        pokemon_png_url = f"https://limitlesstcg.s3.us-east-2.amazonaws.com/pokemon/gen9/{pokemon}.png"
        result += f"<img src={pokemon_png_url} style=\"35px;\">"
    return result

def parse_matchup_table_into_table_data(matchup_data):
    archetype_list = matchup_data.keys()
    matchup_ratio = {
        archetype_p1: {
            archetype_p2: -1
            for archetype_p2 in archetype_list
        }
        for archetype_p1 in archetype_list
    }

    for archetype_p1 in archetype_list:
        for archetype_p2 in archetype_list:
            win, lose, tie = matchup_data[archetype_p1][archetype_p2]
            if win + lose + tie != 0:
                matchup_ratio[archetype_p1][archetype_p2] = (win + (tie/3)) / (win + tie + lose)


    def format_text_for_heatmap(heat):
        if heat == -1:
            return ""
        return f"{100 * heat:.1f}".rstrip('0').rstrip('.') + "%"

    html_data = {}

    for archetype_p1 in archetype_list:
        p1_img_tags = get_img_tags_for_archetype(archetype_p1)
        html_data[p1_img_tags] = {}

        for archetype_p2 in archetype_list:
            p2_img_tags = get_img_tags_for_archetype(archetype_p2)
            heat_value = matchup_ratio[archetype_p1][archetype_p2]
            formatted_text = format_text_for_heatmap(heat_value)
            tooltip_text = (
                f"{p1_img_tags} VS {p2_img_tags}</br>"
                f"{formatted_text}</br>"
                f"{'-'.join([str(x) for x in matchup_data[archetype_p1][archetype_p2]])}"
            )

            html_data[p1_img_tags][p2_img_tags] = {
                "heat": heat_value,
                "text": formatted_text,
                "tooltip": tooltip_text,
            }


    return html_data

def remove_low_occurrences(matchup_table, nb_occurence_min=1):
    for archetype1, matchup_of_archetype1 in matchup_table.items():
        for archetype2 in matchup_of_archetype1.keys():
            number_of_match_played = sum(matchup_table[archetype1][archetype2])
            if number_of_match_played <= nb_occurence_min:
                matchup_table[archetype1][archetype2] = [0, 0, 0]
    return matchup_table

if __name__ == "__main__":
    print("Getting matchup table...")
    matchup_table = get_matchup_table(RK9_URL_LIST, from_round_n=8)
    print("Cleaning data...")
    matchup_table = remove_low_occurrences(matchup_table, nb_occurence_min=1)
    print("Parsing data...")
    table_data = parse_matchup_table_into_table_data(matchup_table)
    print(table_data)
    print("Creating html table...")
    create_html_table(table_data, "matchups.html")
