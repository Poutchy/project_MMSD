import json

from libraries.importExcel import createTableLecturers, createTableProducts
from libraries.list_papers import PaperCollection
from libraries.list_persons import PersonCollection
from libraries.paper import Paper, threshold
from libraries.person import Person


def initialisation(ConfigsFile: str, AffFile: str, ProdFile: str):
    AffTable = createTableLecturers(AffFile, ConfigsFile)
    ProdTable = createTableProducts(ProdFile, ConfigsFile)

    list_persons: PersonCollection = PersonCollection()
    list_papers: PaperCollection = PaperCollection()
    nb_person = 0

    with open(ConfigsFile, "r") as cf:
        configs = json.load(cf)

    for _, row in AffTable.iterrows():
        new_guy: Person = Person(
            row["Identificativi - ID IRIS"],
            row["Nome"],
            row["Cognome"],
            row["Affiliazione - Matricola"],
        )
        if not new_guy in list_persons:
            nb_person += 1
            list_persons.add_person(new_guy)

    objectif = int(2.5 * nb_person)

    begin_year = configs["begin_year"]
    end_year = configs["end_year"]

    for _, row in ProdTable.iterrows():
        published_year = row["Anno di pubblicazione"]
        if published_year < begin_year or published_year > end_year:
            pass

        id_product = row["ID prodotto"]
        if id_product not in list_papers:

            val_array = [
                threshold(
                    row[
                        "scopus: Percentili  rivista - CITESCORE non pesata - miglior percentile"
                    ],
                    configs,
                ),
                threshold(
                    row[
                        "scopus: Percentili rivista - CITESCORE pesata - miglior percentile"
                    ],
                    configs,
                ),
                threshold(
                    row[
                        "scopus: Percentili rivista - SJR non pesata - miglior percentile"
                    ],
                    configs,
                ),
                threshold(
                    row["scopus: Percentili rivista - SJR pesata - miglior percentile"],
                    configs,
                ),
                threshold(
                    row[
                        "scopus: Percentili rivista - SNIP non pesata - miglior percentile"
                    ],
                    configs,
                ),
                threshold(
                    row[
                        "scopus: Percentili rivista - SNIP pesata - miglior percentile"
                    ],
                    configs,
                ),
                threshold(
                    row["wos: Percentili rivista - IF - miglior percentile"], configs
                ),
                threshold(
                    row["wos: Percentili rivista - 5 anni IF - miglior percentile"],
                    configs,
                ),
            ]

            paper_value = max(val_array)

            new_paper: Paper = Paper(row["ID prodotto"], row["Titolo"], paper_value)
            list_papers.add_paper(new_paper)
        paper = list_papers[row["ID prodotto"]]
        list_persons[row["autore: ID persona (IRIS)"]].add_writted_paper(paper)

    return list_persons, nb_person, list_papers, objectif


def first_proposition(list_persons: PersonCollection):
    nb_proposed_papers = 0
    restart = False
    while True:
        for person in list(reversed(list_persons.sorted_persons())):
            if person.nb_proposed_papers != 0:
                continue
            for paper in person.writted_papers:
                if paper.status == 0:
                    person.propose_paper(paper)
                    nb_proposed_papers += 1
                    restart = True
                    break
            if restart:
                restart = False
                break
        else:
            return list_persons, nb_proposed_papers
        list_persons.setup()


def gain_quota(
    list_persons: PersonCollection,
    list_papers: PaperCollection,
    objectif: int,
    nb_proposed_papers: int,
):
    for paper in list_papers.sorted_papers():
        if nb_proposed_papers == objectif:
            break
        if paper.is_presented():
            continue
        list_writter = [person for person in list_persons if person.has_written(paper)]

        for person in list_writter:
            if person.nb_proposed_papers < 4:
                person.propose_paper(paper)
                nb_proposed_papers += 1
                break
    return list_persons, list_papers, nb_proposed_papers


def to_json(list_persons: PersonCollection) -> str:
    professors: list[dict] = []
    for p in list_persons:
        professors.append(p.to_json())
    sum_values = 0
    for p in professors:
        sum_values += p["value"]
    return json.dumps({"value": sum_values, "professors": professors}, indent=2)


def exchange_1(list_persons: PersonCollection):
    for person in list_persons:
        if person.nb_proposed_papers == 0:
            for paper in person.writted_papers:
                if not paper.is_presented:
                    continue
                other_person: Person = list_persons[paper.presenter]
                if other_person.nb_proposed_papers > 1:
                    other_person.unpropose_paper(paper)
                    person.propose_paper(paper)
                    break
            else:
                continue


def exchange_2(list_papers: PaperCollection, list_persons: PersonCollection):
    change: bool
    while True:
        change = False
        for paper in list_papers:
            if not paper.is_presented():
                delta: float = 0  # no exchange will be made if delta = 0
                old_paper: Paper
                person_old_paper: Person
                l_authors = [
                    person for person in list_persons if person.has_written(paper)
                ]
                for person in l_authors:
                    for other_paper in person.proposed_papers:
                        n_delta = paper.value - other_paper.value
                        if n_delta > delta:
                            old_paper = other_paper
                            delta = n_delta
                            person_old_paper = person
                if delta > 0:
                    person_old_paper.unpropose_paper(old_paper)
                    person_old_paper.propose_paper(paper)
                    change = True
                    break
        if not change:
            break


def exchange_3(list_papers: PaperCollection, list_persons: PersonCollection):
    for person in list_persons:
        if person.nb_proposed_papers == 0 or person.nb_proposed_papers == 4:
            continue
        for paper in person.writted_papers:
            if paper.is_presented() or paper.value == 0.0:
                continue
            delta: float = 0
            other_person: Person
            old_paper: Paper
            for person2 in list_persons:
                if person2.nb_proposed_papers <= 1:
                    continue
                for other_paper in person2.proposed_papers:
                    n_delta = paper.value - other_paper.value
                    if n_delta > delta:
                        other_person = person2
                        old_paper = other_paper
                        delta = n_delta
            if delta > 0:
                other_person.unpropose_paper(old_paper)
                person.propose_paper(paper)
                break
