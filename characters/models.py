from django.db import models

Rank = [
    ("G", "G"),
    ("F", "F"),
    ("D", "D"),
    ("C", "C"),
    ("B", "B"),
    ("A", "A"),
    ("S", "S"),
]


class character(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class playable(models.Model):
    character = models.ForeignKey(character, on_delete=models.CASCADE)
    variant = models.CharField(max_length=50)
    star = models.CharField(max_length=5)

    # Surface
    turf = models.CharField(max_length=1, choices=Rank, default="G")
    dirt = models.CharField(max_length=1, choices=Rank, default="G")

    # Distance
    short = models.CharField(max_length=1, choices=Rank, default="G")
    mile = models.CharField(max_length=1, choices=Rank, default="G")
    medium = models.CharField(max_length=1, choices=Rank, default="G")
    long = models.CharField(max_length=1, choices=Rank, default="G")

    # Strategy
    front = models.CharField(max_length=1, choices=Rank, default="G")
    pace = models.CharField(max_length=1, choices=Rank, default="G")
    late = models.CharField(max_length=1, choices=Rank, default="G")
    end = models.CharField(max_length=1, choices=Rank, default="G")

    def __str__(self):
        return f"{self.character}, {self.variant}"


class support(models.Model):
    character = models.ForeignKey(character, on_delete=models.CASCADE)
    rarity_choices = [("R", "R"), ("SR", "SR"), ("SSR", "SSR")]
    rarity = models.CharField(max_length=3, choices=rarity_choices, default="SSR")

    card_types = [
        ("Sp", "Speed"),
        ("St", "Stamina"),
        ("Pw", "Power"),
        ("Gt", "Gut"),
        ("Wt", "Wit"),
        ("P", "Pal"),
        ("Ps", "Pal-group"),
    ]

    type = models.CharField(max_length=2, choices=card_types, default="Ps")

    def __str__(self):
        return f"{self.character}, {self.rarity}"


class skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    # description = models.CharField(max_length=100)

    # strategy_choices = (
    #     ("F", "Front"),
    #     ("P", "Pace"),
    #     ("L", "Late"),
    #     ("E", "End"),
    #     ("A", "All"),
    # )

    # distance_choices = (
    #     ("S", "Short"),
    #     ("M", "Mile"),
    #     ("Me", "Medium"),
    #     ("L", "Long"),
    #     ("A", "All"),
    # )
    # aptitude_choices = (("T", "Turf"), ("D", "Dirt"), ("B", "Both"))

    # strategy = models.CharField(max_length=10, choices=strategy_choices, default="All")
    # distance = models.CharField(max_length=10, choices=distance_choices, default="All")
    # aptitude = models.CharField(max_length=10, choices=aptitude_choices, default="Both")


class skill_assignment(models.Model):
    skill_id = models.ForeignKey(skill, on_delete=models.CASCADE)
    owner_type = models.CharField(
        max_length=10,
        choices=(("playable", "playable"), ("support", "support")),
        default="playable",
    )

    playable_id = models.ForeignKey(
        playable, null=True, blank=True, on_delete=models.CASCADE
    )
    support_id = models.ForeignKey(
        support, null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.skill_id}, {self.owner_type}"
