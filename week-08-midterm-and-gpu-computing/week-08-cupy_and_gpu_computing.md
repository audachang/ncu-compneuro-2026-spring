# Week 8: GPU Computing with CuPy

This week, we'll be exploring how to leverage the power of GPUs to accelerate our scientific computing tasks. We'll be using CuPy, a NumPy/SciPy-compatible array library for GPU-accelerated computing with Python.

[Shared Google Drive Folder](https://drive.google.com/drive/folders/1-z9SflY4WUgVK0YSwRlRrpF8PGsRGXrB?usp=sharing)


## What is CuPy?

CuPy is an open-source library that allows you to perform NumPy and SciPy operations on a GPU. This can lead to significant performance improvements for a wide range of applications, including machine learning, image processing, and scientific simulations.

## Key Features

* **NumPy/SciPy Compatibility:** CuPy provides a familiar interface for those who are already comfortable with NumPy and SciPy.
* **Easy to Use:** With just a few minor code changes, you can start running your existing NumPy/SciPy code on a GPU.
* **High Performance:** CuPy is built on top of NVIDIA's CUDA platform, which allows for highly parallelized computations on the GPU.

## Getting Started

To get started with CuPy, you'll need to have a CUDA-enabled GPU and have the CUDA Toolkit installed. You can then install CuPy using pip:

```bash
pip install cupy-cuda11x
```

## Example

Here's a simple example of how to use CuPy to perform a matrix multiplication on the GPU:

```python
import cupy as cp
import numpy as np

# Create two random matrices on the CPU
x_cpu = np.random.rand(1000, 1000)
y_cpu = np.random.rand(1000, 1000)

# Move the matrices to the GPU
x_gpu = cp.asarray(x_cpu)
y_gpu = cp.asarray(y_cpu)

# Perform the matrix multiplication on the GPU
z_gpu = cp.dot(x_gpu, y_gpu)

# Move the result back to the CPU
z_cpu = cp.asnumpy(z_gpu)
```
