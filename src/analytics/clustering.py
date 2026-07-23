"""
----------------------------------------------------------
Day 36 - Company Clustering
Sprint 6

Objective:
Cluster Nifty100 companies using financial metrics.

Author : Karan Taynak
----------------------------------------------------------
"""

import os
import warnings
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sqlalchemy import text
from scipy.stats import zscore
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from pathlib import Path
from src.dashboard.utils.db import get_engine

warnings.filterwarnings("ignore")

# ----------------------------------------------------------
# Features Used For Clustering
# ----------------------------------------------------------

FEATURE_COLUMNS = [

    "return_on_equity_pct",

    "debt_to_equity",

    "revenue_cagr_5yr",

    "free_cash_flow_cr",

    "operating_profit_margin_pct"

]

# ----------------------------------------------------------
# Load Latest Financial Ratios
# ----------------------------------------------------------

def load_data():

    """
    Load latest financial ratios for each company.
    """

    engine = get_engine()

    query = """

    SELECT

        fr.company_id,

        c.company_name,

        s.broad_sector AS sector,

        fr.return_on_equity_pct,

        fr.debt_to_equity,

        fr.revenue_cagr_5yr,

        fr.free_cash_flow_cr,

        fr.operating_profit_margin_pct

    FROM financial_ratios fr

    INNER JOIN (

        SELECT
            company_id,
            MAX(id) AS latest_id

        FROM financial_ratios

        GROUP BY company_id

    ) latest

        ON fr.id = latest.latest_id

    INNER JOIN companies c

        ON fr.company_id = c.id

    INNER JOIN sectors s

        ON fr.company_id = s.company_id

    ORDER BY fr.company_id;

    """

    df = pd.read_sql(text(query), engine)

    return df

# ----------------------------------------------------------
# Load Latest Financial Ratios
# ----------------------------------------------------------

def load_data():

    """
    Load latest financial ratios for each company.
    """

    engine = get_engine()
    query = """

SELECT

    fr.company_id,

    c.company_name,

    s.broad_sector AS sector,

    fr.return_on_equity_pct,

    fr.debt_to_equity,

    fr.revenue_cagr_5yr,

    fr.free_cash_flow_cr,

    fr.operating_profit_margin_pct,

    fr.net_profit_margin_pct,

    fr.interest_coverage,

    fr.asset_turnover,

    fr.earnings_per_share,

    fr.pat_cagr_5yr

FROM financial_ratios fr

INNER JOIN (

    SELECT
        company_id,
        MAX(id) AS latest_id

    FROM financial_ratios

    GROUP BY company_id

) latest

    ON fr.id = latest.latest_id

INNER JOIN companies c

    ON fr.company_id = c.id

INNER JOIN sectors s

    ON fr.company_id = s.company_id

ORDER BY fr.company_id;

"""
    df = pd.read_sql(text(query), engine)

    return df

# ----------------------------------------------------------
# Dataset Summary
# ----------------------------------------------------------

def dataset_summary(df):

    print("\n")

    print("=" * 60)

    print("DATASET SUMMARY")

    print("=" * 60)

    print(df.info())

    print()

    print(df.head())

    print()

    print("Shape :", df.shape)

    print()

    print("Missing Values")

    print(df.isna().sum())

    print("=" * 60)

# ----------------------------------------------------------
# Sector Median Imputation
# ----------------------------------------------------------

def sector_imputation(df):

    """
    Fill missing values using
    sector-wise median.
    """

    df = df.copy()

    for column in FEATURE_COLUMNS:

        df[column] = (

            df.groupby("sector")[column]

            .transform(

                lambda x: x.fillna(x.median())

            )

        )

    return df

# ----------------------------------------------------------
# Global Median Imputation
# ----------------------------------------------------------

def global_imputation(df):

    df = df.copy()

    imputer = SimpleImputer(

        strategy="median"

    )

    df[FEATURE_COLUMNS] = imputer.fit_transform(

        df[FEATURE_COLUMNS]

    )

    return df



# ----------------------------------------------------------
# Feature Scaling
# ----------------------------------------------------------

def scale_features(df):

    """
    Scale numerical features.
    """

    scaler = StandardScaler()

    scaled = scaler.fit_transform(df[FEATURE_COLUMNS])

    scaled_df = pd.DataFrame(

        scaled,

        columns=FEATURE_COLUMNS,

        index=df.index

    )

    return scaled_df, scaler

# ----------------------------------------------------------
# Features for Correlation Analysis
# ----------------------------------------------------------

