# Financial Bot

## Overview
This project aims to create a financial bot capable of analyzing profit and loss (P&L) statements and other financial documents. The bot allows users to upload PDFs and ask questions related to the contents of the document, providing insights based on the financial data extracted.

## Features
- **PDF Analysis**: The bot extracts and analyzes financial terms and statements from a PDF document.
- **User Interaction**: Users can ask questions related to the document's financial data, and the bot will respond with relevant information.
- **Fast Response**: The bot uses the Gemini-1.5-flash model, which caches information and provides faster response times.

## Requirements
- Python 3.8 or higher
- Streamlit for web deployment
- GitHub repository access

## Installation & Setup

### 1. Clone the Repository
Clone the repository from GitHub to your local machine:
```bash
git clone https://github.com/nj7782/Pl-bot.git
```

### 2. Install Dependencies
Navigate to the project directory and install the required libraries:
```bash
pip install -r requirements.txt
```

### 3. Run the Application Locally
To run the bot locally, use Streamlit to start the web interface:
```bash
streamlit run app.py
```
This will launch the app on your browser.

### 4. Upload a PDF
- Once the app is running, you'll be prompted to upload a PDF document containing financial data.
- The bot will analyze the document and process the relevant financial terms.

### 5. Ask Questions
- After uploading the document, you can ask the bot questions related to its content.
- Example questions include:
  - "What is the total revenue?"
  - "What is the net profit?"

### 6. Review the Results
- The bot will generate and return answers based on the data extracted from the uploaded document.

## Model Used
- **Gemini-1.5-flash**: This model is used for efficient processing. It caches the extracted information and generates output in a minimal time.

## Troubleshooting
- **No Response**: If the bot doesn't respond, ensure that the PDF is correctly uploaded and contains relevant financial data.
- **Performance Issues**: If the app is slow, try running it on a machine with better resources or reduce the document size.


