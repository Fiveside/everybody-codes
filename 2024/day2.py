from dataclasses import dataclass
from typing import Callable
import itertools


@dataclass
class ChallengeInput:
    runes: list[str]

    texts: list[str]

    @classmethod
    def parse(cls, iobuf):
        lines = list(filter(None, (x.strip() for x in iobuf.readlines())))
        runes_line = lines[0].removeprefix("WORDS:")
        text_lines = lines[1:]
        runes = runes_line.split(",")
        return cls(runes, text_lines)


with open("day2.part1.txt", "rt") as fobj:
    challenge = ChallengeInput.parse(fobj)
instances = 0
for rune in challenge.runes:
    for line in challenge.texts:
        instances = instances + line.count(rune)
print(f"Day 2 part 1 solution: {instances}")

# Part 2
with open("day2.part2.txt", "rt") as fobj:
    challenge = ChallengeInput.parse(fobj)
instances = 0
runes = set(challenge.runes) | {x[::-1] for x in challenge.runes}


def overlapping_substring_ranges(subst, haystack):
    start = 0
    while True:
        start = haystack.find(subst, start)
        if start == -1:
            break
        yield range(start, start + len(subst))
        start = start + 1


for line in challenge.texts:
    touched = set()
    for rune in runes:
        for rang in overlapping_substring_ranges(rune, line):
            for i in rang:
                touched.add(i)
    instances = instances + len(touched)

print(f"Day 2 part 2 solution: {instances}")


# Part 3
with open("day2.part3.txt", "rt") as fobj:
    challenge = ChallengeInput.parse(fobj)


# The challenge here is that we need to read each row and column of the input
# as a circular buffer.  We also need to read them backwards as a circular
# buffer, but then we only mark each square once.
@dataclass
class StringCoords:
    texts: list[str]
    positions: list[list[(int, int)]]

    def rows(self):
        for t, p in zip(self.texts, self.positions):
            yield (t, p)


coords = [
    [(x, y) for y, _ in enumerate(line)] for x, line in enumerate(challenge.texts)
]

# In the grid of words, we are to act as if the left is seemlessly connected to the
# right creating circular buffers for every row.  This is not true for columns though.
normal = StringCoords([x + x for x in challenge.texts], [x + x for x in coords])

rotated = StringCoords(
    list("".join(x)[::-1] for x in zip(*challenge.texts)),
    list(x[::-1] for x in zip(*coords)),
)

runes = set(challenge.runes) | {x[::-1] for x in challenge.runes}
marked = set()
for view in (normal, rotated):
    for haystack, pos in view.rows():
        # hs = haystack + haystack
        # poses = pos + pos
        for rune in runes:
            for rang in overlapping_substring_ranges(rune, haystack):
                for x in rang:
                    marked.add(pos[x])

print(f"Day 2 part 3 solution: {len(marked)}")
