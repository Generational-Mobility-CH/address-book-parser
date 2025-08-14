# Generate A Panel Dataset from old Swiss Address Books
![Built with](https://img.shields.io/badge/Built%20With-Python-blue)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

This project processes Swiss address books into a panel dataset containing person per year that can be used for academical research.

Books so far processed:
- [x] 1877 - 1954: [Stadt Basel](https://dls.staatsarchiv.bs.ch/records/hierarchy/1225845?context=%2Frecords%2F1225845)
- [ ] 1859 - 1975: [Stadt Zürich](https://zop.zb.uzh.ch/collections/9e5087c3-e5f8-4b76-a106-3b5fc830a0f7?spc.page=1&query=Adressbuch%20der%20Stadt%20Z%C3%BCrich%20und%20Umgebung&spc.sf=dc.title&spc.sd=ASC)

The pipeline consists of the following modules:
1. **pages_downloader**: Download the relevant chapter containing the residents register from the address books website.
2. **pages_preprocessor**: Cut the address book pages colums into single pages, so the OCR can process them more easily.
3. **Text Extraction**: Extract the text from the scanned address book pages with [ChronoMiner](https://github.com/Paullllllllllllllllll/ChronoMiner), provided by @Paullllllllllllllllll.
4. **persons_data_processor**: Parse the extracted text from step 3. and save the information into a SQL database that contains all the found person's names, address and job.
5. **panel_data**: Create a panel dataset from the SQL database that can be used for academic research.

All relevant data is stored under the `data/` directory.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Project Setup
- [install uv](https://docs.astral.sh/uv/getting-started/installation/)
- [install pre-commit](https://pre-commit.com/#installation)
- [install the git hook scripts](https://docs.astral.sh/uv/getting-started/installation/) used in the project
- install and enable the [MyPy plugin for PyCharm](https://plugins.jetbrains.com/plugin/11086-mypy)

- install project dependencies by running:
```bash
uv pip install
```

### Running the tests

In PyCharm - right-click on the '/test' folder of the module's tests you want to run and select "Run Tests" to execute all the tests.

## License

TODO: This project is licensed under the _XXX_ License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

TODO:
- Thank everyone who provided data...
- ... and helped in building this project

![Built at the Sociology Department UZH](https://img.shields.io/badge/Built%20at%20the%20Sociology%20Department%20at%20UZH-blue)