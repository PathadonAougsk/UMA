from random import choice

from django.db import models
from django.db.models.fields.related import ForeignKey


class character(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class variant_connecter(models.Model):
    character = models.ForeignKey(character, on_delete=models.CASCADE)
    variant = models.ForeignKey(character, on_delete=models.CASCADE)


class variant(models.Model):
    STYLES_CHOICES = (
        ("play", "playable"),
        ("speed", "Speed"),
        ("power", "Power"),
        ("stamina", "Stamina"),
        ("wit", "Wit"),
        ("gut", "Gut"),
        ("pal", "Pal"),
    )
    RARITYS_CHOICES = (("R", "R"), ("SR", "SR"), ("SSR", "SSR"))

    name = models.CharField(max_length=100)
    rarity = models.CharField(max_length=3, choices=RARITYS_CHOICES, default="SSR")
    type = models.CharField(max_length=10, choices=STYLES_CHOICES, default="playable")

    def __str__(self):
        return ", ".join([str(self.rarity), str(self.name), str(self.type)])


class skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    strategy_choices = (
        ("F", "Front"),
        ("P", "Pace"),
        ("L", "Late"),
        ("E", "End"),
        ("A", "All"),
    )

    distance_choices = (
        ("S", "Short"),
        ("M", "Mile"),
        ("Me", "Medium"),
        ("L", "Long"),
        ("A", "All"),
    )
    aptitude_choices = (("T", "Turf"), ("D", "Dirt"), ("B", "Both"))

    strategy = models.CharField(max_length=10, choices=strategy_choices, default="All")
    distance = models.CharField(max_length=10, choices=distance_choices, default="All")
    aptitude = models.CharField(max_length=10, choices=aptitude_choices, default="Both")

    def __str__(self):
        return " : ".join(
            [
                str(self.name),
                str(self.description),
                str(self.strategy),
                str(self.distance),
                str(self.aptitude),
            ]
        )


class connecter(models.Model):
    skill = models.OneToOneField(skill, on_delete=models.CASCADE)
    variant = models.ForeignKey(variant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.variant.name} : {self.skill.name}"
