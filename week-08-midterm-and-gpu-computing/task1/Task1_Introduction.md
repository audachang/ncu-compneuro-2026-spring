# Fundamentals of Accelerated Data Science

This document provides an introduction to the **Task 1** materials found in the `gpu-accelerated-data-science/task1` directory. These Jupyter notebooks guide you through the foundations of using NVIDIA RAPIDS to accelerate data science workflows on the GPU.

## Overview

The "Fundamentals of Accelerated Data Science" workshop demonstrates how to migrate standard data science workflows (Pandas, Scikit-Learn, NetworkX) to the GPU using the RAPIDS ecosystem (cuDF, cuML, cuGraph). The focus is on achieving massive speedups with minimal code changes.

## Notebook Contents

### 1. Introduction & Setup
**File:** `1-00_introduction.ipynb`

An introduction to the JupyterLab environment and the NVIDIA GPU resources available. Covers basic magic commands and checking GPU status with `nvidia-smi`.

### 2. Data Manipulation with cuDF
**File:** `1-02_data_manipulation(3).ipynb`

This notebook represents the core of the transition from CPU to GPU. It introduces **cuDF**, the GPU-accelerated equivalent of Pandas.

**Key Concepts:**
*   **cuDF vs Pandas:** Understanding the API similarities and performance differences.
*   **Data Loading:** Reading CSVs efficiently into GPU memory.
*   **Basic Operations:** Indexing, slicing, filtering, and creating new columns on the GPU.
*   **Vectorization:** Leveraging GPU cores for massive parallel processing of column operations.

### 3. Memory Management
**File:** `1-03_memory_management.ipynb`

Understanding how GPU memory works is critical for performance. This notebook covers the RAPIDS Memory Manager (RMM) and best practices for allocation.

**Key Concepts:**
*   **GPU Memory Architecture:** High bandwidth but limited capacity compared to RAM.
*   **RMM (RAPIDS Memory Manager):** Efficiently managing pool allocations to avoid fragmentation.

### 4. Interoperability
**File:** `1-04_interoperability.ipynb`

RAPIDS allows zero-copy data exchange between different libraries. This notebook demonstrates how to move data between cuDF, PyTorch, and other libraries using the CUDA Array Interface and DLPack.

### 5. Grouping and Aggregation
**File:** `1-05_grouping.ipynb`

Covers "Split-Apply-Combine" strategies on the GPU. GroupBy operations are often the most computationally intensive part of ETL, and GPUs excel here.

### 6. Data Visualization
**File:** `1-06_data_visualization.ipynb`

Explores how to visualize large datasets. Since transferring millions of points to the CPU for plotting is slow, this notebook introduces GPU-accelerated visualization techniques (likely involving cuxfilter or integration with GPU-aware plotting libraries).

### 7. Efficient ETL Pipelines
**File:** `1-07_etl.ipynb`

Putting it all together into an End-to-End Extract-Transform-Load pipeline. Demonstrates a full workflow cleaning and preparing data for training.

### 8. Alternative Frameworks
**File:** `1-08_cudf-polars.ipynb`

A comparison or integration guide featuring **Polars**, a fast multi-threaded DataFrame library, and how it fits into the accelerated ecosystem alongside cuDF.

### 9. Scaling with Dask
**File:** `1-09_dask-cudf.ipynb`

When data exceeds the memory of a single GPU, **Dask** is used to distribute the workload. This notebook covers `dask-cudf` for multi-GPU or multi-node dataframes.

**Key Concepts:**
*   **Distributed Computing:** Partitioning dataframes across devices.
*   **Lazy Evaluation:** Building computation graphs before execution.

## Helpful Extension Links

### Libraries & Documentation
*   [RAPIDS AI Homepage](https://rapids.ai/)
*   [cuDF Documentation](https://docs.rapids.ai/api/cudf/stable/)
*   [Dask-cuDF Documentation](https://docs.rapids.ai/api/dask-cudf/stable/)
*   [RAPIDS Memory Manager (RMM)](https://github.com/rapidsai/rmm)

### Further Reading
*   [10 Minute Guide to cuDF](https://docs.rapids.ai/api/cudf/stable/user_guide/10min/)
*   [Dask for Parallel Computing](https://dask.org/)
*   [Accelerated Data Science on NVIDIA GPUs (NVIDIA Developer)](https://developer.nvidia.com/accelerated-data-science)
