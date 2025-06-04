= Explication of the second exchange type

In the second exchange we would like ?.

== pseudo code:

```python

def exchange_2(list_persons: PersonCollection):
    for person in list_persons with nb_presented_paper < limit:
        non_presented_papers = [person.writted.presented - person.presented]
        for paper in non_presented_papers:
            other_person = paper.presenter
            paper_other_person = min(other_person.presented_paper)
            if other_person.nb_presented_paper >= 2 and paper > other_paper:
                other_person.unpropose(other_paper)
                person.propose(paper)
                continue

```

= notes on that exchange:

Be careful, we are trying to exchange papers, not add new ones.

For that reason, we will ONLY work on the papers that are presented by one and only one person at a time.

Also, because we will create new person that are eligible, we will here only compute once the list at the start, for the loop.

Because of the number of time that algorithm can be launched, that part can be really slow for some implementations of the program.

Because this change can have new targets after the change n°2, you can apply it multiple times.

All the papers are ordered from the bests to the worst.
