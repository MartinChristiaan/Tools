import click
from icecream import ic

ic("\x7f")
while True:
    char = "\x7f"
    char2 = click.getchar()
    ic(char == char2)
    ic(char)
