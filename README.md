# SmartPortfolio

SmartPortfolio is an interactive application for **portfolio construction and financial asset analysis** based on the **Efficient Frontier model** from Modern Portfolio Theory.

The application allows users to explore how different combinations of financial assets affect the **risk–return trade-off** of an investment portfolio. By combining financial theory, statistical estimation and interactive visualization, SmartPortfolio makes portfolio optimization accessible to both technical and non-expert users.

The main goal of the project is to provide a **clear and intuitive environment to analyze portfolios, understand diversification, and evaluate optimal asset allocations**.

---

# Application Overview

The interface is organized into four main sections:

🏠 **Home**
General introduction to the project and theoretical background of the efficient frontier model.

💹 **Asset Selection**
Users can select assets from a predefined local database or import new assets by specifying their ticker. The interface also allows users to define the time range for the analysis and visualize correlation matrices and expected returns.

📊 **Efficient Frontier**
Displays the efficient frontier computed from the selected assets. Users can interactively explore optimal portfolios and compare them with custom portfolios.

⚙️ **Configuration**
Allows users to configure the parameters used in the analysis, including the asset database and the statistical methods used to estimate expected returns and covariance matrices.

---

# Main Features

### Asset Selection and Import

Users can select assets from a **local asset database** or import additional assets by specifying their ticker.

This allows flexible portfolio construction combining predefined datasets with external financial instruments.

---

### Efficient Frontier Visualization

The application computes the efficient frontier for the selected assets and allows users to **navigate along it interactively**, exploring different optimal portfolios.

Users can also define their own portfolios and compare their risk/return profile with the optimal frontier.

---

### Advanced Configuration

Users can configure the statistical methods used to estimate:

* Expected returns
* Covariance matrices

Additional parameters such as **kernel choice, estimation method, and bandwidth** can also be adjusted.

---

# How to Use the Application

## 💹 Asset Selection

### Local Asset Selection

Choose assets from the predefined asset universe stored in the local database.

### Asset Import

New assets can be imported by specifying their **ticker**.

### Date Range Selection

Define the historical period used to compute returns and correlations.

### Correlation and Expected Return Matrices

The application displays correlation matrices and expected returns to help users understand the relationships between assets.

---

## 📊 Efficient Frontier Analysis

### Efficient Frontier Visualization

Once assets are selected, the application computes and displays the associated efficient frontier.

### Interactive Exploration

Users can move along the frontier using an interactive selector to explore optimal asset allocations.

### Comparison with Custom Portfolios

Users can define custom portfolios and compare their **risk/return profile** with the efficient frontier.

---

## ⚙️ Configuration

### Asset Database

Specify which local asset database will be used for the analysis.

### Expected Return Estimation

Configure the method and parameters used to estimate expected returns.

### Covariance Matrix Estimation

Define the method, kernel, and parameters used to estimate the covariance matrix.

---

# Asset Databases

SmartPortfolio supports multiple **asset databases**.
Each database defines a universe of financial assets and the data associated with them.

Asset databases are stored as folders inside:

```
.streamlit/data/
```

Each folder represents a **versioned asset universe** (for example `V1`, `V2`, `V3`).

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

The folder name should represent the **version of the asset universe**.

---

## 2. Required Folder Structure

Each asset database must follow this structure:

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
| `*.json`              | Data files associated with each asset   |

Each asset listed in `asset_universe.xlsx` must have a corresponding JSON file stored in the same folder.

---

# Asset Universe File

The file `asset_universe.xlsx` defines the list of assets available in the database.

## Required Columns

| Column       | Description                                              |
| ------------ | -------------------------------------------------------- |
| `asset`      | Asset identifier (typically ISIN)                        |
| `source`     | Data source (`local` if the JSON file is stored locally) |
| `file`       | Name of the JSON file containing the asset data          |
| `asset_name` | Human-readable name of the asset                         |
| `America`    | Percentage exposure to America                           |
| `Europe`     | Percentage exposure to Europe                            |
| `Asia`       | Percentage exposure to Asia                              |

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

These files contain the data used by the application to compute returns and portfolio statistics.

---

# Register the Database

After creating the folder and adding the assets, register the new database in:

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

To ensure the application works correctly:

1. Each asset must have a **unique identifier**.
2. Every row in `asset_universe.xlsx` must reference an existing JSON file.
3. The filename in the `file` column must match the real file name exactly.
4. The geographic exposure columns (`America`, `Europe`, `Asia`) should sum approximately to **100**.
5. All JSON files must be stored in the **same folder as `asset_universe.xlsx`**.

---

# Best Practices

Recommended conventions when adding new asset databases:

* Use **ISIN codes** as asset identifiers.
* Keep database folders **versioned** (`V1`, `V2`, `V3`).
* Avoid modifying existing versions once they are created.
* When updating the asset universe, create a **new version folder**.

Example:

```
.streamlit/data/
├─ V1/
├─ V2/
└─ V3/
```

This ensures reproducibility of analyses performed with older datasets.

---

# Efficient Frontier Model

The efficient frontier model relies on the estimation of the **covariance matrix of asset returns**

Σ

and the **expected return vector**

μ

For a set of **n available assets**

(a₁, a₂, …, aₙ)

a portfolio is defined by the proportion of capital allocated to each asset.

More formally, each portfolio is represented by a probability vector:

w = (w₁, w₂, …, wₙ) ∈ [0,1]ⁿ

such that:

∑ wᵢ = 1

This means:

* wᵢ represents the weight of asset i in the portfolio
* The sum of all weights equals 1
* Each weight lies between 0 and 1 (short selling is not considered)

---

## Portfolio Risk and Expected Return

For a portfolio defined by weights **w**, its variance and expected return are:

σ² = w Σ wᵀ

μ̂ = μ wᵀ

Where:

* Σ is the covariance matrix
* μ is the vector of expected returns

---

## Efficient Frontier Definition

The efficient frontier is the set of portfolios that **minimize risk for a given expected return**.

Formally:

{ (μₚ, σₚ) | σₚ = min_w w Σ wᵀ subject to μ wᵀ = μₚ }

Each point on the frontier represents an **optimal portfolio**.

If a portfolio does not lie on the frontier, another portfolio exists that provides:

* higher return for the same risk, or
* lower risk for the same return.

---

## Key Portfolios on the Frontier

Two portfolios are particularly important:

**Minimum Variance Portfolio**

The portfolio with the lowest possible risk.

**Maximum Return Portfolio**

The portfolio with the highest expected return, typically corresponding to allocating **100% of the capital to the asset with the highest expected return**.

---

# Author

Created by **Alonso del Rincón Loza**
