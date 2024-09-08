import time
import random


def choose_class():
    print("Welcome to Mooncradle! Mooncradle tells the story of two Children of the Moon...")
    time.sleep(4)
    print("Are you ready to embark on this journey?")
    time.sleep(1)

    while True:
        choice = input("Enter Yes or No: ").lower()
        time.sleep(0.5)

        if choice == "yes":
            print("Choose your character")
            print("\n1. Ashe: Born on the Winter Moon, Ashe shows curiosity and balance. Like all Moon Warriors, her innate magic allows her to create 'Live Mana' when attacking, which her party can use to boost their health. The Elder Mist sees great potential in her, believing she might one day be the one to create paths on water.")
            print("\n2. Sylas: Born on the Summer Mooon, Sylas is optimistic and bold. He wields a sunblade, through which he can absorb Eclipse Orbs whenever his attacks need an extra kick. As a blade-dancer, he walks the path of the Guardian God Solen.")
            break
        elif choice == "no":
            play_again = input("Would you like to give Mooncradle a chance again? Enter Yes or No: ").lower()
            if play_again == "yes":
                return choose_class()  # Use recursion here to start the game again
            else:
                print("Goodbye.")
                return None  # End the game if the player chooses not to play again
        else:
            print("Invalid choice. Please enter Yes or No")

    while True:
        choice = input("\nEnter the number corresponding to your character choice: ")
        time.sleep(1)

        if choice in ['1', '2']:
            ally = select_ally(choice)
            if ally:
                player = {'name': 'Ashe' if choice == '1' else 'Sylas', 'health': 20 if choice == '1' else 25,
                          'attack': 1 if choice == '1' else 3, 'defense': 2 if choice == '1' else 3,
                          'inventory': ['small_potion', 'medium_potion', 'large_potion'] + (
                              ['sunblade'] if choice == '2' else []) +
                                       (['defense_boost_ability'] if choice == '1' else []),
                          'max_health': 30 if choice == '1' else 35, 'ally': ally,
                          'defeated': False}
                player['defense'] = 3 if player['name'] == 'Ashe' else player['defense']
                player['attack'] = 2 if player['name'] == 'Sylas' else player['attack']
                return player
        else:
            print("Invalid choice. Please enter 1 for Ashe or 2 for Sylas.")


def select_ally(choice):
    if choice == '1':
        return {'name': 'Sylas', 'health': 25, 'attack': 6, 'defense': 1, 'defeated': False}
    elif choice == '2':
        return {'name': 'Ashe', 'health': 20, 'attack': 5, 'defense': 2, 'defeated': False}
    return None


def combat(player, monster):
    while True:
        monster_damage = roll_dice()
        player['health'] -= monster_damage
        print(f"\nThe {monster['name']} attacks you and deals {monster_damage} damage.")
        time.sleep(1)

        if player['health'] <= 0:
            print(f"\nYou have been killed by the {monster['name']}!")
            break

        player_damage = roll_dice() + player['attack']
        monster['health'] -= player_damage
        print(f"\nYou attack the {monster['name']} and deal {player_damage} damage.")
        time.sleep(1)

        if monster['health'] <= 0:
            print(f"\nYou have defeated the {monster['name']}!")
            break

def defend(player, monster, ally=None):
    player_defense = 1 + player['defense']
    monster_attack = roll_dice() + monster['attack']

    # Apply player defense to reduce damage taken
    damage_reduction = min(player_defense, monster_attack)
    monster_attack -= damage_reduction

    # Apply ally defense if ally is present
    ally_defense = 0
    if ally is not None:
        ally_defense = roll_dice() + ally['defense']
        damage_reduction = min(ally_defense, monster_attack)
        monster_attack -= damage_reduction

    # Update player's defense value with the defense boost from items
    player_defense += min(1, monster_attack)  # Increase defense by 1
    player_defense += ally_defense  # Add ally's defense

    return player_defense, ally_defense



