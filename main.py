# Import necessary libraries
import streamlit as st
import pdfplumber
import time
import os
import google.generativeai as genai  # Gemini API

# Set your Gemini API key
GEMINI_API_KEY = "AIzaSyAVgOz95HROmUSl1qjdJ3nOydjOUy51OpM"  # Replace with your Gemini API key

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")  # Updated to Gemini 1.5 Flash

# Step 1: Extract text from the PDF using pdfplumber (optimized for large files)
def extract_text_from_pdf(pdf_path, chunk_size=10):
    """
    Extracts text from a PDF in chunks to handle large files efficiently.
    """
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                # Process in chunks to avoid memory issues
                if (i + 1) % chunk_size == 0:
                    yield text
                    text = ""
            # Yield the remaining text
            if text:
                yield text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        yield None

# Step 2: Use Gemini API to convert text into structured format
def convert_text_to_structured_format(text):
    """
    Uses Gemini API to convert text into a structured format.
    """
    try:
        prompt = (
            "You are an artificial intelligence assistant and you need to "
            "process a financial document and convert it into a structured format. "
            "Extract key-value pairs and tables for Profit & Loss (P&L) terms such as "
            "Revenue, Expenses, Gross Profit, Operating Income, Net Profit, etc. "
            "Ensure the output is precise and well-structured. "
            "Provide the output in a clean, tabular format without any code or markdown.\n\n"
            f"Text: {text}\n\nConvert this text into a structured format."
        )

        # Call the Gemini API
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error converting text to structured format: {e}")
        return None

# Step 3: Use Gemini API to answer user queries
def generate_answer_with_gemini(query, structured_data):
    """
    Uses Gemini API to generate an answer based on the query and structured data.
    """
    try:
        prompt = (
            "You are an artificial intelligence assistant and you need to "
            "engage in a helpful, detailed, polite conversation with a user. "
            "Use the provided structured data to answer the user's question. "
            "Focus on Profit & Loss (P&L) terms such as Revenue, Expenses, "
            "Gross Profit, Operating Income, Net Profit, etc. "
            "Provide the output in plain text format without any code or markdown.\n\n"
            f"Structured Data: {structured_data}\n\nQuestion: {query}\nAnswer:"
        )

        # Call the Gemini API
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating answer with Gemini API: {e}")
        return None

# Streamlit App
def main():
    # Set up the UI with Zara's branding
    st.set_page_config(page_title="Zara - Your Financial Assistant", page_icon="🤖")

    # Title and description
    st.title("🤖 Zara - Your Personalized Financial Assistant")
    st.write(
        """
        Hi there! I'm **Zara**, your personalized financial assistant. 
        I can summarize the financial documents you upload and answer any questions you have about them. 
        Whether it's a Profit & Loss statement, balance sheet, or any other financial report, I'm here to help!
        """
    )

    # Initialize session state for caching
    if "structured_data" not in st.session_state:
        st.session_state.structured_data = None
    if "show_structured_data" not in st.session_state:
        st.session_state.show_structured_data = False
    if "ask_questions" not in st.session_state:
        st.session_state.ask_questions = False

    # Step 1: Upload multiple PDFs
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        try:
            # Check if structured data is already cached
            if st.session_state.structured_data is None:
                # Process each uploaded file
                structured_data = ""
                for uploaded_file in uploaded_files:
                    # Save the uploaded file temporarily
                    with open("temp.pdf", "wb") as f:
                        f.write(uploaded_file.getvalue())

                    # Extract text from the PDF in chunks
                    st.write(f"📄 Extracting and processing {uploaded_file.name}...")
                    for chunk in extract_text_from_pdf("temp.pdf"):
                        if chunk:
                            # Convert each chunk to structured format
                            chunk_structured_data = convert_text_to_structured_format(chunk)
                            if chunk_structured_data:
                                structured_data += chunk_structured_data + "\n\n"

                # Cache the structured data in session state
                st.session_state.structured_data = structured_data
            else:
                st.write("📊 Using cached structured data...")

            # Notify the user about incomplete data
            st.warning(
                """
                **Note**: The provided data offers fragments, but not the complete picture. 
                To create a full structured P&L, a complete financial statement is required.
                """
            )

            # Ask the user if they want to see the structured data
            st.write("### What would you like to do next?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Show Structured Data"):
                    st.session_state.show_structured_data = True
                    st.session_state.ask_questions = False
            with col2:
                if st.button("Proceed to Ask Questions"):
                    st.session_state.show_structured_data = False
                    st.session_state.ask_questions = True

            # Display structured data if the user chooses to see it
            if st.session_state.show_structured_data and st.session_state.structured_data:
                st.write("### 📊 Structured Data:")
                st.write(st.session_state.structured_data)

            # Allow user to enter queries if they choose to ask questions
            if st.session_state.ask_questions and st.session_state.structured_data:
                st.write("### ❓ Ask Zara a Question")
                query = st.text_input("Enter your question:")
                if query:  # Only generate an answer if the user has entered a question
                    # Generate an answer using Gemini API
                    start_time = time.time()
                    answer = generate_answer_with_gemini(query, st.session_state.structured_data)
                    end_time = time.time()

                    if answer:
                        # Display Zara's answer with the 🤖 emoji
                        st.write("### 🤖 Zara's Answer:")
                        st.write(answer)
                        st.write(f"⏱️ Response time: {end_time - start_time:.2f} seconds")
                    else:
                        st.warning("Unable to generate an answer. Please try again.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()