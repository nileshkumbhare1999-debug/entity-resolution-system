"""
Entity Resolution - Full Dataset
Purpose: Cluster similar company names
"""

import pandas as pd
import re
from rapidfuzz import fuzz
from datetime import datetime


# ---------------- CONFIG ----------------

INPUT_FILE = "data/sample_for_clustring.xlsx"

timestamp = datetime.now().strftime("%Y%m%d_%H%M")
OUTPUT_FILE = f"output/clusters_{timestamp}.csv"

SIMILARITY_THRESHOLD = 90


# ---------------- FUNCTIONS ----------------

def clean_name(name):
    """
    Normalize company name
    """
    if pd.isna(name):
        return ""

    name = name.lower()
    name = re.sub(r"[^a-z0-9 ]", " ", name)
    name = re.sub(r"\s+", " ", name).strip()

    return name


def create_block(name):
    """
    Blocking to reduce comparisons
    Using first word
    """
    if name:
        return name.split(" ")[0]
    return ""


# ---------------- MAIN LOGIC ----------------

def main():

    print("Loading dataset...")
    df = pd.read_excel(INPUT_FILE)

    print("Cleaning company names...")
    df["clean_name"] = df["buyer-supplier"].apply(clean_name)

    print("Creating blocks...")
    df["block"] = df["clean_name"].apply(create_block)

    visited = set()
    clusters = []

    print("Clustering started...")

    for block, block_df in df.groupby("block"):

        index_list = block_df.index.tolist()

        for i in index_list:

            if i in visited:
                continue

            base_name = df.loc[i, "clean_name"]

            current_cluster = [i]
            visited.add(i)

            for j in index_list:

                if j in visited:
                    continue

                candidate_name = df.loc[j, "clean_name"]

                score = fuzz.token_sort_ratio(
                    base_name,
                    candidate_name
                )

                if score >= SIMILARITY_THRESHOLD:
                    current_cluster.append(j)
                    visited.add(j)

            clusters.append(current_cluster)

    print("Preparing final output...")

    output_rows = []

    for cluster_id, group in enumerate(clusters, start=1):

        original_names = df.loc[group, "buyer-supplier"].tolist()

        # Parent = longest name
        parent_name = max(original_names, key=len)

        for child in original_names:
            output_rows.append({
                "Cluster_ID": cluster_id,
                "Parent_Company": parent_name,
                "Child_Company": child
            })

    result_df = pd.DataFrame(output_rows)
    result_df.to_csv(OUTPUT_FILE, index=False)

    print("Process completed successfully!")
    print("Output file:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
