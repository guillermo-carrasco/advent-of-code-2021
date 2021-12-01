"""Advent of Code executor"""
import click

from solutions import (
    day_1,
)


@click.command()
@click.argument("day", type=click.STRING)
@click.argument("part", type=click.INT)
def run(day, part):
    solver = getattr(globals()[f"day_{day}"], f"Day{day}")(f"data/day_{day}.txt")
    print(getattr(solver, f"part_{part}")())


if __name__ == "__main__":
    run()