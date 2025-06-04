= Explication of the third exchange type

In the second exchange we would like ?.

== pseudo code:

```python

def exchange_3(list_persons: PersonCollection, list_papers: PaperCollection):
    for person in list_persons with nb_presented_paper < limit:
        non_presented_papers = [person.writted.presented - person.presented]
        for paper in non_presented_papers:
            other_person = paper.presenter
            if other_person.nb_presented_paper == limit:
                other_person.unpropose(paper)
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
