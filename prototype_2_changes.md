# Zombie Game — Prototype 2

## Requested changes

| Change | Problem it addresses |
| --- | --- |
| Let the player set the starting human and zombie counts independently. | Fixed starting forces limited the demo to one setup. Custom counts make it possible to try equal forces, an outnumbered side, or a side that starts at zero. |
| Give the player four weapon choices for the humans. | The player previously had no way to give the humans an advantage at setup. |
| Give each weapon a higher chance of eliminating an extra zombie. | The choices need different gameplay effects. A single probability per weapon makes the difference easy to explain and test. |

## How it works

Pressing Enter at either count prompt uses 50. The game accepts whole counts from zero up to `sys.maxsize`, the platform's maximum index size. If either side starts at zero, the game reports the result immediately.

| Choice | Weapon | Chance of one extra zombie casualty per round |
| --- | --- | ---: |
| 1 | Training Baton | 20% |
| 2 | Spark Wand | 40% |
| 3 | Pulse Blaster | 60% |
| 4 | Arc Cannon | 80% |

The game first uses the [battle ontology](battle_ontology.md) to decide the round outcome and calculate base casualties. If any zombies survive that calculation, the selected weapon gets one chance to remove one more. For example, the Pulse Blaster adds one zombie casualty on a successful 60% roll. This bonus can occur in a win, loss, or draw. It reduces the zombies available in the next round and can affect who wins the simulation. The round's outcome label comes from the original battle score.

## Prompt description

The prompt asked me to extend the existing zombie simulation so the player can enter starting counts for both sides and choose one of up to four weapons for the humans. It asked for a simple system where stronger weapons increase the probability of killing zombies. It also asked for the code to be named Prototype 2 and for a document explaining the changes, the problems they address, and the prompt behind them.

## Run the prototype

Open a terminal in the folder containing `prototype_2.py` and run it with Python 3:

```bash
python3 prototype_2.py
```

After setup, press **Enter** for the next battle, **A** to finish automatically, or **Q** to quit.
