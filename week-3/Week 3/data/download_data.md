# Downloading the Data

The competition data is distributed via Google Drive (it is too large to commit
to GitHub). Download the three parquet files and place them in this `data/`
folder.

**Drive folder:**
https://drive.google.com/drive/folders/1oE8A3YCEcDeTiv9Yc2QtzEUBX2XyLDtW?usp=sharing

## Option 1 — Manual download (easiest)

1. Open the Drive folder link above.
2. Download each file: `features.parquet`, `returns.parquet`, `universe.parquet`.
3. Move all three into the `Week 3/data/` directory of this repository.

After this, your folder should look like:

```
Week 3/data/
├── README.md
├── download_data.md
├── features.parquet
├── returns.parquet
└── universe.parquet
```

## Option 2 — Command line with gdown

```bash
pip install gdown
# from inside the Week 3/data/ directory:
gdown --folder "https://drive.google.com/drive/folders/1oE8A3YCEcDeTiv9Yc2QtzEUBX2XyLDtW"
```

## Verify

```python
import pandas as pd
features = pd.read_parquet("data/features.parquet")
universe = pd.read_parquet("data/universe.parquet")
returns  = pd.read_parquet("data/returns.parquet")
print(features.shape, universe.shape, returns.shape)
```

> Do not commit the parquet files back to the repository — they are listed in
> `.gitignore`.
