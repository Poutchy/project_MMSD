= Explication of the first exchange type

In the first exchange we would like to make sure that every people that don't have a paper take at least one.

== pseudo code:

```python
def exchange_1(list_persons: PersonCollection):
    for person: Person in list_persons:
        if person.nb_presented_papers == 0:
            for paper: Paper in person.writted_paper:
                if not paper.is_presented:
                    continue
                other_person: Person = paper.presenter
                if other_person.nb_presented_papers > 1:
                    other_person.unpropose_paper(paper)
                    person.propose_paper(paper)
                    break
            else:
                continue
```

= notes on that exchange:
Be careful, we are trying to exchange papers, not add new ones.
For that reason, we will ONLY work on the papers that are presented, and not on the others.
Because this change can have new targets after the change n°2, you can apply it multiple times.
