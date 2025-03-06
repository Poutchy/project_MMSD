class Paper:
    def __init__(
        self,
        id: int,
        name: str,
        value: float,
    ):
        self.id: int = id
        self.name: str = name
        self.value: int = value
        self.status: int = 0
        self.presenter: int = 0

        # scopus: Percentili pubblicazione - miglior percentile
        # wos: Percentili pubblicazione - miglior percentile

    def add_presenter(self, person):
        from libraries.person import Person

        if isinstance(person, Person):
            self.status = 1
            self.presenter = person.id

        if isinstance(person, int):
            self.status = 1
            self.presenter = person

    def is_presented(self) -> bool:
        return bool(self.status)

    def __eq__(self, other_paper: object, /) -> bool:
        if isinstance(other_paper, Paper):
            return self.id == other_paper.id
        if isinstance(other_paper, int):
            return self.id == other_paper
        return False

    def __le__(self, other_paper: object, /) -> bool:
        if isinstance(other_paper, Paper):
            return self.value <= other_paper.value
        return False

    def __lt__(self, other_paper: object, /) -> bool:
        if isinstance(other_paper, Paper):
            return self.value < other_paper.value
        return False

    def __str__(self):
        return self.name

    def to_json(self) -> dict:
        return {"ID prodotto": self.id, "Titolo": self.name, "value": self.value}

def threshold(value, configs): 
    quantile_thresholds = configs["quantile_thresholds"]
    quantile_values = configs["quantile_values"]

    for i in range(len(quantile_thresholds) - 1):
        if quantile_thresholds[i] <= value < quantile_thresholds[i + 1]:
            return quantile_values[i]  # Usa direttamente l'indice corretto

    return quantile_values[-1]

