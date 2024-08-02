# PDF MASKER



**PDF MASKER** is a tool designed to help you easily process and redact sensitive information from PDF documents. This application uses advanced machine learning models to identify and mask sensitive data such as names, ages, phone numbers, addresses, and emails.

## Features

- **Multi-Language Support**: Processes documents in multiple languages including English, Mandarin, German, Indonesian, Korean, Spanish, French, Italian, Latvian, Dutch, and Portuguese.
- **Advanced Redaction**: Masks sensitive information such as names, ages, phone numbers, addresses, and emails using regex patterns and NER (Named Entity Recognition) models.
- **Easy-to-Use Interface**: User-friendly web interface built with Streamlit, allowing you to upload, process, and download your PDFs with ease.
- **Download Options**: Provides options to download both the redacted PDF and a CSV file containing information about the redactions.

## Getting Started

### Prerequisites

Before running the application, ensure you have Python 3.12 or later installed. You will also need to install the necessary Python packages.

### Installation

1. **Clone the Repository**:
    
    ```bash
    bashCopy code
    git clone https://github.com/your-username/pdf-masker.git
    cd pdf-masker
    
    ```
    
2. **Install Dependencies**:
    
    Create a virtual environment (recommended) and install the required packages using the `requirements.txt` file.
    
    ```bash
    bashCopy code
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    pip install -r requirements.txt
    
    ```
    

### Running the Application

1. **Start the Streamlit App**:
    
    Navigate to the directory where `main.py` is located and run:
    
    ```arduino
    arduinoCopy code
    streamlit run main.py
    
    ```
    
    This will start a local server and open the Streamlit app in your web browser.
    
2. **Upload and Process a PDF**:
    - In the sidebar, select the language of your PDF.
    - Upload your PDF document.
    - The application will process the document, redact sensitive information, and provide download links for the processed PDF and CSV file.

## Troubleshooting

- **Logo Image Not Found**: Ensure that the logo image file is correctly placed in the `./assests/` directory. If not, update the path in the `main.py` file.
- **Dependencies**: If you encounter issues related to missing packages or versions, ensure that all dependencies listed in `requirements.txt` are installed correctly.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any inquiries or support, please contact:

- **Email**: your.email@example.com
- **GitHub**: your-username

## Citations

```
@misc{zaratiana2023gliner,
      title={GLiNER: Generalist Model for Named Entity Recognition using Bidirectional Transformer},
      author={Urchade Zaratiana and Nadi Tomeh and Pierre Holat and Thierry Charnois},
      year={2023},
      eprint={2311.08526},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