CORRELATION_FEATURES = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "earnings_per_share",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
]


# ----------------------------------------------------------
# Elbow Method
# ----------------------------------------------------------

def generate_elbow_plot(scaled_df):

    inertias = []

    k_values = range(2,11)

    for k in k_values:

        model = KMeans(

            n_clusters=k,

            random_state=42,

            n_init=10

        )

        model.fit(scaled_df)

        inertias.append(model.inertia_)

    Path("reports").mkdir(exist_ok=True)

    plt.figure(figsize=(8,5))

    plt.plot(

        k_values,

        inertias,

        marker="o"

    )

    plt.title("KMeans Elbow Method")

    plt.xlabel("Number of Clusters")

    plt.ylabel("Inertia")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(

        "reports/elbow_plot.png",

        dpi=300

    )

    plt.close()

    print("✓ Elbow plot saved.")

# ----------------------------------------------------------
# KMeans Clustering
# ----------------------------------------------------------

def run_kmeans(scaled_df):

    model = KMeans(

        n_clusters=5,

        random_state=42,

        n_init=10

    )

    labels = model.fit_predict(scaled_df)

    return model, labels

# ----------------------------------------------------------
# Distance From Centroid
# ----------------------------------------------------------

def centroid_distance(model, scaled_df):

    distances = model.transform(scaled_df)

    nearest = distances.min(axis=1)

    return nearest

# ----------------------------------------------------------
# Assign Cluster Names
# ----------------------------------------------------------

def assign_cluster_names(df):

    """
    Assign meaningful names to clusters based on
    average financial characteristics.
    """

    summary = (

        df.groupby("cluster_id")[FEATURE_COLUMNS]

        .mean()

        .round(2)

    )

    print("\n")

    print("=" * 60)

    print("CLUSTER SUMMARY")

    print("=" * 60)

    print(summary)

    print("=" * 60)

    # Default names (can be refined after reviewing summary)

    cluster_names = {

        0: "Growth Leaders",

        1: "High Leverage",

        2: "Outlier",

        3: "Steady Performers",

        4: "Stable Companies"

    }

    df["cluster_name"] = df["cluster_id"].map(cluster_names)

    return df

# ----------------------------------------------------------
# Cluster Profiling
# ----------------------------------------------------------

def cluster_profile(df):
    """
    Generate mean and median statistics for each cluster.
    """

    mean_profile = (
        df.groupby("cluster_id")[FEATURE_COLUMNS]
        .mean()
        .round(2)
    )

    median_profile = (
        df.groupby("cluster_id")[FEATURE_COLUMNS]
        .median()
        .round(2)
    )

    profile = pd.concat(
        {
            "Mean": mean_profile,
            "Median": median_profile
        },
        axis=1
    )

    os.makedirs("output", exist_ok=True)

    profile.to_csv(
        "output/cluster_profile.csv"
    )

    print("\n")
    print("=" * 60)
    print("CLUSTER PROFILE")
    print("=" * 60)
    print(profile)
    print("=" * 60)

    print("\n✓ Cluster profile exported.")
    print("output/cluster_profile.csv")

    return profile

# ----------------------------------------------------------
# Correlation Heatmap
# ----------------------------------------------------------

def correlation_heatmap(df):
    """
    Generate Pearson correlation heatmap for financial KPIs.
    """

    corr_df = df[CORRELATION_FEATURES].copy()

    corr_df = corr_df.apply(pd.to_numeric, errors="coerce")

    corr = corr_df.corr(method="pearson")

    os.makedirs("reports", exist_ok=True)

    plt.figure(figsize=(12, 10))

    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="RdYlBu_r",
        square=True,
        linewidths=0.5,
        cbar=True
    )

    plt.title("Financial KPI Correlation Matrix")

    plt.tight_layout()

    plt.savefig(
        "reports/correlation_heatmap.png",
        dpi=300
    )

    plt.close()

    print("\n✓ Correlation heatmap saved.")
    print("reports/correlation_heatmap.png")

# ----------------------------------------------------------
# Outlier Detection
# ----------------------------------------------------------

