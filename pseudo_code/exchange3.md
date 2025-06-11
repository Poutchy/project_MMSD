= Explication of the third exchange type

In the third exchange we would like insert a high value paper into the solution by making room for a paper by displacing others.

== pseudo code:

```python

def exchange_3(list_persons: PersonCollection, list_papers: PaperCollection):
    
    for paper in list_papers:
        if paper is not presented:
            _ = try_alternate(list_papers, list_persons, paper)


def try_alternate(
    list_papers: PaperCollection,
    list_persons: PersonCollection,
    paper: Paper,
    first_writter: Optional[Person] = None,
    l: Optional[List[Paper]] = None,
) -> bool:
    for writter in list_persons:
        for w_paper in writter.proposed_papers:
            if w_paper.value < paper.value:
                if try_alternate(list_papers, list_persons, w_paper, writter, new_l):
                    if first_writter is not None:  
                        first_writter.unpropose_paper(paper)
                    writter.propose_paper(paper)
                    return True
    delta: float = 0
    old_writter: Optional[Person] = None
    old_paper: Optional[Paper] = None
    for writter in list_writter:
        for other_paper in writter.proposed_papers:
            n_delta = paper.value - other_paper.value
            if n_delta > delta:
                old_writter = writter
                old_paper = other_paper
                delta = n_delta

    if old_paper is not None and old_writter is not None:
        old_writter.unpropose_paper(old_paper)
        if first_writter is not None:
            first_writter.unpropose_paper(paper)
        old_writter.propose_paper(paper)
        return True
    return False

```