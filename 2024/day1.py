import itertools
# https://everybody.codes/event/2024/quests/1

# Maps mob types to number of potions required.
MOB_POTIONS = {"A": 0, "B": 1, "C": 3}

with open("day1.part1.txt", "rt") as fobj:
    buf = fobj.read().strip()
pots = sum(MOB_POTIONS[x] for x in buf)
print(f"Day 1 part 1 solution: {pots}")


# Part 2 adds a new mob type
MOB_POTIONS["D"] = 5
# Also pretend that the mob missing marker is a mob that
# costs zero potions to make some of the logic easier
MOB_POTIONS["x"] = 0
with open("day1.part2.txt", "rt") as fobj:
    buf = fobj.read().strip()
fights = itertools.batched(buf, 2)


def fight_cost(fight):
    cost = sum(MOB_POTIONS[x] for x in fight)
    num_enemies = sum(1 for x in fight if x != "x")
    pots_per_enemy = num_enemies - 1
    cost = cost + (pots_per_enemy * num_enemies)
    return cost


pots = sum(fight_cost(x) for x in fights)
print(f"Day 1 part 2 solution: {pots}")


# Part 3

with open("day1.part3.txt", "rt") as fobj:
    buf = fobj.read().strip()
fights = itertools.batched(buf, 3)
pots = sum(fight_cost(x) for x in fights)
print(f"Day 1 part 3 solution: {pots}")
