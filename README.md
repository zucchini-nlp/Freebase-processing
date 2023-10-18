# Freebase Processing and Entity Search

Welcome to the Freebase Processing repository! This repository houses a powerful Python toolset for processing Freebase data dumps and constructing a Lucene index for efficient entity search. This README will guide you through the process, from acquiring the Freebase data to performing seamless entity searches.

## Introduction

[Freebase](https://developers.google.com/freebase) is a vast knowledge base that provides rich, structured data about a wide range of entities. This repository enables you to process Freebase data and build a Lucene index that allows you to search for entities efficiently.

## Prerequisites

Before you dive into this repository, ensure you have the following prerequisites in place:

- **Freebase Data Dump**: Download the latest official data dump of Freebase from [here](https://developers.google.com/freebase).

- **Python and Pip**: Make sure you have Python and Pip installed on your system.

- **Lupyne**: Lupyne is a Python extension for accessing Java Lucene. Install it using:

```bash
pip install lupyne
```

- **PyLucene (Optional)**: If you prefer to work with PyLucene directly, follow the installation instructions on the official page.

- **Docker (Optional)**: If you'd like to work with Docker, you can build a Docker image with Lucene by running:

```bash
docker pull coady/pylucene .
docker run -it --rm -v $PWD:/usr/src coady/pylucene /bin/bash
```

## Installation
Follow these steps to set up your environment and begin processing Freebase data:

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/Freebase-processing.git
cd Freebase-processing
Download the Freebase data dump as mentioned in the Prerequisites.
```

Configure your environment with the necessary packages as described in Prerequisites.

## Usage
With your environment set up, you can now process Freebase data and perform entity searches:

Build the Lucene index using the provided script:

```bash
python build_lucene_index.py
```

Search for entities in the constructed index. You can specify the entities you want to search for, separated by semicolons:

```bash
python search_index.py --entities="Mona Lisa;Paris;Louvre"
```

This repository empowers you to efficiently explore the vast knowledge contained within Freebase, providing a foundation for various knowledge retrieval and data enrichment projects.
