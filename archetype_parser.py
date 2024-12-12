
def is_in_decklist(cardname, decklist):
    return any((cardname in cardname_) for cardname_, quantity in decklist)
    
def is_in_decklist_with_quantity(cardname, quantity, decklist):
    return sum(quantity_ for cardname_, quantity_ in decklist if cardname in cardname_) >= quantity

def parse_decklist_into_archetype(decklist):
    def contains(*card_list):
        return all([is_in_decklist(card, decklist) for card in card_list])
        
    if contains("Charizard ex", "Pidgeot ex") and is_in_decklist_with_quantity("Charizard ex", 2, decklist):
        return ["charizard", "pidgeot"]
    if contains("Chien-Pao ex"):
        return ["chien-pao"]
    if contains("Snorlax PGO"):
        return ["snorlax"]
    if contains("Gardevoir ex", "Drifloon") or contains("Gardevoir ex", "Munkidori"):
        return ["gardevoir"]
    if contains("Lugia V"):
        return ["lugia"]
    if contains("Walking Wake") or contains("Great Tusk", "Flutter Mane") or contains("Koraidon"):
        return ["roaring-moon", "flutter-mane"]
    if contains("Roaring Moon ex", "Squawkabilly ex"):
        return ["roaring-moon"]
    if contains("Giratina", "Comfey"):
        return ["giratina-origin", "comfey"]
    if contains("Arceus", "Goodra"):
        return ["arceus", "goodra"]
    if contains("Arceus", "Giratina"):
        return ["arceus", "giratina-origin"]
    # if contains("Iron Hands ex", "Iron Leaves ex"):
    #     return ["iron-hands", "iron-leaves"]
    # if contains("Iron Hands ex", "Iron Crown ex"):
    #     return ["iron-hands", "iron-crown"]
    if contains("Origin Forme Dialga V", "Metang"):
        return ["dialga-origin", "metang"]
    if contains("Gholdengo ex"):
        return ["gholdengo"]
    if contains("Miraidon ex"):
        return ["miraidon"]
    if contains("Arceus", "Alolan Vulpix V"):
        return ["arceus", "vulpix-alola"]
    # if contains("Espathra ex", "Xatu"):
    #     return ["espathra", "xatu"]
    # if contains("Great Tusk"):
        # return ["great-tusk"]
    if contains("Regidrago V"):
        return ["regidrago"]
    if contains("Dragapult ex", "Pidgeot ex"):
        return ["dragapult", "pidgeot"]
    if contains("Dragapult ex", "Dusknoir"):
        return ["dragapult", "dusknoir"]
    # if contains("Dragapult ex", "Comfey"):
        # return ["dragapult", "comfey"]
    if contains("Raging Bolt ex", "Ogerpon"):
        return ["raging-bolt", "ogerpon"]
    if contains("Pidgeot ex", "Rotom V") and not contains("Charizard ex") and not contains("Dragapult ex"):
        return ["pidgeot", "rotom"]
    if contains("Comfey", "Iron Hands ex"):
        return ["comfey", "iron-hands"]
    if is_in_decklist_with_quantity("Iron Thorns ex", 4, decklist):
        return ["iron-thorns"]
    if contains("Terapagos ex"):
        return ["terapagos"]
    if contains("Origin Form Palkia V"):
        return ["palkia-origin"]
    if contains("Klawf", "Hisuan Electrode V"):
        return ["klawf", "electrode-hisui"]
    if contains("Noivern ex", "Cornerstone Mask Ogerpon ex"):
        return ["ogerpon-cornerstone", "noivern"]
    return ["unown"]
