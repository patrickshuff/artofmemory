#!/usr/bin/env python3

import os

import click

from artofmemory import cards, major, missing, pao


@click.group(help="Art of Memory")
def cli():
    pass


@cli.command("missing")
@click.option("--bible", help="Use books of Bible for quizzing", is_flag=True)
@click.option("--say/--no-say", help="Speak the choices out loud", default=False)
@click.option("--explain", help="Include explanation", is_flag=True, default=False)
@click.argument("choices", nargs=-1)
def missing_support(choices, explain: bool, say: bool, bible: bool):
    """Play guessing game of what is missing"""
    if explain:
        click.echo(missing.explain())

    if bible:
        missing.quiz_bible_books(talk=say)
    elif choices:
        missing.quiz_missing(list(choices), talk=say)
    else:
        click.secho("Pass a series of options for quizzing or preset options", fg="red")


@cli.command("card")
def print_random_card():
    """Show a random card"""
    cards.random_card()


@cli.command("pao")
@click.option("--quiz", help="Quiz how well you know your system", is_flag=True)
@click.option("--explain", help="Include explanation", is_flag=True, default=False)
@click.option(
    "--config-file",
    metavar="<FILE>",
    type=str,
    help="Alternate location of your PAO system",
    default="~/.artofmemory.conf",
)
def person_action_object(config_file, explain: bool, quiz: bool):
    """Test out your Person Action Object (PAO) knowledge"""
    if explain:
        click.echo(pao.explain())

    fname = os.path.expanduser(config_file)
    if not os.path.exists(fname):
        click.secho("Unable to read config file: {}".format(fname), fg="red")
        return

    if quiz:
        pao.basic_quiz(fname)


@cli.command("words")
@click.option("--quiz", help="Quiz how well you know things", is_flag=True)
@click.option("--explain", help="Include explanation", is_flag=True)
@click.option("--nouns", help="Filter words to be only nouns", is_flag=True)
@click.argument("numbers", nargs=-1)
def major_system_words(numbers, nouns: bool, explain: bool, quiz: bool):
    """Print out a possible words that match given number(s)"""
    if explain:
        click.echo(major.explain())

    if quiz:
        major.basic_quiz()
    elif numbers:
        major.print_number_words(numbers, nouns_only=nouns)


@cli.command()
@click.option("--org-mode", help="Make the output more org-mode friendly", is_flag=True)
@click.option("--nouns", help="Filter words to be only nouns", is_flag=True)
@click.option("--max", "max_", help="Maximum number", metavar="INT", default=100)
@click.option("--min", "min_", help="Minimum number", metavar="INT", default=0)
def words_summary(min_: int, max_: int, nouns: bool, org_mode: bool):
    """Show a large summary of words defaulting from 00 -> 99"""
    input_numbers = []
    # single digit numbers first
    for n in range(min_, max_):
        if -1 < n < 10:
            input_numbers.append(str(n))
    # then apply double digits
    for n in range(min_, max_):
        input_numbers.append(f"{n:02}")

    if org_mode:
        summary = major.OrgSummary(nouns_only=nouns)
    else:
        summary = major.Summary(nouns_only=nouns)
    with summary.printer_object() as printer:
        for number in input_numbers:
            printer(number)


if __name__ == "__main__":
    cli()
