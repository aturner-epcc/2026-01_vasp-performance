# EPCC VASP Performance Data: MCC VASP Workshop 2026

Repository for VASP performance data collected at EPCC for 2026 MCC VASP workshop.

Results for two benchmarks on three difference EPCC systems.

Subdirectories:

- [analysis](./analysis/) - Scripts for extracting data from output files, Marimo notebooks for analysis and plotting
- [csv_data](./csv_data/) - Job data extracted from output files, used for input to Marimo notebooks
- [output_data](./output_data/) - aw output data from VASP calculations
- [plots](./plots/) - Performance plots produced by Marimo notebooks

## Benchmarks

- TiO<sub>2</sub>
   + Gamma-point: vasp_gam
   + Pure DFT
   + 1080 ions
   + Bands: 5184 -- 9216 (most in range 5184 -- 5632)
   + NELM = 10
- CdTe Hybrid
   + Non-collinear calculation: vasp_ncl
   + Exact exchange
   + 64 ions
   + 8 k-points
   + Bands: 770 – 1052 (most in range 770 – 812)
   +NELM = 6

## HPC Systems

- [ARCHER2](https://www.archer2.ac.uk)
   + HPE Cray EX
   + 5860 compute nodes: 
   + 2x AMD EPYC 7742 (Rome) 64-core processor
   + 256/512 GB RAM
   + HPE Cray Slingshot 10 interconnect
- [Cirrus](https://www.cirrus.ac.uk)
   + HPE Cray EX4000
   + 256 compute nodes:
   + 2x AMD EPYC 9825 (Turin) 144-core processor
   + 768/1536 GB RAM
   + HPE Cray Slingshot 11 interconnect
- [Tursa](https://epcced.github.io/dirac-docs/)
   + Eviden Sequana XH2000
   + 178 compute nodes:
   + 2x AMD EPYC 7302/7413 16/24-core processor
   + 1024 GB RAM
   + 4x NVIDIA A100 GPU
   + Infiniband interconnect

