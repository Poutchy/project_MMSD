from libraries.functions_algo import (
    exchange_1,
    exchange_2,
    first_proposition,
    gain_quota,
    initialisation,
    to_json,
)

# import of all the papers and persons

ConfigsFile = "data/config.json"
AffFile = "data/2024-02-12-DipInfoAfferenze-PO-PA-RIC-orig.xlsx"
ProdFile = "data/2024-02-12-prodotti-PO-PA-RIC-02A-03A-03B-04A-04B-2020-instampa.xlsx"

list_persons, nb_persons, list_papers, objectif = initialisation(
    ConfigsFile, AffFile, ProdFile
)

# for paper in list_papers:
#     print(paper)

list_persons, nb_proposed_papers = first_proposition(list_persons)

# for person in list_persons:
#     print(f"papers of {person}:")
#     print("  writted paper")
#     for paper in person.writted_papers:
#         print(f"    {paper}")
#     print("  proposed paper")
#     for paper in person.proposed_papers:
#         print(f"    {paper}")

# for person in list_remove:
#     print(person)
#     print("  proposed paper")
#     for paper in person.proposed_papers:
#         print(f"    {paper}")

list_persons, list_papers, nb_proposed_papers = gain_quota(
    list_persons, list_papers, objectif, nb_proposed_papers
)

# sum = 0
# for person in list_persons:
#     print(f"papers of {person}:")
#     print("  writted paper")
#     for paper in person.writted_papers:
#         print(f"    {paper}")
#         sum += paper.value
#     print("  proposed paper")
#     for paper in person.proposed_papers:
#         print(f"    {paper}")

# for person in list_remove:
#     print(person)
#     print("  proposed paper")
#     for paper in person.proposed_papers:
#         print(f"    {paper}")

# print(f"objectif: {objectif}")
# print(f"nb_proposed paper: {nb_proposed_papers}")
# print(f"sum of values: {sum}")

exchange_1(list_persons)

# sum = 0
# sum_prop = 0
# for person in list_persons:
#     # print(f"papers of {person}:")
#     # print("  writted paper")
#     for paper in person.writted_papers:
#         # print(f"    {paper}")
#         sum += paper.value
#     # print("  proposed paper")
#     for paper in person.proposed_papers:
#         # print(f"    {paper}")
#         sum_prop += paper.value

# for person in list_remove:
#     print(person)
#     print("  proposed paper")
#     for paper in person.proposed_papers:
#         print(f"    {paper}")
# print(f"objectif: {objectif}")
# print(f"nb_proposed paper: {nb_proposed_papers}")
# print(f"sum of values: {sum}")
# print(f"sum of proposed values: {sum_prop}")


exchange_2(list_papers, list_persons)

# sum = 0
# sum_prop = 0
# for person in list_persons:
#     # print(f"papers of {person}:")
#     # print("  writted paper")
#     for paper in person.writted_papers:
#         # print(f"    {paper}")
#         sum += paper.value
#     # print("  proposed paper")
#     for paper in person.proposed_papers:
#         # print(f"    {paper}")
#         sum_prop += paper.value

# # for person in list_remove:
# #     print(person)
# #     print("  proposed paper")
# #     for paper in person.proposed_papers:
# #         print(f"    {paper}")
# print(f"objectif: {objectif}")
# print(f"nb_proposed paper: {nb_proposed_papers}")
# print(f"sum of values: {sum}")
# print(f"sum of proposed values: {sum_prop}")

json = to_json(list_persons)

with open("log.json", "w") as f:
    f.write(json)

# totValue = 0
# for person in list_persons:
#     for paper in person.proposed_papers:
#         totValue += paper.value

# print("totValue: ", totValue)
