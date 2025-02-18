# Web Scraping and Data Cleaning Project

This project aims to scrape web pages from any given website, extract relevant data, and clean it to make it suitable for fine-tuning the Gemma:2B model by Google. The data is cleaned by removing redundant sentences, white spaces, and any unnecessary symbols, ensuring high-quality input for the AI model.

## Features

- **General Web Scraping**: The script can scrape any website and extract data based on predefined CSS selectors.
- **Fallback Selectors**: If specific selectors are not provided, the script uses fallback selectors to ensure data extraction.
- **Data Cleaning**: The scraped data is cleaned by removing redundant sentences, extra white spaces, and unnecessary symbols.
- **Duplicate Removal**: The script removes duplicate sentences to ensure unique and high-quality data.

## Requirements

- Python 3.x
- Selenium
- Microsoft Edge WebDriver

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/web-scraping-project.git
    cd web-scraping-project
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv myenv
    ```

3. **Activate the virtual environment**:
    - On Windows:
        ```sh
        myenv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source myenv/bin/activate
        ```

4. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Download and install Microsoft Edge WebDriver**:
    - Download the WebDriver from the [official site](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).
    - Extract the downloaded file and place the `msedgedriver.exe` in a `Driver` directory within your project folder.

## Usage

1. **Update the base URL**:
    - Open `source.py`.
    - Modify the `base_url` variable to the website you want to scrape:
        ```python
        base_url = "https://www.example.com/"
        ```

2. **Run the script**:
    ```sh
    python source.py
    ```

3. **Output**:
    - The scraped and cleaned data will be saved to `output.json`.

## Code Overview

### `source.py`

- **setup_webdriver(driver_path, headless)**:
  Sets up the WebDriver with options to run in headless mode if specified.

- **scrape_page(driver, url, selectors)**:
  Scrapes data from a single page based on given CSS selectors.

- **get_all_links(driver, base_url)**:
  Collects all internal links from the given base URL.

- **scrape_with_fallbacks(driver, url)**:
  Performs scraping using fallback selectors if specific selectors are not provided.

- **clean_data(website_data)**:
  Cleans the scraped data by removing redundant sentences, extra white spaces, unnecessary symbols, and duplicate sentences.

- **main(output_file, base_url, driver_path, headless, delay)**:
  The main function to set up the WebDriver, scrape the website, clean the data, and save it to a JSON file.

## Example Output

```json
{
    "https://www.example.com/": {
        "source_link": "https://www.example.com/",
        "about_me": [
            "Example text 1.",
            "Example text 2."
        ],
        "education": [
            "Education detail 1.",
            "Education detail 2."
        ],
        "work_experience": [
            "Work experience detail 1.",
            "Work experience detail 2."
        ],
        "skills": [
            "Skill 1.",
            "Skill 2."
        ]
    }
}

