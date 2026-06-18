# Dataset Download

The dataset is hosted externally due to GitHub file size limits.

Download from:

https://drive.google.com/drive/folders/1oE8A3YCEcDeTiv9Yc2QtzEUBX2XyLDtW?usp=sharing

Required files:

- features.parquet
- returns.parquet
- universe.parquet

Place all three files directly inside this `data/` folder so the paths look
like `data/features.parquet`, `data/returns.parquet`, and
`data/universe.parquet`. Everything in the repo (notebook, `src/utils.py`,
docs) references these by relative path, so no other changes are needed once
the files are here.

> These files are **not** committed to the repository. See
> [`download_data.md`](download_data.md) for step-by-step instructions.
