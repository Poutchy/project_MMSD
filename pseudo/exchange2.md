= Explication of the second exchange type

In the second exchange we would like to improve the solution by performing direct swaps between authors. We take a better paper from one author and replace a worse one in another author’s proposed list.

== pseudo code:

```python

def exchange_2(list_persons: PersonCollection):
    for person in list_persons with nb_presented_paper < limit:
        non_presented_papers = [person.writted.presented - person.presented]
        
        for paper in non_presented_papers:
            delta: int = 0 
            other_person = paper.presenter
            paper_other_person = min(other_person.presented_paper)
            
            for person2 in list_person:
                if person2.nb_presented_paper <= 1 or person2 is person:
                    continue
                for other_paper in person2.proposed_papers:
                    n_delta = paper.value - other_paper.value
                    if n_delta > delta:
                        other_person = person2
                        old_paper = other_paper
                        delta = n_delta

            if other_person is not None and old_paper is not None:
                other_person.unpropose_paper(old_paper)
                person.propose_paper(paper)
                break

```

= notes on that exchange:

Be careful, we are trying to exchange papers, not add new ones.

For that reason, we will ONLY work on the papers that are presented by one and only one person at a time.

Also, because we will create new person that are eligible, we will here only compute once the list at the start, for the loop.

Because of the number of time that algorithm can be launched, that part can be really slow for some implementations of the program.

Because this change can have new targets after the change n°2, you can apply it multiple times.

All the papers are ordered from the bests to the worst.
