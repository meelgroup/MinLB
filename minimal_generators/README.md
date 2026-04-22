### Encoding from Minimal Generators to Minimal Models
We evaluate a lower-bounding method for the minimal generators of a database transaction. Detailed evaluation results can be found in our [paper](https://www.cambridge.org/core/journals/theory-and-practice-of-logic-programming/article/on-lower-bounding-minimal-model-count/8A0A50842E7F625DA60C24A28050434D).

To obtain the minimal-model formulation of a transaction record, use the Python script `mg_to_mm.py`. Given a transaction record `vote`, run:
```
python mg_to_mm.py -i vote
```

It creates a file `minimal_vote.cnf` such that minimal models of `minimal_vote.cnf` correspond to the minimal generators of `vote`. 

The full dataset is available [here](https://zenodo.org/records/19665509).