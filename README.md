# Entity Resolution System

## Problem Statement

The objective of this assignment is to build an **Entity Resolution System** to identify and cluster similar company names.
Each cluster should have:

* One **Parent (Canonical Name)**
* Multiple **Child company names**

This helps in removing duplicates and standardizing company names for business use cases such as reporting and analytics.

---

## Input Data

As per the assignment, expected input fields were:

* Company Name
* Origin Country
* Destination Country
* HS Code

### Data Reality

The provided dataset contained only the following columns:

* `buyer-supplier` → Company Name
* `parent_canonical_name` → (Empty column)

Since country and HS code were not available in the dataset, clustering was performed **only on company name similarity**.

---

## Dataset Summary

* Total Records: **802,394**
* Data Type: **Text (Company Names)**
* Nature:

  * Multiple name variations
  * Special characters
  * Suffix differences (Ltd, GmbH, Co, Inc)
  * Spacing and formatting inconsistencies

This makes it a perfect use case for **Entity Resolution**.

---

## Approach

### 1. Data Cleaning

* Converted names to lowercase
* Removed special characters
* Normalized extra spaces

### 2. Blocking Technique

To reduce unnecessary comparisons:

* Used **first word of company name** as a block key
* Compared names only within the same block

This significantly improved performance.

### 3. Fuzzy Matching

* Used **RapidFuzz** library
* Applied `token_sort_ratio`
* Similarity threshold: **90%**

If similarity ≥ 90%, records are placed in the same cluster.

### 4. Parent Selection

For each cluster:

* The **longest company name** is selected as
  **Parent Canonical Name**

---

## Output

Final output file:

```
output/clusters_final.csv
```

### Columns

| Column Name    | Description               |
| -------------- | ------------------------- |
| Cluster_ID     | Unique cluster number     |
| Parent_Company | Canonical company name    |
| Child_Company  | All related name variants |

---

## Validation

Clustering was validated using:

1. Programmatic checks

   * Total rows match input
   * Unique cluster count verified

2. Manual sampling

   * Verified similar company variants
   * Checked parent selection logic

---

## How to Run

### 1. Activate Environment

```bash
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install pandas rapidfuzz openpyxl
```

### 3. Run Script

```bash
python src/entity_resolution.py
```

Output will be generated inside:

```
output/
```

---

## Scalability

For large-scale production:

* This logic can be deployed on

  * Apache Spark
  * Databricks
  * Distributed environments

Local execution was used only for demonstration and validation.

---

## Key Highlights

* Production-style pipeline
* Blocking optimization
* Fuzzy matching logic
* Versioned outputs
* Manual + programmatic validation

---

## Conclusion

This project successfully demonstrates an **Entity Resolution system** that:

* Groups similar company names
* Generates canonical parent names
* Produces clean, structured output
* Follows real industry practices

---

## Future Improvements

* Include country & HS code when available
* Deploy on Spark for large-scale processing
* Build API for real-time matching

---

**Thank you!**
