import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from characters.models import character, playable, skill, skill_assignment, support


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("Directoly Path")

    def handle(self, *args, **options):
        path_file = Path(options["Directoly Path"])
        if not path_file.exists() or path_file.suffix != ".json":
            raise CommandError(f"{path_file} is invalid")

        with open(path_file, "r") as file:
            characters = json.load(file)
            character_names = list(characters.keys())

            for name in character_names:
                if not character.objects.filter(name=name).exists():
                    character.objects.create(name=name)

                playable, support = (
                    characters[name]["Playable"],
                    characters[name]["Support"],
                )
                if playable:
                    for playable_variant in playable:
                        Command.scrape_playable(name, playable_variant)

                if support:
                    for support_variant in support:
                        Command.scrape_support(name, support_variant)

    @classmethod
    def scrape_playable(cls, name: str, variant: dict):
        variant_key = list(variant.keys())[0]

        current_variant = variant[variant_key]
        if playable.objects.filter(variant=current_variant).exists():
            return

        variant_star = current_variant["star"]

        variant_aptitude = current_variant["aptitude"]
        turf, dirt = (
            variant_aptitude["Surface"][0]["Turf"],
            variant_aptitude["Surface"][1]["Dirt"],
        )

        short, mile, medium, long = (
            variant_aptitude["Distance"][0]["Short"],
            variant_aptitude["Distance"][1]["Mile"],
            variant_aptitude["Distance"][2]["Medium"],
            variant_aptitude["Distance"][3]["Long"],
        )

        front, pace, late, end = (
            variant_aptitude["Strategy"][0]["Front"],
            variant_aptitude["Strategy"][1]["Pace"],
            variant_aptitude["Strategy"][2]["Late"],
            variant_aptitude["Strategy"][3]["End"],
        )

        variant_skills = current_variant["skills"]
        unique_skill = variant_skills["Unique skill"]
        normal_skills = [skill for skill in variant_skills["Normal skills"]] + [
            unique_skill
        ]

        uma = playable(
            character=character.objects.get(name=name),
            variant=variant_key,
            star=variant_star,
            turf=turf,
            dirt=dirt,
            short=short,
            mile=mile,
            medium=medium,
            long=long,
            front=front,
            pace=pace,
            late=late,
            end=end,
        )

        uma.save()

        for skill_name in normal_skills:
            query = skill.objects.filter(name=skill_name)
            if not query.exists():
                skill.objects.create(name=skill_name)

            skill_object = skill.objects.get(name=skill_name)
            skill_assignment.objects.create(
                skill_id=skill_object, owner_type="playable", playable_id=uma
            )

    @classmethod
    def scrape_support(cls, name: str, variant: dict):
        variant_key = list(variant.keys())[0]

        current_variant = variant[variant_key]

        variant_rarity = current_variant["rarity"]

        if support.objects.filter(
            character=character.objects.get(name=name), rarity=variant_rarity
        ).exists():
            return

        variant_type = current_variant["type"]

        variant_skills = current_variant["skills"]
        normal_skills = [skill for skill in variant_skills["Normal skills"]]

        uma = support(
            character=character.objects.get(name=name),
            rarity=variant_rarity,
            type=variant_type,
        )
        uma.save()

        for skill_name in normal_skills:
            query = skill.objects.filter(name=skill_name)
            if not query.exists():
                skill.objects.create(name=skill_name)

            skill_object = skill.objects.get(name=skill_name)
            skill_assignment.objects.create(
                skill_id=skill_object,
                owner_type="support",
                support_id=uma,
            )
