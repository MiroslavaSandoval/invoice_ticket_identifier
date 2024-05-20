# invoice_ticket_identifier

# Project Title

One-liner subtitle: Efficient Data Processing and Visualization Tool for Invoices and Tickets

## Introduction

This project is designed to streamline the process of data analysis by providing a set of scripts and tools that facilitate data cleaning, processing, and visualization. The key features of this project include:

- **Automated Data Cleaning**: Efficiently handle missing values, outliers, and inconsistencies in your dataset.
- **Data Processing**: Transform and normalize data to prepare it for analysis.
- **Visualization Tools**: Generate insightful and customizable charts and graphs.
- **OCR and XML Handling**: Extract and process text from images and XML files for comprehensive analysis.
- **AI Integration**: Utilize OpenAI to analyze and summarize data effectively.

By using this tool, you can save time and effort in preparing your data for analysis, ensuring that your insights are based on clean and well-processed data.

![Example Visualization](path/to/your/image.png)

## Instructions

To get started with this project, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine using `git clone`.
   
2. **Install Dependencies**: Install the necessary dependencies using the following command:
   ```sh
   pip install -r requirements.txt
   ```

3. **Provide Input Files**: Ensure that your data files are available in the appropriate directories. The required files are:
   - `Tickets/*.jpeg`: The raw ticket images that need processing.
   - `xml_files/*.xml`: The raw XML files containing invoice information.
   - `excluded_lines.txt`: List of lines to exclude during XML processing.
   - `irrelevant_attributes.txt`: List of irrelevant attributes to ignore during XML processing.
   - `customer_attributes.txt`: List of customer-related attributes to ignore during XML processing.

4. **Run the Scripts**: Execute the scripts in the following order:

   ### 1. Preprocess Images
   Process the ticket images by converting them to grayscale, enhancing their contrast, and applying binarization. The processed images are saved in the `processed` folder.
