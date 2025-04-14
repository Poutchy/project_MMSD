import json
from typing import List, Optional

from libraries.importExcel import createTableLecturers, createTableProducts
from libraries.list_papers import PaperCollection
from libraries.list_persons import PersonCollection
from libraries.paper import Paper, threshold
from libraries.person import Person


def initialisation(ConfigsFile: str, AffFile: str, ProdFile: str, selected_parameters: list[str]):
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

    authorized_types = [t.upper() for t in configs["product_type"]]

    for _, row in ProdTable.iterrows():
        published_year = row["Anno di pubblicazione"]
        paper_type = row["Tipologia (collezione)"]
        if (
            published_year < begin_year
            or published_year > end_year
            or not paper_type.startswith(tuple(authorized_types))
        ):
            continue

        id_product = row["ID prodotto"]
        if id_product not in list_papers:
            
            val_array = []
            for param in selected_parameters:
                val_array.append(
                    threshold(row[param], configs),
                )
            # if "selection" in parser.key():
            #     mask = parser["selection"]
            #     val_array = [
            #         val if (i not in mask and not isnan(val)) else 0
            #         for i, val in enumerate(configs["product_type"])
            #     ]:with expression as target:
            # else:
            #     val_array = [val for val in configs["product_type"] if not isnan(val)]

            # paper_value = max(val_array)
            # val_array = [
            #     threshold(
            #         row[
            #             "scopus: Percentili  rivista - CITESCORE non pesata - miglior percentile"
            #         ],
            #         configs,
            #     ),
            #     # threshold(
            #     #     row[
            #     #         "scopus: Percentili rivista - CITESCORE pesata - miglior percentile"
            #     #     ],
            #     #     configs,
            #     # ),
            #     # threshold(
            #     #     row[
            #     #         "scopus: Percentili rivista - SJR non pesata - miglior percentile"
            #     #     ],
            #     #     configs,
            #     # ),
            #     # threshold(
            #     #     row["scopus: Percentili rivista - SJR pesata - miglior percentile"],
            #     #     configs,
            #     # ),
            #     # threshold(
            #     #     row[
            #     #         "scopus: Percentili rivista - SNIP non pesata - miglior percentile"
            #     #     ],
            #     #     configs,
            #     # ),
            #     # threshold(
            #     #     row[
            #     #         "scopus: Percentili rivista - SNIP pesata - miglior percentile"
            #     #     ],
            #     #     configs,
            #     # ),
            #     threshold(
            #         row["wos: Percentili rivista - IF - miglior percentile"], configs
            #     ),
            #     # threshold(
            #     #     row["wos: Percentili rivista - 5 anni IF - miglior percentile"],
            #     #     configs,
            #     # ),
            # ]

            paper_value = max(val_array)

            new_paper: Paper = Paper(
                row["ID prodotto"],
                row["Titolo"],
                row["Tipologia (collezione)"],
                paper_value,
            )
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


def recompute_objectif(objectif: int, list_persons):
    remove = 0
    for person in list_persons:
        if not person.nb_proposed_papers:
            remove += 1
    return objectif - remove


def gain_quota(
    list_persons: PersonCollection,
    list_papers: PaperCollection,
    objectif: int,
    nb_proposed_papers: int,
):
    for paper in list(reversed(list_papers.sorted_papers())):
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


def to_json(list_persons: PersonCollection, nb_proposed_papers: int) -> str:
    professors: list[dict] = []
    for p in list_persons:
        professors.append(p.to_json())
    sum_values = 0
    for p in professors:
        sum_values += p["value"]
    return json.dumps(
        {
            "value": sum_values,
            "proposed_papers": nb_proposed_papers,
            "professors": professors,
        },
        indent=2,
    )


# def exchange_1(list_persons: PersonCollection):
#     for person in list_persons:
#         if person.nb_proposed_papers == 0:
#             for paper in person.writted_papers:
#                 if not paper.is_presented:
#                     continue
#                 other_person: Person = list_persons[paper.presenter]
#                 if other_person.nb_proposed_papers > 1:
#                     other_person.unpropose_paper(paper)
#                     person.propose_paper(paper)
#                     break
#             else:
#                 continue


def exchange_1(list_papers: PaperCollection, list_persons: PersonCollection):
    change: bool
    while True:
        change = False
        for paper in list_papers:
            if not paper.is_presented():
                delta: float = 0  # no exchange will be made if delta = 0
                old_paper: Optional[Paper] = None
                person_old_paper: Optional[Person] = None
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
                if old_paper is not None and person_old_paper is not None:
                    person_old_paper.unpropose_paper(old_paper)
                    person_old_paper.propose_paper(paper)
                    change = True
                    break
        if not change:
            break


def exchange_2(list_persons: PersonCollection):
    for person in list_persons:
        if person.nb_proposed_papers == 0 or person.nb_proposed_papers == 4:
            continue

        for paper in person.writted_papers:
            if paper.is_presented() or paper.value == 0.0:
                continue

            delta: float = 0
            other_person: Optional[Person] = None
            old_paper: Optional[Paper] = None
            for person2 in list_persons:
                if person2.nb_proposed_papers <= 1 or person2 is person:
                    continue
                for other_paper in person2.proposed_papers:
                    n_delta = paper.value - other_paper.value
                    if n_delta > delta:
                        other_person = person2
                        old_paper = other_paper
                        delta = n_delta
            if other_person is not None and old_paper is not None:
                other_person.unpropose_paper(old_paper)
                person.propose_paper(paper)
                break


def exchange_3(list_papers: PaperCollection, list_persons: PersonCollection):
    """ """
    for paper in list_papers:
        if not paper.is_presented():
            _ = try_alternate(list_papers, list_persons, paper)


def try_alternate(
    list_papers: PaperCollection,
    list_persons: PersonCollection,
    paper: Paper,
    first_writter: Optional[Person] = None,
    l: Optional[List[Paper]] = None,
) -> bool:
    if paper.id == "":
        print(paper)
    new_l: List[Paper] = [paper]
    if l is not None:
        new_l.extend(l.copy())
    list_writter: List[Person] = [
        person for person in list_persons if paper in person.writted_papers
    ]
    for writter in list_writter:
        for w_paper in writter.proposed_papers:
            if w_paper.value >= paper.value or w_paper in new_l:
                continue
            if try_alternate(list_papers, list_persons, w_paper, writter, new_l):
                if first_writter is not None:
                    first_writter.unpropose_paper(paper)
                writter.propose_paper(paper)
                return True
    delta: float = 0
    old_writter: Optional[Person] = None
    old_paper: Optional[Paper] = None
    for writter in list_writter:
        for other_paper in writter.proposed_papers:
            n_delta = paper.value - other_paper.value
            if n_delta > delta:
                old_writter = writter
                old_paper = other_paper
                delta = n_delta
    if old_paper is not None and old_writter is not None:
        old_writter.unpropose_paper(old_paper)
        if first_writter is not None:
            first_writter.unpropose_paper(paper)
        old_writter.propose_paper(paper)
        return True
    return False
