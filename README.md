# 🌿 Eco Design

## 📝 Description

Eco Design is a toolkit for analyzing the ecodesign of websites, incorporating:
- 🚀 Google PageSpeed Insights
- 🌍 Ecoindex
- 🔍 Network Request Analysis

### 🚀 Google PageSpeed Insights

Utilizes the Google PageSpeed Insights API to evaluate website performance.
[API Documentation](https://developers.google.com/speed/docs/insights/v5/get-started?hl=fr)

### 🌍 Ecoindex

Employs Playwright to scrape websites and calculate their Ecoindex score.
Adapted from [ecoindex_python](https://github.com/cnumr/ecoindex_python).

### 🔍 Network Request Analysis

Leverages Playwright to examine network requests made by the website.

## 🏗️ Project Structure

### Core Components

#### Google Insight

```python
from app.core.insight.google_insight import MobileInsight, DesktopInsight

url = "https://www.alextraveylan.fr"

# Mobile Insight
mobile_insight = MobileInsight(url)
print(mobile_insight.get_result())
# Output: performance=85 accessibility=100 best_practices=96 seo=100 ...

# Desktop Insight
desktop_insight = DesktopInsight(url)
print(desktop_insight.get_result())
# Output: performance=99 accessibility=100 best_practices=100 seo=100 ...
```

#### Ecoindex

```python
from app.core.eco_index.scraper import EcoindexScraper


url = "https://www.alextraveylan.fr"

eco_index = asyncio.run(EcoindexScraper(url=url).get_page_analysis())
print(eco_index)
# Output: width=1920 height=1080 url='https://www.alextraveylan.fr/' ...
```

#### Network Requests

```python
from app.core.inspect_network.count_requests import InspectNetwork

url = "https://www.alextraveylan.fr"

inspect = InspectNetwork(url=url)
print(inspect.get_result())
# Output: total=32 js=19 css=1
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository
2. Set up a virtual environment:
   ```sh
   python -m venv env
   ```
3. Install dependencies:
   ```sh
   pip install -r dev_requirements.txt
   ```
4. Install Playwright browsers:
   ```sh
   playwright install
   ```

### Usage

Run the application:
```sh
python app/main.py
```

Execute tests:
```sh
pytest
```

## 🛠️ Development

This project is configured for Visual Studio Code with Python extension settings for formatting and linting. Configuration files are located in the `.vscode` directory.

## 🐳 Docker

Build the Docker image:
```sh
docker build -t eco-design .
```

Run the container:
```sh
docker run -p 80:80 eco-design
```

## 🔄 Continuous Integration

GitHub Actions workflow is set up for CI, running tests and security checks on push and pull request events to the main branch.

## 📊 Logging

Logging is configured using Python's built-in logging module. Configuration file: `app/adapter/logger/config_log.json`.

## 📦 Packaging

Create the package:
```bash
python setup.py sdist bdist_wheel
```

Install the package:
```bash
pip install dist/ecodesign-0.1-py3-none-any.whl
```
Note: Replace `0.1` with the current version number.

## 🤝 Contributing

Contributions are welcome! Please submit a pull request or create an issue to discuss proposed changes.

## 📄 License

This project is licensed under the [MIT License](LICENSE).