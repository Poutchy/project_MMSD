# Data types

```
Person:
    - id
    - names (name + surname)
    - list of papers wrotted as author (PaperCollection)
    - List of proposed papers (PaperCollection)

Paper:
    - id
    - title
    - score
    - attribution
    - authors (list of Person.id)
    - co-authors (list of Person.id)

PaperCollection:
    - list of papers ordered by their rank and can be accessed by ids

PersonCollection:
    - list of persons ordered by their number of papers and can be accessed by ids
```

# Algorithm

```
l_paper: PaperCollection = list of all the papers of all the department
l_persons: PersonCollection = list of all the persons of all the department
nb: int = number of paper needed with removed persons

list_remove: list[Person]
for p in l_persons:
    if p.nb_p_paper != 0: break
    nb -= nb_paper_to_remove
    list_remove.push(p)
while p = list_remove.pop():
    l_paper.pop(p)

for person in l_persons:
    for wpaper in person.list_w_paper:
        if !wpaper.is_assigned():
            person.add_paper(wpaper)

possible_take = {}
for person in l_person ordered by call = (nb_wpaper - nb_given_paper in the list + nb_presented_papers):
    if call == 0:
        possible_take[person.id] = [list_of_proposer_for_all_the_other_papers]
    if call > 1:
        while call > 1 and not_appear in possible_take dy old_person
            exchange the paper with the old_person
            and take anotherone for the actual person

for paper in list_papers:
    if nb_paper_presented == nb: break
    if paper.is_presented(): pass
    for person in paper.authors + paper.co-author:
        if person.have_place():
            person.add_paper(paper)
            nb_paper_presented++
            break
    else:
        pass

    l_old_papers = list of all papers presented by all the persons ordered by rank
    for old_paper in l_old_papers:
        if paper.rank > old_paper.rank && can_be_removed(author, old_paper):
            exchange of the old_paper and the actual paper
```