import re
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from characters.models import character


class Command(BaseCommand):
    help = "Insert / Create Data According to arg"

    def add_arguments(self, parser):
        parser.add_argument("Path-to-file")

    def handle(self, *args, **options):
        file = options["Path-to-file"]

        if "Character_card.txt" not in file.split("/"):
            raise CommandError("Require Path to contain Character_card.txt file")

        try:
            with open(file, "r") as file:
                new_character = True

                name = ""
                rarity = ""
                card_type = ""
                skills = []

                for sentence in file:
                    if "-------------------" in sentence:
                        new_character = True
                        continue

                    if new_character:
                        pattern = re.compile(r"(.+?)\s(\(SSR\)|\(SR\)|\(R\))\s(.+)")
                        match = pattern.match(sentence)
                        if match:
                            name, rarity, card_type = match.groups()

                        new_character = False

        except FileNotFoundError:
            raise CommandError(f"Path `{file}` is invalid try again")
