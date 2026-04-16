# ShopSense: Curated Fashion Engine

ShopSense is an AI-powered retail agent that provides hyper-personalized clothing and fashion recommendations. Built as a Streamlit application, it combines deterministic ranking algorithms with advanced Large Language Model (LLM) reasoning to offer a premium, curated shopping experience.

## Overview

The application features a hybrid architecture:
- **Deterministic Logic:** Fetches, filters, and scores products using specific user styling preferences, local area trends, social network influence (peer purchases), and upcoming events in the user's vicinity.
- **LLM Reasoning:** Generates a personalized natural language explanation detailing exactly *why* certain products were recommended, tailored to the individual.

## Project Structure

- **`main.py`**: The Streamlit entry point that orchestrates the overall dashboard and user interface.
- **`agent.py`**: The core AI orchestration logic that ties together backend tools to fetch, rank, and summarize product recommendations.
- **`core/`**: Core utilities including LLM API interactions (`llm.py`) and user profile retrieval (`user_profile.py`).
- **`data/`**: Contains the foundational mock datasets (users, products, events, sales trends, purchase history).
- **`prompts/`**: Stores system instructions and instructions given to the LLM backend.
- **`tools/`**: Handles specialized backend tasks such as event filtering, trends analysis, catalog search, peer insight generation, and product scoring.
- **`ui/`**: Houses all Streamlit frontend layouts and custom CSS styling for a robust dashboard presentation.

## Running Locally

To run the application, install the dependencies from your virtual environment and start the Streamlit server:

```bash
streamlit run main.py
```
