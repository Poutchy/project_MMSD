"""General example of the use of the program"""

from libraries.functions_algo import (exchange_1, exchange_2,
                                      first_proposition, gain_quota,
                                      initialisation, to_json)


# import of all the papers and persons
def do_all(
    configs_file="data/config.json",
    aff_file="data/2024-02-12-DipInfoAfferenze-PO-PA-RIC-orig.xlsx",
    prod_file="data/2024-02-12-prodotti-PO-PA-RIC-02A-03A-03B-04A-04B-2020-instampa.xlsx",
):
    list_persons, _, list_papers, objectif = initialisation(
        configs_file, aff_file, prod_file
    )

    list_persons, nb_proposed_papers = first_proposition(list_persons)

    list_persons, list_papers, nb_proposed_papers = gain_quota(
        list_persons, list_papers, objectif, nb_proposed_papers
    )

    exchange_1(list_persons)

    exchange_2(list_papers, list_persons)

    json = to_json(list_persons)

    with open("log.json", "w", encoding="utf-8") as f:
        f.write(json)


if __name__ == "__main__":
    do_all()
