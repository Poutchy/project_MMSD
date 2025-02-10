from libraries.list_papers import PaperCollection
from libraries.list_persons import PersonCollection
from libraries.importExcel import createTableLecturers, createTableProducts
from libraries.paper import Paper
from libraries.person import Person

# import of all the papers and persons

Configs = "data/config.json"
AffFile = "data/2024-02-12-DipInfoAfferenze-PO-PA-RIC-orig.xlsx"
ProdFile = "data/2024-02-12-prodotti-PO-PA-RIC-02A-03A-03B-04A-04B-2020-instampa.xlsx"

AffTable = createTableLecturers(AffFile, Configs)
ProdTable = createTableProducts(ProdFile, Configs)

# list_persons: PersonCollection = PersonCollection()
# list_papers: PaperCollection = PaperCollection()

# for _, row in AffTable.iterrows():
#     new_guy: Person = Person(row["Identificativi - ID IRIS"], row["Nome"], row["Cognome"], row["Affiliazione - Matricola"])
#     if not new_guy in list_persons:
#         list_persons.add_person(new_guy)

for _, row in ProdTable.iterrows():
    print(row.keys)
    break
    # new_paper: Paper = Paper(row["ID prodotto"], row["Titolo"], 1)
    # if not new_paper in list_papers:
    #     list_papers.add_paper(new_paper)
    # list_persons[row["autore: Matricola"]].add_writted_paper(new_paper)
    # writte all co author

# list_remove: list[Person] = []

# for person in list_persons.sorted_persons():
#     for paper in person.writted_papers:
#         if paper.status == 0:
#             person.propose_paper(paper)
#             break
#     if person.nb_proposed_papers != 0:
#         continue
#     list_remove.append(person)

# for person in list_remove:
#     list_persons.remove_person(person)
