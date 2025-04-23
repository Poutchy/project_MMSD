"""General example of the use of the program"""

import argparse
import json

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


def parse_args(exchange_types, parameter_to_optimize):
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        "--exchange",
        nargs="+",
        choices=exchange_types,
        help="choice of the different exchanges and their order",
    )

    param_help = "Indices of parameters to optimize. Available options:\n"
    for i, param in enumerate(parameter_to_optimize):
        param_help += f"  [{i}] {param}\n"

    parser.add_argument(
        "--params",
        nargs="+",
        type=int,
        help=param_help,
    )

    return parser.parse_args()


# import of all the papers and persons
def main(
    configs_file="data/config.json",
    aff_file="data/2024-02-12-DipInfoAfferenze-PO-PA-RIC-orig.xlsx",
    prod_file="data/2024-07-05-prodotti-PO-PA-RIC-02A-03A-03B-04A-04B-2020-instampa.xlsx",
):
    with open(configs_file, "r") as f:
        configs = json.load(f)
    param_to_optimize = configs["parameter_to_optimize"]
    exchange_types = ["1", "2", "3"]

    args = parse_args(exchange_types, param_to_optimize)
    selected_exchanges = args.exchange if args.exchange else exchange_types
    selected_parameters = (
        [param_to_optimize[i] for i in args.params]
        if args.params
        else param_to_optimize
    )

    print("Selected exchanges:", selected_exchanges)
    print("Selected parameters:")
    for param in selected_parameters:
        print(f"  - {param}")

    list_persons, _, list_papers, objectif = initialisation(
        configs_file, aff_file, prod_file, selected_parameters
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

    with open("log.json", "w", encoding="utf-8") as f:
        f.write(to_json(list_persons, nb_proposed_papers))


if __name__ == "__main__":
    main()
