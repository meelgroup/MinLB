### MinLB
On lower bound on minimal model count. The related publication: [paper](https://www.cambridge.org/core/journals/theory-and-practice-of-logic-programming/article/on-lower-bounding-minimal-model-count/8A0A50842E7F625DA60C24A28050434D)

### Clone the repo
```
git clone --recurse-submodules git@github.com:meelgroup/MinLB.git
```

### Dependencies
You need to install cmake, g++, re2c, and bison.
```
sudo apt-get install bison
sudo apt-get install re2c
sudo apt install build-essential cmake
```

You also need to install `gmp` and `mpfr`.
```
sudo apt-get install libgmp-dev libmpfr-dev
```

Install the following python packages
- [clingo](https://github.com/potassco/clingo): install from [potassco](https://potassco.org/clingo/)
- [networkx](https://pypi.org/project/networkx/): `pip install networks`


## Run HashCount
hashcount is a modified implementation of [ApproxASP](https://github.com/meelgroup/ApproxASP). It is added as a submodule in `hashcount` directory. 

First you need to compile `hashcount`. cd to hashcount and see the readme present in `hashcount` directory to compile hashcount. After sucessful compilation, mv hashcount binary to `scripts` directory.

The command to run ``HashCount`` on model counting benchmark:
```
python run_hashcount_on_modelcounting.py -i mccmc2021_track1_058.cnf
```
The command to run ``HashCount`` on item mining benchmark:
```
python run_hashcount_on_itemmining.py -i vote.cnf
```

## Run ProjEnum
The tree decomposer of `ProjEnum` is the similar tree decomposition of [SharpSAT-TD](https://github.com/Laakeri/sharpsat-td). The implementation is added as a submodule in treedecom. To compile it, first cd to treedecom and build it using the command in the README present in `treedecom` directory. After successful compilation, mv td and flow_cutter_pace17 to `scripts` directory, then cd to scripts.

The command to run ``ProjEnum`` on model counting benchmark:
```
python run_projenum_on_modelcounting.py -i mccmc2021_track1_058.cnf
```
The command to run ``ProjEnum`` on item mining benchmark:
```
python run_projenum_on_itemmining.py -i vote.cnf
```

Proj-Enum runs the tree decomposer for ``100s`` to compute a cut of the Boolean formula.

## Benchmarks
The benchmarks and artifact can be found [here](https://zenodo.org/records/13337006).

## Reference
```
@article{KM2024,
  title={On lower bounding minimal model count},
  author={Kabir, Mohimenul and Meel, Kuldeep S},
  journal={Theory and Practice of Logic Programming},
  volume={24},
  number={4},
  pages={586--605},
  year={2024},
  publisher={Cambridge University Press}
}
```

