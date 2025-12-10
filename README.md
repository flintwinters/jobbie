# Spreadsheet CSV Viewer

This is a single-file web application for viewing and editing CSV data, backed by a simple FastAPI server. It includes features like undo/redo, automatic date stamping, a boolean "Done" column, and rich link previews with favicons and titles.

## Features

- **CSV Data Management**: Load, display, and edit tabular data from a CSV file.
- **Undo/Redo**: Track changes with `Ctrl+Z` (undo) and `Ctrl+Y` or `Ctrl+Shift+Z` (redo).
- **Auto-Timestamped Date Column**: A hardcoded "Date" column automatically records the creation time for new entries.
- **Boolean "Done" Checkbox Column**: A hardcoded "Done" column allows you to mark entries as complete with a checkbox.
- **Link Previews**: Cells containing URLs display the website's favicon and title, with the underlying link remaining editable.
- **Add/Delete Columns**: Dynamically add new columns and delete existing ones (except for hardcoded columns).
- **Add Rows**: Add new data entries to the top of the spreadsheet.

## `data.csv` Contents

The `data.csv` file serves as the backend storage for the spreadsheet data. It contains the following columns:

- `Date`: (Hardcoded) Automatically populated with the entry creation timestamp.
- `Done`: (Hardcoded) A boolean checkbox indicating completion status.
- `Job Title`: A free-text field for the job title.
- `Company Name`: A free-text field for the company name.
- `Job Posting Link`: A URL field that will display a link preview (favicon and title).
- `Job Description`: A free-text field for the job description.
- `Application Status`: A free-text field for the application status.

## How to Self-Host

To run this application on your local machine, follow these steps:

1.  **Clone the repository (if applicable) or ensure you have all project files.**

2.  **Install Python Dependencies**:

    Navigate to the project root directory in your terminal and install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start the Backend Server**:

    From the project root directory, run the FastAPI application:
    ```bash
    python main.py
    ```
    This will start the server, typically on `http://0.0.0.0:28889`.

4.  **Access the Application**:

    Open your web browser and navigate to `http://localhost:28889`. The backend server will serve the `index.html` file, and the application will be ready for use.
