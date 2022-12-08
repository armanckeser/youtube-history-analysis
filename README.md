# youtube-history-analysis

[![PyPI](https://img.shields.io/pypi/v/youtube-history-analysis?style=flat-square)](https://pypi.python.org/pypi/youtube-history-analysis/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/youtube-history-analysis?style=flat-square)](https://pypi.python.org/pypi/youtube-history-analysis/)
[![PyPI - License](https://img.shields.io/pypi/l/youtube-history-analysis?style=flat-square)](https://pypi.python.org/pypi/youtube-history-analysis/)
[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)


---

**Documentation**: [https://armanckeser.github.io/youtube-history-analysis](https://armanckeser.github.io/youtube-history-analysis)

**Source Code**: [https://github.com/armanckeser/youtube-history-analysis](https://github.com/armanckeser/youtube-history-analysis)

**PyPI**: [https://pypi.org/project/youtube-history-analysis/](https://pypi.org/project/youtube-history-analysis/)

---

See how your YouTube interests evolved over time

## Installation

```sh
python -m venv yt-history-venv
./yt-history-venv/Scripts/activate
pip install youtube-history-analysis
```

## Usage
### Get a YouTube API Key

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Click the project drop-down and select or create the project for which you want to add an API key.
3. Click the hamburger menu and select APIs & Services > Credentials.
4. On the Credentials page, click Create credentials > API key.
5. The API key created dialog displays your newly created API key.

Remember to restrict the API key so that it can only be used with certain websites or IP addresses by clicking the Edit button for the API key and then setting the restrictions in the Key restriction section.
### Get your YouTube History as JSON
1. Visit [Google Takeout](https://takeout.google.com/) and sign in to your Google account.
2. Scroll down to the "YouTube" section and click All data included.
3. Click the Deselect All button and then select the checkbox next to Watch history.
4. Click the Next button at the bottom of the page.
5. On the next page, you can select the file type and delivery method for your takeout. Make sure to select JSON as the file type.
6. Click the Create export button to start the export process.

Once the export is complete, you will receive an email with a link to download your takeout. The downloaded file will be a zip archive containing your YouTube watch history in JSON format.

```sh
python -m youtube_history_analysis $API_KEY --watch-history-file-path $WATCH_HISTORY_JSON_PATH
```

This will create an `outputs` folder with a bunch of `.csv` files and a few `.png` files. Feel free to use the `.csv` file to do your own analysis.

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.9+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [Github project page
 ](https://pages.github.com/) automatically as part each release.

### Releasing

Trigger the [Draft release workflow](https://github.com/armanckeser/youtube-history-analysis/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/armanckeser/youtube-history-analysis/releases) and publish it. When
 a release is published, it'll trigger [release](https://github.com/armanckeser/youtube-history-analysis/blob/master/.github/workflows/release.yml) workflow which creates PyPI
 release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

This project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.
