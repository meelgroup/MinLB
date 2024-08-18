### Minimal Model Counting
__We run our experiment in a linux environment__

## Requirements
Your system must have [clingo](https://github.com/potassco/clingo) and [networkx](https://pypi.org/project/networkx/) installed.

## Directory Structure
- ``compute_dlp.py``, ``propagator.py``, ``compute_independent_support.py`` and ``prepare_td.py`` : useful scripts
- ``decomposition.py``: script to run ProjEnum
- ``hashCount``: Static binary of HashCount
- ``td`` and ``flow_cutter_pace17``: tools for computing tree decomposition and cut

## Benchmarks
The benchmarks can be found [here](https://zenodo.org/records/13337006).

## Quick Run Proj-Enum
(__Install clingo in your system__) ``ProjEnumInput`` folder contains input instances in ProjEnum input format. First unzip:
```
unzip ProjEnumInput.zip
```

Run ``ProjEnum`` on input ``mcctrack1_002.mcc2020_cnf``:
```
cp ProjEnumInput/cut_mcctrack1_002.mcc2020_cnf .
python decomposition.py -i cut_mcctrack1_002.mcc2020_cnf -c 1
```

## Quick Run HashCounter
__(Make sure that hashcounter is executable in your machine or run chmod +x hashcounter)__
``HashCounterInput`` folder contains input instances in HashCounter input format. First unzip:

```
unzip HashCounterInput.zip
```
Run ``HashCounter`` on input ``mcctrack1_002.mcc2020_cnf`` (``chmod +x hashcounter`` if hashcounter is not executable):
```
cp HashCounterInput/dlp_mcctrack1_002.mcc2020_cnf HashCounterInput/IS_dlp_mcctrack1_002.mcc2020_cnf .
./hashcounter --useind IS_dlp_mcctrack1_002.mcc2020_cnf --asp dlp_mcctrack1_002.mcc2020_cnf
```


## Run HashCount Step-by-Step
(__Install clingo in your system__)

(__``chmod +x hashcounter`` if hashcounter is not executable__)

The command to run ``HashCount`` on model counting benchmark:
```
python run_hashcount_on_modelcounting.py -i mccmc2021_track1_058.cnf
```
The command to run ``HashCount`` on item mining benchmark:
```
python run_hashcount_on_itemmining.py -i vote.cnf
```

## Run Proj-Enum Step-by-Step
(__Install clingo in your system__)

(__Make sure that td and flow_cutter_pace17 are executable in your machine (run chmod +x td flow_cutter_pace17)__)

Proj-Enum runs a tree decomposer for ``100s`` to compute a cut of the Boolean formula.
The command to run ``ProjEnum`` on model counting benchmark:
```
python run_projenum_on_modelcounting.py -i mccmc2021_track1_058.cnf
```
The command to run ``ProjEnum`` on item mining benchmark:
```
python run_projenum_on_itemmining.py -i vote.cnf
```