def display_stats(player, monster, ally=None):
    time.sleep(1)
    print(f"\nPlayer: {player['name']} - Health: {player['health']}, attack: {player['attack']}, Defense: {player['defense']}")
    print(f"Monster: {monster['name']} - Health: {monster['health']}, attack: {monster['attack']}, Defense: {monster['defense']}")
    if ally is not None:
        print(f"Ally: {ally['name']} - Health: {ally['health']}, attack: {ally['attack']}, Defense: {ally['defense']}")



def display_inventory(player):
    time.sleep(1)
    print("\nInventory:")
    for i, item in enumerate(player['inventory'], start=1):
        print(f"{i}. {item.capitalize()}")


def game_over(player, monster=None):
    time.sleep(2)
    if monster is not None:
        print(f"\nGame Over. You were defeated by the {monster['name']}!")
    else:
        print("\nThanks for playing!")



def roll_dice():
    return random.randint(1, 6)  # Assuming a six-sided die for simplicity


def moonshimmer_fight(player):
    print("\nSuddenly, a mystical creature, the Moonshimmer Sprite, appears!")

    moonshimmer = {
        'name': 'Moonshimmer Sprite',
        'health': 15,
        'attack': 4,
        'defense': 2
    }

    print(f"The {moonshimmer['name']} attacks you and deals 2 damage.")

    # Initialize player_defense outside the loop
    player_defense = 0

    while moonshimmer['health'] > 0 and player['health'] > 0:
        display_stats(player, moonshimmer)

        action = input("\nChoose an action: attack, defend, or use an item: ").lower()

        if action == 'attack':
            player_damage = roll_dice() + player['attack']
            moonshimmer['health'] -= player_damage
            print(f"\nYou attack the {moonshimmer['name']} and deal {player_damage} damage.")
            time.sleep(2)
        elif action == 'defend':
            player_defense, _ = defend(player, moonshimmer)
            player['defense'] = player_defense
            print(f"\nYou raise your defense and increase it to {player_defense}.")
            time.sleep(2)
        elif action == 'use an item':

            display_inventory(player)

            item_number = input("\nChoose the number corresponding to the item in your inventory: ")

            if not item_number.isdigit():
                print("Invalid input. Please enter a valid number.")
                continue

            item_number = int(item_number)

            if item_number < 1 or item_number > len(player['inventory']):
                print("Invalid item number. Please enter a valid number.")
                continue

            item = player['inventory'][item_number - 1]

            if 'potion' in item and player['name'] == 'Ashe':
                restore_amount = {'small_potion': 5, 'medium_potion': 8, 'large_potion': 12}[item]
                player['health'] += restore_amount
                print(f"\n{player['name']} uses a healing potion and restores {restore_amount} health.")
            elif 'potion' in item and player['name'] == 'Sylas':
                boost_amount = {'small_potion': 2, 'medium_potion': 3, 'large_potion': 5}[item]
                player['attack'] += boost_amount
                print(f"\n{player['name']} uses an attack potion and boosts attacks by {boost_amount}.")
            elif 'defense_boost_ability' in item:
                # Add special ability logic for Ashe (increase defense by a lot)
                if player['name'] == 'Ashe':
                    player['defense'] += 6  # Adjust the value as needed
                    print(f"\nAshe activates her special ability, increasing defense by 6!")
            elif 'sunblade' in item:
                # Add special ability logic for Sylas (increase attack by a lot)
                if player['name'] == 'Sylas':
                    player['attack'] += 10  # Adjust the value as needed
                    player_damage = roll_dice() + player['attack']
                    moonshimmer['health'] -= player_damage
                    print(f"\nYou wield the sunblade at {moonshimmer['name']} and deal {player_damage} damage.")

            else:
                print("\nInvalid item. Please choose a valid item for your character.")
                continue

            print(f"{player['name']} uses {item}.")
            player['inventory'].remove(item)
        else:
            print("\nInvalid option. Please choose a valid action for your character.")
            continue
        if moonshimmer['health'] > 0:
            moonshimmer_damage = roll_dice() + moonshimmer['attack']
            # Apply player defense to reduce damage taken
            damage_reduction = min(player_defense, moonshimmer_damage)
            moonshimmer_damage -= damage_reduction
            player['health'] -= moonshimmer_damage
            print(f"\nMoonshimmer attacks you and deals {moonshimmer_damage} damage.")

        if player['health'] <= 0:
            print(f"\nYou have been killed by the {moonshimmer['name']}!")
            game_over(player, moonshimmer)
            return False  # Indicate that the player was defeated
    additional_fight(player, moonshimmer)



