# haddock_param_scripts
Python scripts to manipulate HADDOCK2.4 parameter files (*.json)

Tested with __Python3.6__

## Summary

```bash
$> python haddock_param_summary.py job_params.json
it0	1000
it1	20
itw	20
Partner1: Protein
Partner2: Protein
clust_meth: FCC
clust_cutoff: 0.6
```

## Get input PDB files

```bash
$> python haddock_param_extract_pdb.py job_params.json
partner1.pdb created
partner2.pdb created
```
