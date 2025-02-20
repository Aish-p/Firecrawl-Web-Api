# WebScraperAPI 🔥 – Extract smarter, faster, and better! 

WebScraperAPI is a powerful web application that transforms any website into structured data using the Firecrawl API. It provides an intuitive interface for extracting specific information from websites and converting it into structured formats like JSON and CSV.

## Features

- 🌐 Extract data from any website URL
- 📊 Custom schema builder for structured data extraction
- 💬 Natural language interface for data queries
- ⬇️ Export data in JSON and CSV formats
- 🔄 Real-time data streaming
- 🎯 Support for multiple data types (string, boolean, integer, float)


## ⚡ Quick Start

1️⃣ Clone the Repository
  ```
  git clone https://github.com/Aish-p/WebScraperAPI.git
  cd WebScraperAPI
  ```

2️⃣ Install Dependencies
  ```
  pip install -r requirements.txt
  ```

3️⃣ Set Up Environment Variables
  Create a .env file and add your Firecrawl API key:
  ```
  FIRECRAWL_API_KEY=your-api-key-here
  ```

4️⃣ Run the App
  ```
  streamlit run app.py
  ```


## 🛠 How It Works

1. Enter a website URL in the sidebar.

2. (Optional) Configure the schema builder:
   * Add fields by clicking "Add Field ➕"
   * Specify field names and types
   * Remove fields using the ❌ button

3. Ask questions about the website in the chat interface

4. Download the extracted data in JSON or CSV format


## 🔗 Technologies Used

**Firecrawl** – AI-powered web data extraction

**Streamlit** – Interactive Python apps

**Pandas** – Data processing

**Pydantic** – Schema validation

**Dotenv** – Environment variable management

## Demo
### Main Interface
![Main Interface](screenshots/main_interface.png)
*The main application interface with sidebar configuration*

### Example Queries and Results

#### Product Information Extraction
![Product Query](screenshots/product_query1.png)
![Product Query](screenshots/product_query2.png)
*Extracting product details from an e-commerce website*

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Firecrawl API](https://firecrawl.com/)
