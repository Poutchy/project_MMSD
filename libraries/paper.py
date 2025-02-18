class Paper:
    def __init__(self, id: int, name: str, value: float,):
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


def threshold(value, configs): 
    for i in range(len(configs["quantile_thresholds"]) - 1):
        if configs["quantile_thresholds"][i] <= value < configs["quantile_thresholds"][i + 1]:
            return configs["quantile_values"][len(configs["quantile_values"]) -2 - i]
    
    return configs["quantile_values"][-1]