def detect_outliers(df):
    """
    Detect sector-wise outliers using Z-score.
    Flags observations where |Z-score| > 3.
    """

    outliers = []

    for sector in df["sector"].unique():

        sector_df = df[df["sector"] == sector].copy()

        for feature in CORRELATION_FEATURES:

            if feature not in sector_df.columns:
                continue

            values = pd.to_numeric(
                sector_df[feature],
                errors="coerce"
            )

            if values.notna().sum() < 2:
                continue

            z_scores = zscore(
                values,
                nan_policy="omit"
            )

            sector_df[f"{feature}_z"] = z_scores

            flagged = sector_df[
                sector_df[f"{feature}_z"].abs() > 3
            ]

            for _, row in flagged.iterrows():

                outliers.append({

                    "company_id": row["company_id"],
                    "company_name": row["company_name"],
                    "sector": row["sector"],
                    "metric": feature,
                    "value": row[feature],
                    "z_score": round(
                        row[f"{feature}_z"],
                        2
                    )

                })

    outlier_df = pd.DataFrame(outliers)

    os.makedirs("output", exist_ok=True)

    outlier_df.to_csv(
        "output/outlier_report.csv",
        index=False
    )

    print()

    print("✓ Outlier report exported.")

    print("output/outlier_report.csv")

    print(f"Outliers Found : {len(outlier_df)}")

    return outlier_df

# ----------------------------------------------------------
# Portfolio Statistics
# ----------------------------------------------------------

def portfolio_statistics(df):
    """
    Generate descriptive statistics for all KPIs.
    """

    stats = []

    for feature in CORRELATION_FEATURES:

        values = pd.to_numeric(
            df[feature],
            errors="coerce"
        )

        stats.append({

            "KPI": feature,

            "P10": round(values.quantile(0.10), 2),

            "P25": round(values.quantile(0.25), 2),

            "P50": round(values.quantile(0.50), 2),

            "P75": round(values.quantile(0.75), 2),

            "P90": round(values.quantile(0.90), 2),

            "Mean": round(values.mean(), 2),

            "Std": round(values.std(), 2)

        })

    stats_df = pd.DataFrame(stats)

    os.makedirs("output", exist_ok=True)

    stats_df.to_csv(
        "output/portfolio_stats.csv",
        index=False
    )

    print()

    print("✓ Portfolio statistics exported.")

    print("output/portfolio_stats.csv")

    return stats_df

# ----------------------------------------------------------
# Cluster Members
# ----------------------------------------------------------

def export_cluster_members(df):
    """
    Export companies belonging to each cluster.
    """

    members = df[
        [
            "cluster_id",
            "cluster_name",
            "company_id",
            "company_name",
            "sector"
        ]
    ].sort_values(
        ["cluster_id", "company_name"]
    )

    members.to_csv(
        "output/cluster_members.csv",
        index=False
    )

    print("\n✓ Cluster members exported.")
    print("output/cluster_members.csv")

    return members


# ----------------------------------------------------------
# Export Results
# ----------------------------------------------------------

def export_results(df):

    os.makedirs("output", exist_ok=True)

    output = df[

        [

            "company_id",

            "cluster_id",

            "cluster_name",

            "distance_from_centroid"

        ]

    ]

    output.to_csv(

        "output/cluster_labels.csv",

        index=False

    )

    print()

    print("✓ Cluster labels exported.")

    print("output/cluster_labels.csv")


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

if __name__ == "__main__":

    df = load_data()

    dataset_summary(df)

    df = sector_imputation(df)

    df = global_imputation(df)

    scaled_df, scaler = scale_features(df)

    print()

    print("Scaled Shape :", scaled_df.shape)

    generate_elbow_plot(scaled_df)

    model, labels = run_kmeans(scaled_df)

    distances = centroid_distance(

        model,

        scaled_df

    )

    df["cluster_id"] = labels

    df["distance_from_centroid"] = distances

    print()

    print("Cluster Counts")

    print(df["cluster_id"].value_counts().sort_index())

    df = assign_cluster_names(df)
    profile = cluster_profile(df)
    correlation_heatmap(df)
    outlier_df = detect_outliers(df)
    stats_df = portfolio_statistics(df)
    members = export_cluster_members(df)

    export_results(df)

    print()

    print("=" * 60)

    print("DAY 36 COMPLETED SUCCESSFULLY")

    print("=" * 60)

    print()

    print(f"Companies Clustered : {len(df)}")

    print(f"Clusters Created    : {df['cluster_id'].nunique()}")

    print()

    print("Output Files:")

    print("reports/elbow_plot.png")

    print("output/cluster_labels.csv")

    print("reports/correlation_heatmap.png")

    print("output/cluster_profile.csv")

    print("output/cluster_members.csv")

    print("output/outlier_report.csv")

    print("output/portfolio_stats.csv") 