def additional_fight(player, current_monster):
    print(f"\nAfter defeating the {current_monster['name']}, you decide to explore further.")
    time.sleep(2)

    new_monster = {
        'name': f"Goblin {current_monster['name'][-1]}",
        'health': 20 + current_monster['health'],
        'attack': 5 + current_monster['attack'],
        'defense': 3 + current_monster['defense'],
        'ally': player['ally']  # Set the ally for the new monster
    }

    print(f"A wild {new_monster['name']} appears!")
    player_defense = 0
    while new_monster['health'] > 0 and player['health'] > 0:
        display_stats(player, new_monster)

        action = input("\nChoose an action: attack, defend, or use an item: ").lower()

        if action == 'attack':
            player_damage = roll_dice() + player['attack']
            if 'sunblade' in player['inventory']:
                player_damage += 2  # Bonus damage for using Sunblade
            new_monster['health'] -= player_damage
            print(f"\nYou attack the {new_monster['name']} and deal {player_damage} damage.")
            time.sleep(2)
        elif action == 'defend':
            player_defense, _ = defend(player, new_monster)
            player['defense'] = player_defense
            print(f"\nYou raise your defense and increase it to {player_defense}.")
            time.sleep(2)

        elif action == 'use an item':
            display_inventory(player)

            item_number = input("\nChoose the number corresponding to the item in your inventory: ")

            if not item_number.isdigit():
                print("Invalid input. Please enter a valid number.")
                continue

            item_number = int(item_number)

            if item_number < 1 or item_number > len(player['inventory']):
                print("Invalid item number. Please enter a valid number.")
                continue

            item = player['inventory'][item_number - 1]

            if 'potion' in item and player['name'] == 'Ashe':
                restore_amount = {'small_potion': 5, 'medium_potion': 8, 'large_potion': 12}[item]
                player['health'] += restore_amount
                print(f"\n{player['name']} uses a healing potion and restores {restore_amount} health.")
            elif 'potion' in item and player['name'] == 'Sylas':
                boost_amount = {'small_potion': 3, 'medium_potion': 4, 'large_potion': 5}[item]
                player['attack'] += boost_amount
                print(f"\n{player['name']} uses an attack potion and boosts attacks by {boost_amount}.")
            elif 'defense_boost_ability' in item:
                # Add special ability logic for Ashe (increase defense by a lot)
                if player['name'] == 'Ashe':
                    player['defense'] += 5  # Adjust the value as needed
                    print(f"\nAshe activates her special ability, increasing defense by 5!")
            elif 'sunblade' in item:
                # Add special ability logic for Sylas (increase attack by a lot)
                if player['name'] == 'Sylas':
                    player['attack'] += 10  # Adjust the value as needed
                    player_damage = roll_dice() + player['attack']
                    new_monster['health'] -= player_damage
                    print(f"\nYou wield the sunblade at {new_monster['name']} and deal {player_damage} damage.")
            else:
                print("\nInvalid item. Please choose a valid item for your character.")
                continue

            print(f"{player['name']} uses {item}.")
            player['inventory'].remove(item)

        else:
            print("\nInvalid option. Please choose a valid action for your character.")
            continue
        if new_monster['health'] > 0:
            monster_damage = roll_dice()
            # Apply player defense to reduce damage taken
            damage_reduction = min(player_defense, monster_damage)
            monster_damage -= damage_reduction
            player['health'] -= monster_damage
            print(f"\nThe {new_monster['name']} attacks you and deals {monster_damage} damage.")
            time.sleep(1)

        if player['health'] <= 0:
            print(f"\nYou have been killed by the {new_monster['name']}!")
            game_over(player, new_monster)
            return False  # Indicate that the player was defeated

    print(f"\nCongratulations! You have successfully defeated the {new_monster['name']}!")
    time.sleep(2)

    # Boost player's attack and health for the boss fight
    player['attack'] += 3
    player['max_health'] += 10
    player['health'] = player['max_health']

    next_fight = input(
        "\nYou feel a powerful presence ahead! Do you want to face the final boss? Enter Yes or No: (Entering No will exit the game) ").lower()

    if next_fight == 'yes':
        # After defeating the goblin, call the boss fight
        boss = {
            'name': 'Fleshmancer',
            'health': 60,
            'attack': 8,
            'defense': 5
        }
        boss_fight(player, player['ally'], boss)
    else:
        return False  # End the game if the player chooses not to face another challenge



