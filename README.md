# btvnano-prod

1. Modify the yml cards for production, specially the `workArea` and `outLFNDirBase`

2. Make sure the jec json file is already present in the parent directory:
```bash
ll ../jet_jerc.json.gz
```
if not, copy it for the corresponding campaing: https://cms-analysis-corrections.docs.cern.ch/

3. Send to crab by running:
```bash
python3 crabby.py -c crab_ymls/mc_summer23_wjets.yml --make --submit
```