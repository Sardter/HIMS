# Project Setup and Launch Instructions

This guide walks you through setting up a Python virtual environment, installing all the required global dependencies, and running both the FastAPI backend and the Streamlit frontend from their respective directories. All dependencies are managed by a single `requirements.txt` file located at the project root.

## Prerequisites

- **Python 3.9+** (or your preferred Python 3.x version)
- **pip** (usually included with Python)
- **virtualenv** (optional, but recommended if not using `python -m venv`)

Make sure you have Python and pip installed:
```bash
python --version
pip --version
```

If `virtualenv` is not installed, you can install it with:
```bash
pip install virtualenv
```

## Project Structure

```
project-root/
├─ requirements.txt     # All global dependencies (for both frontend and backend)
├─ backend/
│  └─ main.py           # FastAPI application entry point
└─ frontend/
   └─ main.py           # Streamlit application entry point
```

## Setting Up the Environment

1. **Navigate to the project root directory:**
    ```bash
    cd path/to/project-root
    ```

2. **Create and activate a virtual environment:**
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install all global dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

This single environment now contains all the necessary packages to run both the FastAPI backend and the Streamlit frontend.

## Running the Backend (FastAPI)

1. **Open a terminal (with the virtual environment activated).**
   
2. **Navigate to the `backend` directory:**
    ```bash
    cd backend
    ```

3. **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
    Your backend API will be available at:
    [http://localhost:8000](http://localhost:8000)

    You can also access the interactive API docs at:
    [http://localhost:8000/docs](http://localhost:8000/docs)

## Running the Frontend (Streamlit)

1. **Open a separate terminal window/tab (with the same virtual environment activated).**

2. **Navigate to the `frontend` directory:**
    ```bash
    cd frontend
    ```

3. **Run the Streamlit application:**
    ```bash
    streamlit run main.py
    ```
   
    After running the command, the Streamlit app should open automatically in your browser. If not, you can access it by visiting:
    [http://localhost:8501](http://localhost:8501)

## Notes

- **Virtual Environment Activation:**
  Each time you open a new terminal, you need to re-activate the virtual environment before running your commands:
  - On macOS/Linux: `source venv/bin/activate`
  - On Windows: `venv\Scripts\activate`

- **Deactivating the Virtual Environment:**
  When done, you can deactivate by running:
  ```bash
  deactivate
  ```

- **Updating Dependencies:**
  If `requirements.txt` is updated, you can re-run:
  ```bash
  pip install -r requirements.txt --upgrade
  ```
  to ensure you have the latest dependencies.

## Conclusion

By following these steps, you’ll have a running FastAPI backend on `http://localhost:8000` and a Streamlit frontend on `http://localhost:8501`. Remember to keep both servers running in separate terminals with the same virtual environment activated for smooth operation.