def boss_fight(player, ally, boss):
    print("\nA formidable foe, the Fleshmancer, stands before you!")

    # Story before the final boss fight
    print(
        "\nAs you stand before the menacing figure of the Fleshmancer, memories of your journey flash before your eyes.")
    time.sleep(3)
    print(
        "You recall the humble beginnings in Mooncradle, the encounters with mystical creatures, and the trials in the Elder Mist's trails.")
    time.sleep(3)
    print("The journey has tested your strength, forged alliances, and uncovered the secrets of Eclipse Magic.")
    time.sleep(3)
    print(
        f"Now, the fate of Mooncradle and the Children of Moon rests on your shoulders as you prepare to confront the ultimate evil.")
    time.sleep(3)
    print(
        "The air thickens with tension as the Fleshmancer, a master of dark arts, raises its twisted form before you.")
    time.sleep(3)
    print("The final battle for Mooncradle begins!")

    # Initialize total defenses before the loop
    total_player_defense = 0
    total_ally_defense = 0

    while True:
        display_stats(player, boss, ally)

        # Check if player is defeated
        if player['health'] <= 0:
            print(f"\n{player['name']} has been defeated!")
            player['defeated'] = True
            total_player_defense = 0  # Reset total defense

        # Check if ally is defeated
        if ally is not None and ally['health'] <= 0:
            print(f"\n{ally['name']} has been defeated!")
            ally['defeated'] = True
            total_ally_defense = 0  # Reset total defense

        # Skip turn if a character is defeated
        if not player['defeated']:
            action = input("\nChoose an action: attack, defend, or use an item: ").lower()
            if action == 'attack':
                player_damage = roll_dice() + player['attack']
                ally_damage = roll_dice() + ally['attack']
                boss['health'] -= player_damage + ally_damage
                print(
                    f"\nYou and {ally['name']} attack the {boss['name']} and deal {player_damage + ally_damage} damage.")
                time.sleep(2)
            elif action == 'defend':
                player_defense, _ = defend(player, boss)
                player['defense'] = player_defense
                ally['defense'] = total_ally_defense
                print(f"\nTotal defense for {player['name']}: {total_player_defense}")
                print(f"Total defense for {ally['name']}: {total_ally_defense}")
                time.sleep(2)
            elif action == 'use an item':
                display_inventory(player)

                item_number = input("\nChoose the number corresponding to the item in your inventory: ")

                if not item_number.isdigit():
                    print("Invalid input. Please enter a valid number.")
                    continue

                item_number = int(item_number)

                if item_number < 1 or item_number > len(player['inventory']):
                    print("Invalid item number. Please enter a valid number.")
                    continue

                item = player['inventory'][item_number - 1]

                if 'potion' in item and player['name'] == 'Ashe':
                    restore_amount = {'small_potion': 5, 'medium_potion': 8, 'large_potion': 12}[item]
                    player['health'] = min(player['health'] + restore_amount, player['max_health'])
                    print(f"\n{player['name']} uses a healing potion and restores {restore_amount} health.")
                elif 'potion' in item and player['name'] == 'Sylas':
                    boost_amount = {'small_potion': 3, 'medium_potion': 4, 'large_potion': 5}[item]
                    player['attack'] += boost_amount
                    print(f"\n{player['name']} uses an attack potion and boosts attacks by {boost_amount}.")
                elif 'defense_boost_ability' in item:
                    # Add special ability logic for Ashe (increase defense by a lot)
                    if player['name'] == 'Ashe':
                        player['defense'] += 5  # Adjust the value as needed
                        print(f"\nAshe activates her special ability, increasing defense by 5!")
                elif 'sunblade' in item:
                    # Add special ability logic for Sylas (increase attack by a lot)
                    if player['name'] == 'Sylas':
                        player['attack'] += 10  # Adjust the value as needed
                        player_damage = roll_dice() + player['attack']
                        boss['health'] -= player_damage
                        print(
                            f"\nYou wield the sunblade at {boss['name']} and deal {player_damage} damage.")
                else:
                    print("\nInvalid item. Please choose a valid item for your character.")
                    continue
        # Check if both characters are defeated
        if player['defeated'] and (ally is None or ally['defeated']):
            print(f"\nYou and {ally['name']} have both been defeated by the {boss['name']}." 
                  f" Game Over.")
            game_over(player, boss)
            return

        # Check if boss is defeated
        if boss['health'] <= 0:
            print(f"\nCongratulations! You and {ally['name']} have defeated the {boss['name']}!")
            break

        # Boss attacks
        if not player['defeated'] and (ally is None or not ally['defeated']):
            boss_damage = roll_dice() + boss['attack']
            total_damage = max(0, boss_damage - total_player_defense - total_ally_defense)
            player['health'] -= total_damage
            if ally is not None:
                ally['health'] -= total_damage

            print(f"\nThe {boss['name']} attacks! "
                  f"You and {ally['name']} take {total_damage} damage.")
            time.sleep(2)

            if player['health'] <= 0 and (ally is None or ally['health'] <= 0):
                print(f"\nYou and {ally['name']} have been defeated by the {boss['name']}. Game Over.")
                game_over(player, boss)
                return

    print("\nCongratulations! You have defeated the Fleshmancer and saved Mooncradle!")
    time.sleep(2)


