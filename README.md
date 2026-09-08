# Dynamic-CNN Based DNA Sequence Classification for Viral Genome Prediction

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-Deep%20Learning-orange.svg)](https://www.tensorflow.org/)
[![Bioinformatics](https://img.shields.io/badge/Domain-Bioinformatics-green.svg)](https://www.ncbi.nlm.nih.gov/)

A deep learning approach for viral genomic sequence classification using
a **Hot Matrix representation** and a **Dynamic Convolutional Neural
Network (Dynamic CNN)** designed to process DNA sequences with varying
lengths.

------------------------------------------------------------------------

## Table of Contents

-   [Overview](#overview)
-   [Problem Statement](#problem-statement)
-   [Key Idea](#key-idea)
-   [Dataset](#dataset)
-   [Methodology](#methodology)
    -   [1. FASTA Sequence Processing](#1-fasta-sequence-processing)
    -   [2. Handling Ambiguous
        Nucleotides](#2-handling-ambiguous-nucleotides)
    -   [3. 4-mer Generation](#3-4-mer-generation)
    -   [4. One-Hot Encoding](#4-one-hot-encoding)
    -   [5. Hot Matrix Representation](#5-hot-matrix-representation)
    -   [6. Dynamic CNN](#6-dynamic-cnn)
-   [Model Architecture](#model-architecture)
-   [Training and Evaluation](#training-and-evaluation)
-   [Baseline Models](#baseline-models)
-   [Evaluation Metrics](#evaluation-metrics)
-   [Results](#results)
-   [Key Contributions](#key-contributions)
-   [Data](#data)
-   [Reproducibility](#reproducibility)
-   [Limitations](#limitations)
-   [Future Work](#future-work)
-   [Technologies](#technologies)
-   [Reference](#reference)
-   [Disclaimer](#disclaimer)

------------------------------------------------------------------------

## Overview

DNA sequences contain genetic information that can be analyzed to
identify patterns associated with different organisms, viruses, and
biological conditions.

This project investigates **viral genome classification using deep
learning**. Genomic sequences collected from the **National Center for
Biotechnology Information (NCBI)** are transformed from raw nucleotide
strings into numerical representations and classified using a Dynamic
CNN.

The proposed pipeline is:

``` text
NCBI Genomic Sequences
          |
          v
    FASTA Processing
          |
          v
      Preprocessing
          |
          v
    Overlapping 4-mers
          |
          v
  256-D One-Hot Vectors
          |
          v
      Hot Matrix
          |
          v
     Dynamic CNN
          |
          v
 Viral Genome Classification
```

The study evaluates the proposed model against multiple classical
machine learning and deep learning approaches.

------------------------------------------------------------------------

## Problem Statement

Full viral genome sequences can vary significantly in length.
Conventional CNN architectures generally work with fixed-size inputs,
which can require:

-   truncating longer sequences, or
-   padding shorter sequences.

Such transformations may remove or alter sequence information.

The objective of this project is to develop a CNN-based architecture
that can process genomic sequences of varying lengths while learning
useful local sequence patterns.

The proposed approach combines:

1.  **4-mer-based Hot Matrix representation**
2.  **Convolutional feature extraction**
3.  **Global Average Pooling**
4.  **Dense classification layers**

Global Average Pooling produces a fixed-size representation from
convolutional feature maps regardless of the input sequence length.

------------------------------------------------------------------------

## Key Idea

The central idea is:

> **Represent DNA sequences as overlapping 4-mers, convert the 4-mers
> into one-hot vectors, construct a Hot Matrix, and use a CNN with
> Global Average Pooling to classify variable-length genomic
> sequences.**

The representation and model work together as follows:

``` text
DNA sequence
     |
     v
Overlapping 4-mers
     |
     v
256-dimensional one-hot vectors
     |
     v
2D Hot Matrix
     |
     v
Convolutional feature extraction
     |
     v
Global Average Pooling
     |
     v
Fixed-size representation
     |
     v
Classification
```

------------------------------------------------------------------------

# Dataset

The genomic sequences used in the study were collected from **NCBI** and
stored in FASTA format.

The dataset contains five categories:

  Class                     Number of Sequences
  ----------------------- ---------------------
  COVID-19 / SARS-CoV-2                  30,902
  Dengue                                  2,000
  Hepatitis                               8,311
  MERS                                    1,658
  Influenza                              10,880
  **Total**                          **53,751**

The dataset is highly imbalanced, with COVID-19/SARS-CoV-2 representing
the largest class.

------------------------------------------------------------------------

# Methodology

## 1. FASTA Sequence Processing

The source data is provided in FASTA format.

A FASTA record contains an identifier/metadata line beginning with `>`
followed by the nucleotide sequence.

Example:

``` text
>sequence_identifier
CGATAATCGACTACAT...
```

The nucleotide sequence is extracted and prepared for further
processing.

------------------------------------------------------------------------

## 2. Handling Ambiguous Nucleotides

DNA sequences may contain ambiguous nucleotide symbols such as `N`.

In the study, `N` is treated as an ambiguous nucleotide corresponding to
any of:

``` text
A, C, G, T
```

The preprocessing stage handles these special nucleotide characters
before generating the numerical representation.

------------------------------------------------------------------------

## 3. 4-mer Generation

The DNA sequence is divided into **overlapping subsequences of length
four**, known as 4-mers.

For example:

``` text
CGATAATCGACTACAT
```

produces 4-mers such as:

``` text
CGAT
GATA
ATAA
TAAT
...
```

Because there are four possible nucleotide bases:

``` text
A
C
G
T
```

the total number of possible 4-mers is:

``` text
4^4 = 256
```

Therefore, a dictionary containing all possible 256 4-mers can be
constructed.

Using overlapping 4-mers allows local nucleotide patterns and
dependencies to be represented.

------------------------------------------------------------------------

## 4. One-Hot Encoding

Each 4-mer is mapped to a unique index among the 256 possible 4-mers.

It is then represented using a 256-dimensional binary vector.

For example:

``` text
ACGT -> [0, 0, 0, ..., 1, ..., 0]
```

Only the position corresponding to that particular 4-mer is set to `1`;
all remaining positions are `0`.

Therefore:

``` text
4-mer
  |
  v
256-dimensional binary vector
```

------------------------------------------------------------------------

## 5. Hot Matrix Representation

The one-hot vectors for all consecutive 4-mers in a sequence are
appended to create a two-dimensional matrix.

Conceptually:

``` text
                 256 dimensions
          <------------------------>

4-mer 1   [0 0 0 1 0 0 ... 0]
4-mer 2   [0 0 1 0 0 0 ... 0]
4-mer 3   [0 1 0 0 0 0 ... 0]
4-mer 4   [0 0 0 0 1 0 ... 0]
   ...
```

This produces the **Hot Matrix representation** of the DNA sequence.

The resulting representation provides a structured numerical input
suitable for convolutional neural networks.

> The Hot Matrix representation was adopted from previous work
> referenced by the study; the primary contribution of this project is
> the Dynamic CNN architecture and its evaluation with the
> representation.

------------------------------------------------------------------------

## 6. Dynamic CNN

The proposed model is a convolutional neural network designed to work
with genomic sequences of varying lengths.

A standard CNN may require sequences to be transformed into a common
fixed size. The proposed architecture instead uses **Global Average
Pooling** after convolutional feature extraction.

This produces a fixed-length feature vector from variable-length feature
maps.

``` text
Variable-Length Sequence
          |
          v
     Hot Matrix
          |
          v
      Conv1D
          |
          v
      Max Pool
          |
          v
      Conv1D
          |
          v
      Max Pool
          |
          v
      Conv1D
          |
          v
      Max Pool
          |
          v
Global Average Pooling
          |
          v
   Fixed-size Vector
          |
          v
    Dense + Dropout
          |
          v
     Classification
```

------------------------------------------------------------------------

# Model Architecture

The architecture described in the study consists of:

  Stage   Layer
  ------- ------------------------
  1       Conv1D --- 32 filters
  2       ReLU
  3       Max Pooling
  4       Conv1D --- 64 filters
  5       ReLU
  6       Max Pooling
  7       Conv1D --- 128 filters
  8       ReLU
  9       Max Pooling
  10      Global Average Pooling
  11      Dense Layer
  12      Dropout
  13      Dense Layer
  14      Classification Output

### Convolutional Layers

The number of filters increases progressively:

``` text
32 -> 64 -> 128
```

This allows the network to learn increasingly complex feature patterns
from the genomic representation.

### Max Pooling

Max pooling reduces the spatial/sequence representation while retaining
strong feature activations and reducing computational load.

### Global Average Pooling

Global Average Pooling is the key component that enables the
architecture to handle variable-length feature maps.

Instead of flattening the complete feature map, the model computes an
aggregate value for each feature map:

``` text
Variable-length feature map
            |
            v
Global Average Pooling
            |
            v
Fixed-size feature vector
```

This fixed-size representation can then be passed to dense layers.

### Dense and Dropout Layers

The dense layers transform the extracted representation for
classification, while dropout is used as a regularization mechanism.

------------------------------------------------------------------------

# Training and Evaluation

The proposed method uses **sequence-by-sequence preprocessing and
training**.

The sequence is processed on the fly:

``` text
DNA Sequence
     |
     v
Preprocessing
     |
     v
4-mer Generation
     |
     v
Hot Matrix
     |
     v
Dynamic CNN
     |
     v
Weight Update
```

The same preprocessing pipeline is used during testing and evaluation.

The study evaluates the models using **4-fold cross-validation**.

------------------------------------------------------------------------

# Baseline Models

The Dynamic CNN was compared with multiple machine learning and deep
learning approaches.

## Deep Learning Models

-   CNN
-   MLP
-   RNN
-   Dynamic CNN

## Classical Machine Learning Models

-   Decision Tree
-   Support Vector Machine (SVM)
-   Random Forest
-   Logistic Regression
-   K-Nearest Neighbors (KNN)
-   Multinomial Naive Bayes
-   XGBoost
-   Extra Trees
-   Gradient Boosting
-   LightGBM

For the additional classical machine learning models, the study uses a
**16-mer counting representation** followed by feature selection to
reduce the computational requirements.

------------------------------------------------------------------------

# Evaluation Metrics

Eight evaluation metrics are used in the study:

-   Accuracy
-   Precision
-   Sensitivity
-   Specificity
-   F1 Score
-   Matthews Correlation Coefficient (MCC)
-   Area Under the ROC Curve (AUROC)
-   Area Under the Precision-Recall Curve (AUPRC)

These metrics provide a broader evaluation than accuracy alone,
particularly for an imbalanced dataset.

------------------------------------------------------------------------

# Results

The proposed Dynamic CNN reports the following average results across
the evaluation folds:

  Metric            Dynamic CNN
  ------------- ---------------
  Sensitivity       **99.928%**
  Specificity       **24.766%**
  Precision         **99.928%**
  Accuracy          **99.928%**
  F1 Score          **99.928%**
  AUROC             **99.986%**
  AUPRC             **99.946%**
  MCC             **99.886%**\*

\* The paper's Table XIV prints the MCC average as `9.886`; based on the
individual fold values reported in the same table, this appears to be a
formatting/typographical issue. The README reports the value as
approximately `99.886%`.

### Comparison with Previous CNN

The previous CNN model reported:

  Metric        Previous CNN     Dynamic CNN
  ----------- -------------- ---------------
  Accuracy            73.50%     **99.928%**
  Precision           91.28%     **99.928%**
  F1 Score            66.04%     **99.928%**
  AUROC               80.15%     **99.986%**
  AUPRC               83.60%     **99.946%**
  MCC                 52.11%   **\~99.886%**

The study reports a substantial improvement over the previous CNN and
the other evaluated models.

------------------------------------------------------------------------

# Model Comparison

Selected average accuracy values reported in the study:

  Model                          Accuracy
  ------------------------- -------------
  CNN                              73.50%
  Decision Tree                    62.50%
  MLP                              78.00%
  RNN                              69.00%
  SVM                              50.00%
  Random Forest                    58.41%
  Logistic Regression              64.34%
  KNN                              67.20%
  Multinomial Naive Bayes          69.19%
  XGBoost                          63.87%
  Extra Trees                      59.06%
  Gradient Boosting                64.00%
  LightGBM                        62.292%
  **Dynamic CNN**             **99.928%**

------------------------------------------------------------------------

# Key Contributions

1.  **Dynamic genomic sequence classification**

    Developed a CNN-based architecture intended to process genomic
    sequences with varying lengths.

2.  **Hot Matrix-based input representation**

    Used overlapping 4-mers and 256-dimensional one-hot vectors to
    construct a structured representation of DNA sequences.

3.  **Global Average Pooling**

    Used Global Average Pooling to transform variable-length
    convolutional feature maps into fixed-size feature representations.

4.  **Comprehensive comparison**

    Compared the proposed model with multiple classical machine learning
    and deep learning approaches.

5.  **Multi-metric evaluation**

    Evaluated the models using eight classification metrics, including
    MCC, AUROC, and AUPRC.

------------------------------------------------------------------------

# Data

The raw genomic dataset is not included in this repository.

The study uses full-genome sequences collected from NCBI. Users
reproducing the experiments should obtain the appropriate genomic
sequences from the original source and prepare them according to the
methodology described above.

The dataset contains:

``` text
COVID-19 / SARS-CoV-2 : 30,902
Dengue                :  2,000
Hepatitis             :  8,311
MERS                  :  1,658
Influenza             : 10,880
--------------------------------
Total                 : 53,751
```

------------------------------------------------------------------------

# Reproducibility

The experimental pipeline can be summarized as:

``` text
FASTA Files
    |
    v
Extract Genomic Sequences
    |
    v
Handle Ambiguous Nucleotides
    |
    v
Generate Overlapping 4-mers
    |
    v
Create 256-D One-Hot Vectors
    |
    v
Construct Hot Matrix
    |
    v
Dynamic CNN
    |
    v
4-Fold Cross-Validation
    |
    v
Calculate Evaluation Metrics
```

For classical machine learning baselines:

``` text
FASTA Sequences
    |
    v
16-mer Counting
    |
    v
Feature Selection
    |
    v
Classical ML Model
    |
    v
4-Fold Cross-Validation
```

Exact hyperparameters and implementation details should be taken from
the corresponding source code when reproducing the original experiment.

------------------------------------------------------------------------

# Limitations

Although the proposed model reports very high performance on the
evaluated dataset, several limitations should be considered.

### Class Imbalance

The dataset is highly imbalanced. COVID-19/SARS-CoV-2 sequences account
for a substantially larger portion of the dataset than MERS and Dengue
sequences.

### Sequence Similarity

The study does not provide a detailed analysis of duplicate or highly
similar genomic sequences across the evaluation splits.

For genomic classification, similarity-aware splitting can be important
because closely related sequences may otherwise appear in both training
and evaluation data.

### Generalization

The reported results are based on the dataset and evaluation methodology
used in the study. Additional evaluation on independent external
datasets would be required to establish generalization.

### Clinical Interpretation

This project performs **genomic sequence classification**. The reported
classification performance should not be interpreted as clinical
diagnostic accuracy.

------------------------------------------------------------------------

# Future Work

Potential extensions include:

-   Duplicate and near-duplicate sequence removal
-   Similarity-aware train/test splitting
-   Evaluation on independent external genomic datasets
-   Class-balancing techniques
-   Ablation studies with different k-mer sizes
-   Comparison of 4-mer, 5-mer, 6-mer, and larger representations
-   Transformer-based genomic sequence models
-   Attention-based architectures
-   Explainability methods for identifying influential genomic regions
-   Hyperparameter optimization
-   Computational efficiency and inference-time analysis
-   Robustness testing across different genomic datasets

------------------------------------------------------------------------

# Technologies

-   **Python**
-   **TensorFlow / Keras**
-   **Convolutional Neural Networks**
-   **Conv1D**
-   **Global Average Pooling**
-   **One-Hot Encoding**
-   **k-mer Analysis**
-   **Machine Learning**
-   **Deep Learning**
-   **Bioinformatics**
-   **Genomic Sequence Processing**

------------------------------------------------------------------------

# Reference

This project is based on the research paper written as part of univerity research work:

> **Dynamic-CNN based DNA sequence classification for efficient Viral
> Genome Prediction**

The study compares the proposed Dynamic CNN against multiple machine
learning and deep learning models for viral genomic sequence
classification.

### Related Work

The methodology builds upon previous research in:

-   Viral genome prediction
-   DNA sequence classification
-   CNN-based genomic analysis
-   k-mer representations
-   Deep learning for bioinformatics
-   Variable-length genomic feature extraction

------------------------------------------------------------------------

# Disclaimer

This repository implements a research approach for **viral genomic
sequence classification**.

The reported performance values correspond to the experimental setup and
dataset described in the associated study. They should not be
interpreted as clinical diagnostic accuracy, medical advice, or evidence
that the model can independently diagnose disease in clinical settings.
