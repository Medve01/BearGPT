# BearGPT

BearGPT is a custom chat GPT implementation that leverages Pinecone for long-term memory. This project aims to provide an interactive and engaging AI experience using the latest natural language processing models.
It's a single-user app that I wrote for myself. It's definitely not ready for publishing on the internet, I only run it on my home server that is not public.

## Table of Contents

- [BearGPT](#beargpt)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Dependencies](#dependencies)
    - [Install with Poetry](#install-with-poetry)
  - [Usage](#usage)
    - [Starting the Flask App](#starting-the-flask-app)

## Installation

### Dependencies

Before you proceed, make sure you have the following dependencies installed:

- Python 3.7 or higher
- Poetry (Python dependency management tool)

### Install with Poetry

1. Clone the BearGPT repository by running the following command:

   ```bash
   git clone https://github.com/Medve01/BearGPT.git
   ```

2. Change directory to the cloned repository:

   ```bash
   cd BearGPT
   ```

3. Install the project and its dependencies using Poetry:

   ```bash
   poetry install
   ```

   This will create a virtual environment and install all the required packages in it.

## Usage

### Starting the Flask App

1. To start the Flask app, first activate the virtual environment created by Poetry:

   ```bash
   poetry shell
   ```

3. Chane to the app folder:
   ```bash
   cd beargpt
   ```

4. Run the Flask app:

   ```bash
   flask run
   ```

   The BearGPT Flask app should now be running on `http://127.0.0.1:5000/`. You can interact with the app using your web browser.

That's it! You have successfully installed and started BearGPT. Enjoy interacting with your custom chat GPT implementation powered by Pinecone long-term memory.