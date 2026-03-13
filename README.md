## Asset Databases

The application supports multiple **asset databases**.
Each database defines a universe of assets and the associated data used by the application.

Asset databases are stored as folders inside:

```
.streamlit/data/
```

Each folder represents a **versioned asset universe** (e.g. `V1`, `V2`, `V3`).

---

# Adding a New Asset Database

To add a new asset database, follow the steps below.

---

## 1. Create a New Database Folder

Create a new folder inside:

```
.streamlit/data/
```

Example:

```
.streamlit/data/V3/
```

The folder name should represent the **version of the asset universe** (e.g. `V1`, `V2`, `V3`).

---

## 2. Required Folder Structure

Each asset database folder must follow this structure:

```
.streamlit/data/V3/
│
├─ asset_universe.xlsx
├─ ES0112611001_V3.json
├─ ES0165242001_V3.json
├─ IE000N4ZYX28_V3.json
├─ IE00B42W3S00_V3.json
└─ ...
```

Where:

| File                  | Description                             |
| --------------------- | --------------------------------------- |
| `asset_universe.xlsx` | Defines the asset universe and metadata |
| `*.json`              | Data files for each asset               |

Each asset listed in `asset_universe.xlsx` must have a corresponding JSON file in the same folder.

---

# Asset Universe File

The file `asset_universe.xlsx` defines the assets included in the database.

## Required Columns

| Column       | Description                                           |
| ------------ | ----------------------------------------------------- |
| `asset`      | Asset identifier (typically ISIN)                     |
| `source`     | Data source (`local` if stored as JSON in the folder) |
| `file`       | Name of the JSON file containing the asset data       |
| `asset_name` | Human-readable name of the asset                      |
| `America`    | Percentage exposure to America                        |
| `Europe`     | Percentage exposure to Europe                         |
| `Asia`       | Percentage exposure to Asia                           |

---

## Example

| asset        | source | file                 | asset_name                                                     | America | Europe | Asia |
| ------------ | ------ | -------------------- | -------------------------------------------------------------- | ------- | ------ | ---- |
| ES0112611001 | local  | ES0112611001_V2.json | Azvalor Internacional FI                                       | 53      | 42     | 5    |
| ES0165242001 | local  | ES0165242001_V2.json | Myinvestor S&P500 Equiponderado FI                             | 99      | 1      | 0    |
| IE000N4ZYX28 | local  | IE000N4ZYX28_V2.json | iShares US Index Fund (IE) S Acc EUR                           | 100     | 0      | 0    |
| IE00B42W3S00 | local  | IE00B42W3S00_V2.json | Vanguard Global Small-Cap Index Fund Investor EUR Accumulation | 65      | 17     | 18   |
| IE00BYX5NX33 | local  | IE00BYX5NX33_V2.json | Fidelity MSCI World Index Fund P-ACC-EUR                       | 75      | 17     | 8    |
| IE0031786696 | local  | IE0031786696_V2.json | Vanguard Emerging Markets Stock Index Fund EUR Acc             | 7       | 12     | 81   |
| LU3038481936 | local  | LU3038481936_V2.json | Hamco SICAV - Global Value R EUR Acc                           | 21      | 18     | 61   |

---

# JSON Asset Files

Each asset must have a corresponding JSON file.

Example:

```
ES0112611001_V3.json
```

The filename **must exactly match** the value specified in the `file` column of `asset_universe.xlsx`.

These files contain the historical or structured data used by the application for each asset.

---

# Register the Database

After creating the folder, register the new database in:

```
.streamlit/config.toml
```

Example:

```
[assets_databases]
V1 = "Fondos indexados y de gestión activa 24/01/2026"
V2 = "MSCI WORLD + SP500 + EMERGING MARKETS + AZVALOR + HAMCO 24/01/2026"
V3 = "Custom Asset Universe"
```

Where:

| Key              | Description                                      |
| ---------------- | ------------------------------------------------ |
| `V1`, `V2`, `V3` | Folder name of the asset database                |
| Value            | Human-readable name displayed in the application |

---

# Validation Rules

To ensure the application works correctly, the following rules must be respected:

1. Each asset must have a unique `asset` identifier.
2. Each row in `asset_universe.xlsx` must reference an existing JSON file.
3. The filename in the `file` column must match the actual file in the folder.
4. Regional exposure columns (`America`, `Europe`, `Asia`) should sum to approximately **100**.
5. Asset JSON files must be stored in the same folder as `asset_universe.xlsx`.

---

# Best Practices

Recommended conventions when adding assets:

* Use **ISIN codes** as asset identifiers.
* Keep database folders **versioned** (`V1`, `V2`, `V3`).
* Avoid modifying older versions once created.
* Create a new version folder when updating the asset universe.

Example:

```
.streamlit/data/
├─ V1/
├─ V2/
└─ V3/
```

This ensures reproducibility of historical analyses.

---

# Summary

To add a new asset database:

1. Create a new folder in `.streamlit/data/`
2. Add `asset_universe.xlsx`
3. Add JSON files for each asset
4. Register the database in `.streamlit/config.toml`
5. Restart the Streamlit application

The new asset universe will then be available in the app.
