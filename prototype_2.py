"""Run the standalone Humans vs. Zombies Prototype 2."""

import math
import random
import sys


STARTING_HUMANS = 50
STARTING_ZOMBIES = 50
MAX_BATTLES = 100
DRAW_THRESHOLD = 0.15


# Each weapon's chance applies to one extra zombie casualty per round.
WEAPONS = {
    "1": ("Training Baton", 0.20),
    "2": ("Knife", 0.40),
    "3": ("Handgun", 0.60),
    "4": ("Automatic Rifle", 0.95),
}


def read_starting_count(side, default):
    while True:
        choice = input(f"Starting {side} [{default}]: ").strip()
        if not choice:
            return default
        try:
            count = int(choice)
        except ValueError:
            count = -1

        if 0 <= count <= sys.maxsize:
            return count
        print(f"Enter a whole number from 0 to {sys.maxsize:,}, or press Enter for {default}.")


def choose_weapon():
    print("\nChoose a weapon for the humans:")
    for choice, (name, chance) in WEAPONS.items():
        print(f"{choice}. {name} ({chance:.0%} chance of 1 extra zombie casualty)")

    while True:
        choice = input("Weapon [1–4]: ").strip()
        if choice in WEAPONS:
            return WEAPONS[choice]
        print("Choose a number from 1 to 4.")


def resolve_battle(humans, zombies):
    """Return the round outcome and each side's losses while both sides have units."""
    # As in the prototype, a larger force shifts the odds and reduces uncertainty.
    advantage = math.log((humans + 1) / (zombies + 1))
    uncertainty = max(0.3, 1.5 / (1 + 0.6 * abs(advantage)))
    result = random.gauss(advantage, uncertainty)

    overwhelming_advantage = math.log(10)
    if advantage >= overwhelming_advantage:
        result = max(result, advantage)
    elif advantage <= -overwhelming_advantage:
        result = min(result, advantage)

    # Treat close results as draws so normal random rolls can produce a tie.
    if abs(result) <= DRAW_THRESHOLD:
        result = 0.0

    # Each side normally loses about 12%. A more decisive win shifts losses
    # toward the losing side, and the loser always loses at least one unit.
    loss_adjustment = 0.08 * math.tanh(result)
    human_losses = round(humans * (0.12 - loss_adjustment))
    zombie_losses = round(zombies * (0.12 + loss_adjustment))

    if result > 0:
        if humans >= 10 * zombies:
            zombie_losses = zombies
        return "Humans win", human_losses, max(1, zombie_losses)
    if result < 0:
        if zombies >= 10 * humans:
            human_losses = humans
        return "Zombies win", max(1, human_losses), zombie_losses
    return "Draw", max(1, human_losses), max(1, zombie_losses)


def run_game(humans=STARTING_HUMANS, zombies=STARTING_ZOMBIES, weapon_chance=0.0):
    battle_number = 0
    automatic = False

    print("Humans vs. Zombies")
    print(f"Starting forces: {humans} humans | {zombies} zombies")

    while humans and zombies and battle_number < MAX_BATTLES:
        if not automatic:
            try:
                choice = input("Enter: next battle | A: finish automatically | Q: quit > ")
            except (EOFError, KeyboardInterrupt):
                print()
                choice = "q"

            choice = choice.strip().lower()
            if choice == "q":
                print("Game ended.")
                break
            if choice not in ("", "a"):
                print("Press Enter, A, or Q.")
                continue
            automatic = choice == "a"

        outcome, human_losses, zombie_losses = resolve_battle(humans, zombies)

        # A weapon can remove one zombie that survived the base battle.
        weapon_hit = (
            weapon_chance > 0
            and zombie_losses < zombies
            and random.random() < weapon_chance
        )
        if weapon_hit:
            zombie_losses += 1

        humans -= human_losses
        zombies -= zombie_losses
        battle_number += 1
        print(
            f"Battle {battle_number}: {outcome}. "
            f"Lost {human_losses} humans and {zombie_losses} zombies. "
            f"Remaining: {humans} humans | {zombies} zombies."
            + (" Weapon bonus: 1 extra zombie lost." if weapon_hit else "")
        )
    else:
        if humans and zombies:
            print("Battle limit reached.")
        if humans > zombies:
            print("Humans win the game!")
        elif zombies > humans:
            print("Zombies win the game!")
        else:
            print("The game ends in a draw!")

    print(f"Final forces: {humans} humans | {zombies} zombies")


def main():
    print("Humans vs. Zombies — Prototype 2")
    print("Press Enter at either starting-count prompt to use the number in brackets.")
    try:
        humans = read_starting_count("humans", STARTING_HUMANS)
        zombies = read_starting_count("zombies", STARTING_ZOMBIES)
        weapon_name, weapon_chance = choose_weapon()
    except (EOFError, KeyboardInterrupt):
        print("\nGame setup canceled.")
        return

    print(f"\nHuman weapon: {weapon_name} ({weapon_chance:.0%} bonus chance per round)\n")
    run_game(humans, zombies, weapon_chance)


if __name__ == "__main__":
    main()
