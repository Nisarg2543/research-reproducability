# Setup Guide

## Requirements

- Python {python_version}
- conda (recommended) or pip

## Install

### Using conda (recommended)

```bash
conda env create -f environment.yml
conda activate my-research-env
```

### Using pip

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Data

Data files are in `data/`. If the `data/` folder is empty, download from: [link here]

## Expected outputs

Running the scripts produces the following files in `output/`:
- `figure1.png` — [description]
- `results.csv` — [description]

## Tested on

- [OS], Python {python_version}
