from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from characters.models import character


class Command(BaseCommand):
    help = "Insert / Create Data According to arg"

    def add_arguments(self, parser):
        parser.add_argument("Path-to-file")

    def handle(self, *args, **options):
        file = options["Path-to-file"]

        if "Character_name.txt" not in file.split("/"):
            raise CommandError("Require Path to contain Character_name.txt file")

        try:
            with open(file, "r") as file:
                for sentence in file:
                    character.objects.create(name=sentence.strip())

        except FileNotFoundError:
            raise CommandError(f"Path `{file}` is invalid try again")
