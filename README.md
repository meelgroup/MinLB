## MinLB
On lowering bound on minimal model count. The related publication: [paper](https://www.cambridge.org/core/journals/theory-and-practice-of-logic-programming/article/on-lower-bounding-minimal-model-count/8A0A50842E7F625DA60C24A28050434D)

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

You also need to install `gmp`, `mpfr`, `clasp`, `gringo`, and `python`.
```
sudo apt-get install libgmp-dev libmpfr-dev gringo clasp python3-pip
```

Install the following python packages
- [clingo](https://github.com/potassco/clingo): `pip install clingo`
- [networkx](https://pypi.org/project/networkx/): `pip install networks`


## Compile
Build using `build.sh` as follows:
```
chmod +x build.sh
./build.sh
```

## Run MinLB
The input to MinLB is a CNF formula. Depending on the decomposability of the formula, MinLB chooses either ProjEnum or HashCount. We quantify decomposability by the cut size of the formula; see our [paper](https://www.cambridge.org/core/journals/theory-and-practice-of-logic-programming/article/on-lower-bounding-minimal-model-count/8A0A50842E7F625DA60C24A28050434D) for details. If the cut size is below a user-specified threshold, MinLB runs ProjEnum; otherwise, it runs HashCount.

To run MinLB, first `cd scripts`. 

Now execute:
```
python run_minlb.py -i mccmc2021_track1_058.cnf --thresh 20
```
In this example, MinLB runs ProjEnum if the cut size is smaller than `20`; otherwise, it runs HashCount. The cut size is computed using a _tree decomposition_ based method, where the underlying tree decomposer is allowed to run for 100 seconds.

## Run HashCount
First `cd scripts`:

To run ``HashCount``, execute:
```
python run_hashcount.py -i mccmc2021_track1_058.cnf
```

## Run ProjEnum
First `cd scripts`:

To run ``ProjEnum``, execute:
```
python run_projenum.py -i mccmc2021_track1_058.cnf
```

ProjEnum runs a tree decomposer for `100` seconds. 

## Benchmarks
The benchmarks and artifact can be found [here](https://zenodo.org/records/19757334).

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

