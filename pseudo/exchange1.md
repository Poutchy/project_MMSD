= Explication of the first exchange type

In the first exchange we would like to make sure that every people only take the bests papers they can presents. It tries to replace low value papers proposed by an author with higher value papers they have written but not yet proposed.


== pseudo code:

```python

def exchange_1(list_papers: PaperCollection):
    change: bool
    while True:
        change = False
        for paper: Paper in list_papers:
            if not paper.is_presented:
                delta: int = 0 # no exchange will be made if delta = 0
                old_paper: Paper = None
                person_old_paper: Paper = None
                for person: Person in paper.authors:
                    for other_paper: Paper in person.proposed_papers:
                        n_delta = paper.value - other_paper.value
                        if n_delta > delta:
                            old_paper = other_paper
                            delta = n_delta
                            person_old_paper = person
                if old_paper is not None and person_old_paper is not None:
                    person_old_paper.unpropose(old_paper)
                    person_old_paper.propose(paper)
                    change = True
                    break
        if not change:
            break

```

= notes on that exchange:
Be careful, we are trying to exchange papers, not add new ones.
For that reason, we will ONLY work on the papers that are presented by one and only one person at a time until it don't change anymore.
Because of the number of time that algorithm can be launched, that part can be really slow for some implementations of the program.
Because this change can have new targets after the change n°2, you can apply it multiple times.

All the papers are ordered from the bests to the worst.
