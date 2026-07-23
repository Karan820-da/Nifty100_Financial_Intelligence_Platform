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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sqlalchemy import text

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

# Remove unrealistic values
df["return_on_equity_pct"] = df["return_on_equity_pct"].clip(-100, 100)
df["operating_profit_margin_pct"] = df["operating_profit_margin_pct"].clip(-100, 100)
df["debt_to_equity"] = df["debt_to_equity"].clip(0, 20)


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