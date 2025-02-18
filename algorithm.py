from libraries.list_papers import PaperCollection
from libraries.list_persons import PersonCollection
from libraries.importExcel import createTableLecturers, createTableProducts
from libraries.paper import Paper, threshold
from libraries.person import Person
import json

# import of all the papers and persons

ConfigsFile = "data/config.json"
AffFile = "data/2024-02-12-DipInfoAfferenze-PO-PA-RIC-orig.xlsx"
ProdFile = "data/2024-02-12-prodotti-PO-PA-RIC-02A-03A-03B-04A-04B-2020-instampa.xlsx"

AffTable = createTableLecturers(AffFile, ConfigsFile)
ProdTable = createTableProducts(ProdFile, ConfigsFile)

list_persons: PersonCollection = PersonCollection()
list_papers: PaperCollection = PaperCollection()
nb_proposed_papers = 0
nb_person = 0

with open(ConfigsFile, 'r') as cf:
    configs = json.load(cf)

for _, row in AffTable.iterrows():
    new_guy: Person = Person(row["Identificativi - ID IRIS"], row["Nome"], row["Cognome"], row["Affiliazione - Matricola"])
    if not new_guy in list_persons:
        nb_person += 1
        list_persons.add_person(new_guy)

objectif = int(2.5 * nb_person)

for _, row in ProdTable.iterrows():
    if row["Anno di pubblicazione"] < configs["begin_year"]  or row["Anno di pubblicazione"] > configs["end_year"]:
        pass
    
    if not row["ID prodotto"] in list_papers:
      
        val_array = [
            threshold(row["scopus: Percentili  rivista - CITESCORE non pesata - miglior percentile"], configs),
            threshold(row["scopus: Percentili rivista - CITESCORE pesata - miglior percentile"], configs),
            threshold(row["scopus: Percentili rivista - SJR non pesata - miglior percentile"], configs),
            threshold(row["scopus: Percentili rivista - SJR pesata - miglior percentile"], configs),
            threshold(row["scopus: Percentili rivista - SNIP non pesata - miglior percentile"], configs),
            threshold(row["scopus: Percentili rivista - SNIP pesata - miglior percentile"], configs),
            threshold(row["wos: Percentili rivista - IF - miglior percentile"], configs),
            threshold(row["wos: Percentili rivista - 5 anni IF - miglior percentile"], configs),
        ]

        paper_value = max(val_array)

        new_paper: Paper = Paper(row["ID prodotto"], row["Titolo"], paper_value) 
        list_papers.add_paper(new_paper)
    paper = list_papers[row["ID prodotto"]]
    list_persons[row["autore: ID persona (IRIS)"]].add_writted_paper(paper)

for person in list_persons.sorted_persons():
    for paper in person.writted_papers:
        if paper.status == 0:
            person.propose_paper(paper)
            nb_proposed_papers += 1
            break
    if person.nb_proposed_papers != 0:
        continue

# for paper in list_papers: 
#     print(paper)

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

for paper in list_papers.sorted_papers(): 
    if nb_proposed_papers == objectif:
        break
    if paper.is_presented():
        continue
    list_writter = [ person for person in list_persons if person.has_written(paper) ]

    for person in list_writter: 
        if person.nb_proposed_papers < 4: 
            person.propose_paper(paper)
            nb_proposed_papers += 1
            break
    
for person in list_persons:
    print(f"papers of {person}:")
    print("  writted paper")
    for paper in person.writted_papers:
        print(f"    {paper}")
    print("  proposed paper")
    for paper in person.proposed_papers:
        print(f"    {paper}")

# for person in list_remove:
#     print(person)
#     print("  proposed paper")
#     for paper in person.proposed_papers:
#         print(f"    {paper}")

print(f"objectif: {objectif}")
print(f"nb_proposed paper: {nb_proposed_papers}")

