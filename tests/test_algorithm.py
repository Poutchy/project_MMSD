import pytest

from libraries.functions_algo import first_proposition, gain_quota, initialisation


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

    assert nb_proposed_papers in range(nb_persons - 5, nb_persons + 1)

    list_persons, list_papers, nb_proposed_papers = gain_quota(
        list_persons, list_papers, objectif, nb_proposed_papers
    )

    all_proposed_paper = list()

    for person in list_persons:
        assert person.nb_proposed_papers < 5, "enough people have a proposed paper"
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
