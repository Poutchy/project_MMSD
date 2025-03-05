= Explication of the second exchange type

In the second exchange we would like to make sure that every people only take the bests papers they can presents.

== pseudo code:

```python
def exchange_2(list_papers: PaperCollection):
    change: bool
    while True:
        change = False
        for paper: Paper in list_papers:
            if not paper.is_presented:
                for person: Person in paper.authors:
                    for other_paper: Paper in person.presented:
                        if other_paper < paper:
                            person.unpropose(other_paper)
                            person.propose(paper)
                            change = True
                            break
                    else:
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
