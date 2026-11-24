"""Play the Humans vs. Zombies prototype with Python 3."""

import math
import random


STARTING_HUMANS = 50
STARTING_ZOMBIES = 60
MAX_BATTLES = 100


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


def run_game():
    humans = STARTING_HUMANS
    zombies = STARTING_ZOMBIES
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
        humans -= human_losses
        zombies -= zombie_losses
        battle_number += 1
        print(
            f"Battle {battle_number}: {outcome}. "
            f"Lost {human_losses} humans and {zombie_losses} zombies. "
            f"Remaining: {humans} humans | {zombies} zombies."
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


if __name__ == "__main__":
    run_game()
