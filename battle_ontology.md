# Step 2 — Single-round battle ontology

This ontology defines what a valid battle round means in the zombie simulation. It covers the battle rules in `zombie_demo.py` and the survivor counts that the game calculates from each round.

## Concepts and relationships

| Concept | Properties and relationships |
| --- | --- |
| Battle round | Starts with exactly one human force and one zombie force and produces exactly one round result. |
| Force | Belongs to one side (`Human` or `Zombie`) and has a positive integer starting count. |
| Battle score | A real number used to decide the round outcome and adjust casualties. |
| Round result | Records one outcome (`Human win`, `Zombie win`, or `Draw`) and one set of counts for each side. |
| Casualty count | The number of units removed from a specific force during the round. |
| Survivor count | The number of units of the same force left after the round. |

## Rules

| ID | Rule |
| --- | --- |
| B1 | A round can begin only when both sides have at least one unit. A negative or fractional force count is outside the valid input domain. |
| B2 | The effective battle score determines the outcome. A positive score means humans win, a negative score means zombies win, and zero means a draw. Equal starting counts can still produce a win for either side. |
| B3 | The losing side takes at least one casualty. In a draw, each side takes at least one casualty. The winning side may take zero casualties. |
| B4 | If the winning side starts with at least ten times as many units as the losing side, the losing side loses its entire force. |
| B5 | Each side's casualty count is an integer from zero through that side's starting count, inclusive. Each side's survivor count equals its starting count minus its own casualties. |

## How the demo determines scores and casualties

Let `H` and `Z` be the starting human and zombie counts. The demo samples a score from a normal distribution with mean `advantage = ln((H + 1) / (Z + 1))` and standard deviation `max(0.3, 1.5 / (1 + 0.6 × abs(advantage)))`. When the advantage is at least `ln(10)`, the effective score is the greater of the sampled score and the advantage. When the advantage is at most `-ln(10)`, the effective score is the lesser of the two. Otherwise the sampled score is the effective score.

With effective score `s`, the initial human casualties are `round(H × (0.12 − 0.08 × tanh(s)))`. The initial zombie casualties are `round(Z × (0.12 + 0.08 × tanh(s)))`. The demo then applies the minimum-loss and wipeout rules in B3 and B4. The guaranteed outcome uses the smoothed ratio `(H + 1) / (Z + 1)`, while the wipeout rule uses the actual starting counts.

## Example rounds

For these examples, the sampled score is fixed so the outcome can be checked.

| Starting forces (human, zombie) | Sampled score | Outcome | Casualties (human, zombie) | Survivors (human, zombie) |
| --- | ---: | --- | --- | --- |
| (50, 60) | +1 | Human win | (3, 11) | (47, 49) |
| (50, 60) | −1 | Zombie win | (9, 4) | (41, 56) |
| (1, 1) | 0 | Draw | (1, 1) | (0, 0) |
| (20, 2) | +1 | Human win | (1, 2) | (19, 0) |
| (30, 2) | −1 | Human win | (1, 2) | (29, 0) |
| (0, 5) | — | No round begins | — | — |

## Prompt for documenting the ontology

> Using the one-round battle behavior in the zombie game demo, define the concepts, relationships, input conditions, and rules for round outcomes, casualties, and survivors. Give each rule an ID so a test can reference it later. Include concrete examples with fixed battle scores and show how the casualty and survivor counts follow from the rules.
