# Financial Researcher

This project is a financial researcher crew built using the CrewAI framework. It is designed to research a given company and generate a comprehensive report.

## Project Structure

```
financialresearcher/
├── src/
│   └── financialresearcher/
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       ├── tools/
│       │   └── __init__.py # Assuming tools will be added here
│       ├── crew.py
│       ├── main.py
│       └── __init__.py
├── .gitignore # (Optional) Recommended
├── requirements.txt # (Optional) Recommended
├── .env # (Optional) For API keys
└── README.md
```

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd financialresearcher
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    Assuming you have a `requirements.txt` file with necessary libraries (like `crewai`, `crewai-tools`, `httpx`, `pysbd`, `qdrant-client`, `groq`, etc.):

    ```bash
    pip install -r requirements.txt
    ```

    If you don't have `requirements.txt`, you'll need to install the libraries manually:

    ```bash
    pip install crewai crewai-tools httpx pysbd qdrant-client groq
    # Install any other tools you might be using (e.g., serper-python for Serper)
    ```

4.  **Configure API Keys:**

    If your agents use external APIs (like Groq or Serper), you'll likely need to set up environment variables. Create a `.env` file in the project root and add your API keys:

    ```env
    GEMINI_API_KEY='your_gemini_api_key'
    SERPER_API_KEY='your_serper_api_key'
    # Add any other necessary API keys
    ```

    Make sure your code loads these environment variables (e.g., using `python-dotenv`).

## Usage

1.  **Ensure your virtual environment is active:**

    ```bash
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

2.  **Run the main script:**

    Modify `src/financialresearcher/main.py` to specify the company you want to research.

    ```python
    inputs={
        "company":"The Company You Want to Research"
    }
    ```

    Then, run the script:

    ```bash
    python src/financialresearcher/main.py
    ```

The crew will execute the research and analysis tasks, and the final report should be saved to the location specified in `config/tasks.yaml` (defaulting to `output/report.md`).

## Configuration

-   `src/financialresearcher/config/agents.yaml`: Defines the roles, goals, and backstories for the agents.
-   `src/financialresearcher/config/tasks.yaml`: Defines the tasks, their descriptions, expected output, and assigned agents.

Adjust these files to customize the behavior of the financial researcher crew. 
