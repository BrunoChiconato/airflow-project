# Introduction

I enrolled in *“Apache Airflow: The Hands-On Guide”*, an A-to-Z course taught by **Marc Lamberti**, **Head of Customer Education at Astronomer**, and I mastered how to programmatically author, schedule, and monitor workflows with Airflow’s TaskFlow API, operators, executors, and integrations.

## Course Examples & Exercises

This folder (`airflow-project/course/`) contains all the hands-on examples and exercises from the course. Here you’ll explore Airflow fundamentals, end-to-end pipelines, TaskFlow API patterns, custom operators, dataset-triggered scheduling, and testing strategies—all powered by the Astro CLI and Docker.

> **Note:** This is an internal README for the `course/` directory. The repository root hosts the production project; this folder holds only the course material.

## Table of Contents

- [Highlights](#highlights)
- [Prerequisites](#prerequisites)
- [Setup & Quick Start](#setup--quick-start)
- [Examples & Usage](#examples--usage)
- [Directory Structure](#directory-structure)

## Highlights

- **Airflow Fundamentals:** scheduler, webserver & metadata DB interactions
- **Stock Market Data Pipeline:** HTTP, Spark, Hadoop & Slack integrations
- **DAG Design:** timezones, catchup, folder structure, subDAGs, cross-DAG dependencies & deadlock avoidance
- **Executors:** Local & Celery setups, specialized workers, node-failure handling
- **Deploy:** AWS EKS cluster with Rancher for cloud-based KubernetesExecutor runs
- **Templating & Advanced Patterns:** Jinja templates, dynamic DAGs, SubDAGs & deadlocks
- **Dataset-Triggered Scheduling:** launch DAG runs via Airflow Datasets
- **Monitoring:** Elasticsearch & Grafana dashboards
- **Security:** RBAC, authentication, password policies & data encryption
- **Testing:** unit tests (`pytest`) and DAG validation

## Prerequisites

- **Python** ≥ 3.8
- **Astro CLI** installed and authenticated (see [Astronomer docs](https://www.astronomer.io/docs/astro/cli/install-cli))
- **Docker & Docker Compose** running

## Setup & Quick Start

1. **Clone the repo** (if not already):
    ```bash
    git clone https://github.com/BrunoChiconato/airflow-project.git
    cd airflow-project/course
    ```

2. **Start Airflow locally** (Astro CLI will build images and spin up services):

    ```bash
    astro dev start
    ```

3. **Access the Airflow UI** at `http://localhost:8080`.

4. **Stop the environment** when you’re done:

    ```bash
    astro dev stop
    ```

## Examples & Usage

### 1. `ecom.py` – Dataset-Triggered DAG

* A simple DAG using an `EmptyOperator`, configured with an outlet dataset.
* Purpose: demonstrate scheduling via Airflow Datasets.
* It runs after the `extractor` DAG completes, but has no other logic.

### 2. `extractor.py` – Cocktail Data Workflow

This DAG showcases:

* **Custom Tasks & Operators:**

  * `get_cocktail` fetches cocktail JSON and writes to a Dataset.
  * TaskGroup `checks` runs `_check_size` and `_validate_cocktail_fields` in sequence.
* **Branching Logic:**

  * `branch_cocktail_type` reads the dataset and routes to `alcoholic_drink` or `non_alcoholic_drink`.
* **Callbacks & Retry Policies:**

  * `on_failure_callback` handlers for DAG and per-task failures.
  * Exponential backoff, max retry delays, and trigger rules.
* **Cleanup Task:**

  * `clean_data` removes the dataset file when downstream succeeds.

Run or test dags manually:

```bash
# Test a single dag
astro dev run dags test extractor 2025-01-01
```

> See `include/extractor/` for callback functions, datasets definitions, and task implementations.

### 3. Tests

* **Run all Tests:**

  ```bash
  astro dev pytest --verbosity debug
  ```

## Directory Structure

```
course/
├── .astro/
├── dags/
│   ├── .airflowignore
│   ├── ecom.py
│   └── extractor.py
├── include/
│   └── extractor/
│       ├── callbacks.py
│       ├── datasets.py
│       └── tasks.py
├── plugins/
├── tests/
│   ├── dags/
│   │   └── test_dag_example.py
│   └── unit_tests/
│       └── test_check_size.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── packages.txt
├── requirements.txt
└── README.md
```