def main():
    player_character = choose_class()

    if player_character is None:
        print("Thanks for considering Mooncradle.")
        return  # Exit the game as no character was chosen

    player_character['max_health'] = player_character['health']  # Store max health for healing

    print("\nYou have chosen the character:", player_character['name'])
    time.sleep(0.5)

    print("Let the adventure begin!")
    time.sleep(2)

    print("You find yourself in Mooncradle, hometown of the Children of Moon...")
    time.sleep(3)
    print("You see Headmaster C and decide to approach him")
    time.sleep(1.5)
    print("....footsteps....")
    time.sleep(5)
    print("Headmaster: Hello Children of Moon. I see you fools have taken upon yourself to defeat the Fleshmancer.")
    time.sleep(2)
    print("......")
    time.sleep(2)
    print("You brats must have gone nuts!!!!")
    time.sleep(3)
    print("But... Maybe I could try trusting you for once. I have grown old after all.")
    time.sleep(3)
    print("......")
    time.sleep(3)
    print(
        "BUT YOU ARE NO WAY NEAR STRONG ENOUGH TO CHALLENGE THE FLESHMANCER. Head towards the eldermists trails and train. Don't show your face here again until you have mastered eclipse magic. NOW GO!")
    time.sleep(4)
    print("You start heading towards the eldermists trail")
    time.sleep(4)
    print("....How am I supposed to train here? There's nothing here....")
    time.sleep(3)

    # Call the moonshimmer_fight function when the player encounters the Moonshimmer Sprite
    moonshimmer_fight(player_character)


if __name__ == "__main__":
    main()