from typing import List

import pytest

from libraries.functions_algo import (
    exchange_1,
    exchange_2,
    exchange_3,
    first_proposition,
    gain_quota,
    initialisation,
)
from libraries.paper import Paper


def test_initialisation():
    ConfigsFile = "data/config.json"
    AffFile = "data/2024-02-12-DipInfoAfferenze-PO-PA-RIC-orig.xlsx"
    ProdFile = (
        "data/2024-02-12-prodotti-PO-PA-RIC-02A-03A-03B-04A-04B-2020-instampa.xlsx"
    )

    list_persons, nb_persons, list_papers, objectif = initialisation(
        ConfigsFile, AffFile, ProdFile
    )

    list_persons, nb_proposed_papers = first_proposition(list_persons)

    assert nb_proposed_papers in range(
        nb_persons - 5, nb_persons + 1
    ), "too much people don't have a first proposed paper"

    list_persons, list_papers, nb_proposed_papers = gain_quota(
        list_persons, list_papers, objectif, nb_proposed_papers
    )

    all_proposed_paper: List[Paper] = list()

    for person in list_persons:
        assert person.nb_proposed_papers < 5, "a person have too much proposed papers"
        for paper in person.proposed_papers:
            assert (
                paper in person.writted_papers
            ), f"{paper} is proposed but not written by {person}"
            assert (
                paper not in all_proposed_paper
            ), f"{paper} is proposed multiple times"
            all_proposed_paper.append(paper)

    assert (
        nb_proposed_papers == objectif
    ), f"the objectif isn't obtained: {nb_proposed_papers} != {objectif}"


def test_upgrades():
    ConfigsFile = "data/config.json"
    AffFile = "data/2024-02-12-DipInfoAfferenze-PO-PA-RIC-orig.xlsx"
    ProdFile = (
        "data/2024-02-12-prodotti-PO-PA-RIC-02A-03A-03B-04A-04B-2020-instampa.xlsx"
    )

    list_persons, nb_persons, list_papers, objectif = initialisation(
        ConfigsFile, AffFile, ProdFile
    )

    list_persons, nb_proposed_papers = first_proposition(list_persons)

    list_persons, list_papers, nb_proposed_papers = gain_quota(
        list_persons, list_papers, objectif, nb_proposed_papers
    )

    sum_scores: float = 0.0

    for person in list_persons:
        for paper in person.proposed_papers:
            sum_scores += paper.value

    exchange_1(list_papers, list_persons)

    sum_first_exchange: float = 0.0

    for person in list_persons:
        for paper in person.proposed_papers:
            sum_first_exchange += paper.value

    assert (
        sum_first_exchange == sum_scores
    ), "The first exchange can't change the score of the selection."

    all_proposed_paper: List[Paper] = list()

    for person in list_persons:
        assert person.nb_proposed_papers < 5, "a person have too much proposed papers"
        for paper in person.proposed_papers:
            assert (
                paper in person.writted_papers
            ), f"{paper} is proposed but not written by {person}"
            assert (
                paper not in all_proposed_paper
            ), f"{paper} is proposed multiple times"
            all_proposed_paper.append(paper)

    exchange_2(list_persons)

    sum_second_exchange = 0.0

    for person in list_persons:
        for paper in person.proposed_papers:
            sum_second_exchange += paper.value

    assert (
        sum_second_exchange >= sum_first_exchange
    ), "The second exchange can't make the score worst than before"

    all_proposed_paper = list()

    for person in list_persons:
        assert person.nb_proposed_papers < 5, "a person have too much proposed papers"
        for paper in person.proposed_papers:
            assert (
                paper in person.writted_papers
            ), f"{paper} is proposed but not written by {person}"
            assert (
                paper not in all_proposed_paper
            ), f"{paper} is proposed multiple times"
            all_proposed_paper.append(paper)

    exchange_3(list_papers, list_persons)

    sum_third_exchange = 0.0

    for person in list_persons:
        for paper in person.proposed_papers:
            sum_third_exchange += paper.value

    assert (
        sum_third_exchange >= sum_second_exchange
    ), "The third exchange can't make the score worst than before"

    all_proposed_paper = list()

    for person in list_persons:
        assert person.nb_proposed_papers < 5, "a person have too much proposed papers"
        for paper in person.proposed_papers:
            assert (
                paper in person.writted_papers
            ), f"{paper} is proposed but not written by {person}"
            assert (
                paper not in all_proposed_paper
            ), f"{paper} is proposed multiple times"
            all_proposed_paper.append(paper)

    assert (
        nb_proposed_papers == objectif
    ), f"the objectif isn't obtained: {nb_proposed_papers} != {objectif}"
