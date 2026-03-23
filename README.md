

# PostgreSQL 1 Million Row Benchmark 🚀

A Python-based simulator to stress-test PostgreSQL and measure the exact millisecond impact of B-Tree indexing on a massive dataset. 

This project was built to move beyond the textbook definitions of database performance and actually measure the raw latency differences between **Full Table Scans** and **Index Scans** using high-resolution Python timers.

## 🧠 The Experiment

When querying small tables, databases return results instantly. But what happens at scale? This script does the following:
1. Generates exactly **1,000,000 rows** of dummy user data using PostgreSQL's native `generate_series()`.
2. Runs a baseline query (`SELECT * FROM users WHERE age = 25;`) in a tight loop to measure the latency of a **Full Table Scan**.
3. Dynamically creates a **B-Tree Index** on the target column.
4. Re-runs the query in a loop of 10,000 iterations to measure the optimized latency.

*Note: Queries are run in loops of up to 10,000 iterations to dilute OS-level background noise (micro-stutters) and network overhead, revealing the true average execution time of the database engine.*

## 📋 Prerequisites

To run this locally, you will need:
* **Python 3.x** installed.
* **PostgreSQL** installed and running on your local machine (Default port: `5432`).
* A GUI like **pgAdmin** (optional, but helpful for setup).

## 🚀 Quick Start Setup

### 1. Database Setup
Open pgAdmin (or `psql` command line) and create a new, empty database for the test:
```sql
CREATE DATABASE db_perf_project;


Medium Link: 