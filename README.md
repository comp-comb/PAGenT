# PAGenT: Particle Aggregate Generator Tool

PAGenT is a simple, tunable Python tool for generating fractal particle aggregates. It leverages Particle Cluster and Cluster–Cluster aggregation algorithms to create customizable fractal structures with adjustable parameters such as particle radii, radius of gyration, and fractal dimension.

## Method

PAGenT implements the aggregation method described in:

**Morán, J., Fuentes, A., Liu, F., & Yon, J. (2019). FracVAL: An improved tunable algorithm of cluster–cluster aggregation for generation of fractal structures formed by polydisperse primary particles. *Comput. Phys. Commun.*, 239, 225–237. doi: 10.1016/j.cpc.2019.01.015**

This algorithm allows for the generation of fractal aggregates formed by polydisperse primary particles, making it ideal for various computational physics and simulation applications.

## Repository Structure

```
PAGenT/
├── PAGenT.py               # core fractal-aggregate generator
├── README.md               # this file
└── image_mask_generation/  # new module for mask & noise pipeline + GUI
    ├── pipeline.py         # command-line mask & noise pipeline
    └── gui.py              # PyQt5 GUI front-end
```

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:comp-comb/PAGenT.git
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   cd PAGenT
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

*`requirements.txt` should include:*
```text
numpy
pandas
matplotlib
pyvista
noise
pillow
PyQt5
```

## Usage

### 1. Fractal Aggregate Generator

Run the core generator:
```bash
python PAGenT.py
```
![image](https://github.com/user-attachments/assets/c7272968-477b-4903-8fec-8e32e7a31277)


### 2. Image Mask & Noise Pipeline (CLI)

Parse XML clusters, generate 1-bit masks, render base images, and apply noise/TEM backgrounds:
```bash
cd image_mask_generation
python pipeline.py \
  --xml_dir ./xmls/ \
  --file_begins_with geometry \
  --file_ends_with .xml \
  --output_csv ./data.csv \
  --mask_dir ./masks/ \
  --image_dir ./images/ \
  --noisyoutput_dir ./noisyoutput/ \
  --mask_type both \
  --noise_types gauss,poisson,tem \
  --tem_style \
  --tem_mean 180 \
  --tem_std 25 \
  --tem_color 0.045,0.045,0.045,0.3
```
> **Note:** Adjust `noise_types` (comma‑separated) and `tem_color` (RGBA floats) as desired.

### 3. Image Mask & Noise Pipeline (GUI)

Launch an interactive Qt app:
```bash
cd image_mask_generation
python gui.py
```

Use the GUI to:
- Browse for your **working directory** and **XML folder** (defaults to `<working_dir>/xmls/`).
- Set **file prefix/suffix** filters.
- Select **Particle** and/or **Cluster** masks.
- Choose one or more **noise types** (Gaussian, Poisson, Combined, TEM).
- Toggle **TEM style**, set **mean**, **std**, and pick **TEM overlay color** (with opacity).
- Switch between **Light** and **Dark** themes for the interface.
- Click **Run** to generate masks and noisy images.

![image](https://github.com/user-attachments/assets/6dc7b3d4-7150-45bd-ba0f-87404f147f51)


- **mask_type**: `particle`, `cluster`, or `both`.
- **noise_types**: list of `gauss`, `poisson`, `combined`, `tem`.
- **tem_style**: enable grainy TEM background.
- **tem_mean**, **tem_std**: control background noise distribution.
- **tem_color**: RGBA tuple `(r,g,b,a)` with values in `[0,1]`.

## To Cite PAGenT
```bibtex
@misc{PAGenT-v0.2a,
  title = {{PAGenT: Particle Aggregate Generation Tool. v0.2.0-alpha}},
  author = {Mukut. K. M. and Gray, I. and Day, T. and Roy, S. P.},
  year = {2025},
  url = {https://github.com/comp-comb/PAGenT}
}
```

## Current Status
> **Note:** This is an initial, untested release. Contributions, bug reports, and feedback are highly appreciated!

## Acknowledgment

This work was supported by the National Science Foundation under Grant No. 2144290. The opinions, findings, and conclusions or recommendations expressed herein are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.

## Contributing

Contributions to enhance PAGenT's functionality, performance, and usability are welcome. Please open an issue or submit a pull request with your suggestions and improvements.
