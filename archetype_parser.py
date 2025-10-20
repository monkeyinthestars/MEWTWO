"""
decklist_parser.py

This module provides utility functions for analyzing a decklist and determining archetypes
based on the cards it contains. It supports checking for the presence and quantity of cards
in a decklist, as well as parsing decklists into archetypes using predefined logic.

Functions:
    is_in_decklist(cardname: str, decklist: List[Tuple[str, int]]) -> bool:
        Checks if a card is present in the decklist.

    is_in_decklist_with_quantity(cardname: str, quantity: int, decklist: List[Tuple[str, int]]) -> bool:
        Checks if a card is present in the decklist with at least the specified quantity.

    contains(decklist: List[Tuple[str, int]], *card_list: str) -> bool:
        Checks if all specified cards are present in the decklist.

    parse_decklist_into_archetype(decklist: List[Tuple[str, int]]) -> List[str]:
        Parses a decklist to determine its archetype(s) based on included cards.

Example Usage:
    decklist = [
        ("Charizard ex", 2),
        ("Pidgeot ex", 1),
        ("Snorlax PGO", 3),
    ]
    archetypes = parse_decklist_into_archetype(decklist)
    print(archetypes)  # Output: ['charizard', 'pidgeot']

Dependencies:
    - Python 3.5+
    - typing module for type hints (List, Tuple)
"""

from typing import List, Tuple


def is_in_decklist(cardname: str, decklist: List[Tuple[str, int]]) -> bool:
    """
    Checks if a card is present in the decklist.

    Args:
        cardname (str): The name of the card to check.
        decklist (List[Tuple[str, int]]): A list of (cardname, quantity) tuples representing the decklist.

    Returns:
        bool: True if the card is present in the decklist, False otherwise.
    """
    return any((cardname in cardname_) for cardname_, quantity in decklist)

def is_in_decklist_with_quantity(cardname: str, quantity: int, decklist: List[Tuple[str, int]]) -> bool:
    """
    Checks if a card is present in the decklist with at least the specified quantity.

    Args:
        cardname (str): The name of the card to check.
        quantity (int): The minimum quantity of the card required.
        decklist (List[Tuple[str, int]]): A list of (cardname, quantity) tuples representing the decklist.

    Returns:
        bool: True if the card is present with at least the specified quantity, False otherwise.
    """
    return sum(quantity_ for cardname_, quantity_ in decklist if cardname in cardname_) >= quantity

def parse_decklist_into_archetype(decklist: List[Tuple[str, int]]) -> List[str]:
    """
    Parses a decklist to determine its archetype based on included cards.

    Args:
        decklist (List[Tuple[str, int]]): A list of (cardname, quantity) tuples representing the decklist.

    Returns:
        List[str]: A list of strings representing the archetype(s) inferred from the decklist.
    """
    def contains(*card_list: str) -> bool:
        """
        Checks if all specified cards are present in the decklist.

        Args:
            card_list (str): A list of card names to check.

        Returns:
            bool: True if all specified cards are in the decklist, False otherwise.
        """
        return all(is_in_decklist(card, decklist) for card in card_list)

    if contains("Charizard ex", "Pidgeot ex") and is_in_decklist_with_quantity("Charizard ex", 2, decklist):
        return ["charizard"]
    if contains("Chien-Pao ex"):
        return ["chien-pao"]
    if contains("Gardevoir ex", "Drifloon") or contains("Gardevoir ex", "Munkidori"):
        return ["gardevoir"]
    if contains("Roaring Moon ex", "Squawkabilly ex"):
        return ["roaring-moon", "squawkabilly"]
    if contains("Roaring Moon", "Dundunsparce"):
        return ["roaring-moon", "dundunsparce"]
    if contains("Wellspring Mask Ogerpon ex", "Noctowl"):
        return ["noctowl", "ogerpon-wellspring"]
    if is_in_decklist_with_quantity("Ceruledge ex", 3, decklist):
        return ["ceruledge"]
    if contains("Roaring Moon"):
        return ["roaring-moon"]
    if contains("Mega Absol ex", "Mega Kangaskhan ex"):
        return ["absol-mega", "kangaskhan-mega"]
    if contains("Gholdengo ex"):
        return ["gholdengo"]
    if contains("Miraidon ex", "Joltik"):
        return ["miraidon", "joltik"]
    if contains("Dragapult ex", "Pidgeot ex"):
        return ["dragapult", "pidgeot"]
    if contains("Dragapult ex", "Dusknoir"):
        return ["dragapult", "dusknoir"]
    if contains("Raging Bolt ex", "Noctowl"):
        return ["raging-bolt", "noctowl"]
    if is_in_decklist_with_quantity("Crustle", 3, decklist):
        return ["crustle"]
    if is_in_decklist_with_quantity("Iron Thorns ex", 4, decklist):
        return ["iron-thorns"]
    if contains("Noivern ex", "Cornerstone Mask Ogerpon ex"):
        return ["ogerpon-cornerstone", "noivern"]
    if contains("Marnie's Grimmsnarl", "Froslass"):
        return ["grimmsnarl", "froslass"]
    if contains("Flareon ex"):
        return ["flareon"]
    if contains("N's Zoroark", "Reshiram"):
        return ["zoroark"]
    if contains("Milotic ex", "Cornerstone Mask Ogerpon ex"):
        return ["milotic"]
    if contains("Pidgeot ex", "Elgyem", "Mist Energy"):
        return ["pidgeot"]
    return ["unown"]
