"""General example of the use of the program"""

import argparse

from libraries.functions_algo import (
    exchange_1,
    exchange_2,
    exchange_3,
    first_proposition,
    gain_quota,
    initialisation,
    recompute_objectif,
    to_json,
)


# import of all the papers and persons
def main(
    configs_file="data/config.json",
    aff_file="data/2024-02-12-DipInfoAfferenze-PO-PA-RIC-orig.xlsx",
    prod_file="data/2024-07-05-prodotti-PO-PA-RIC-02A-03A-03B-04A-04B-2020-instampa.xlsx",
):
    list_persons, _, list_papers, objectif = initialisation(
        configs_file, aff_file, prod_file
    )

    list_persons, nb_proposed_papers = first_proposition(list_persons)

    objectif = recompute_objectif(objectif, list_persons)

    json_before = to_json(list_persons, nb_proposed_papers)

    with open("log_before.json", "w", encoding="utf-8") as f:
        f.write(json_before)

    list_persons, list_papers, nb_proposed_papers = gain_quota(
        list_persons, list_papers, objectif, nb_proposed_papers
    )

    print(f"{objectif}")

    json_between = to_json(list_persons, nb_proposed_papers)

    with open("log_between.json", "w", encoding="utf-8") as f:
        f.write(json_between)

    exchange_types = ["1", "2", "3"]

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--exchange",
        nargs="+",
        choices=exchange_types,
        help="choice of the different exchanges and their order",
    )

    args = parser.parse_args()

    selected_exchanges = args.exchange if args.exchange else exchange_types
    print("Selected exchanges:", selected_exchanges)
    for ex in selected_exchanges:
        if ex == "1":
            exchange_1(list_papers, list_persons)
            json_after_1 = to_json(list_persons, nb_proposed_papers)

            with open("log_after_1.json", "w", encoding="utf-8") as f:
                f.write(json_after_1)

        elif ex == "2":
            exchange_2(list_persons)
            json_after_2 = to_json(list_persons, nb_proposed_papers)

            with open("log_after_2.json", "w", encoding="utf-8") as f:
                f.write(json_after_2)

        elif ex == "3":
            exchange_3(list_papers, list_persons)

    json = to_json(list_persons, nb_proposed_papers)

    with open("log.json", "w", encoding="utf-8") as f:
        f.write(json)

    totValue = 0
    for person in list_persons:
        for paper in person.proposed_papers:
            totValue += paper.value
    print("totvalue", totValue)


if __name__ == "__main__":
    main()
