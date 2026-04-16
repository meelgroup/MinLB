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

## Run HashCount
First `cd scripts`:

The command to run ``HashCount`` on model counting benchmark:
```
python run_hashcount_on_modelcounting.py -i mccmc2021_track1_058.cnf
```
The command to run ``HashCount`` on item mining benchmark:
```
python run_hashcount_on_itemmining.py -i vote.cnf
```

## Run ProjEnum
First `cd scripts`:

The command to run ``ProjEnum`` on model counting benchmark:
```
python run_projenum_on_modelcounting.py -i mccmc2021_track1_058.cnf
```
The command to run ``ProjEnum`` on item mining benchmark:
```
python run_projenum_on_itemmining.py -i vote.cnf
```


## Benchmarks
The benchmarks and artifact can be found [here](https://zenodo.org/records/19473281).

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

