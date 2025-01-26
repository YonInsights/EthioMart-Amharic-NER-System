# EthioMart Amharic NER System for Telegram E-Commerce Integration

## Project Overview
EthioMart is a comprehensive solution designed to revolutionize Ethiopian e-commerce conducted on Telegram. By leveraging advanced Amharic Named Entity Recognition (NER) and object detection techniques, this system extracts and organizes critical business entities—such as product names, prices, and locations—from unstructured text and images shared on various Telegram channels.

The project consolidates these extracted entities into a centralized database, enabling a unified platform for buyers and sellers, thus enhancing accessibility, efficiency, and decision-making in Ethiopian e-commerce.

---

## Objectives
- **Entity Extraction**: Extract product names, prices, and locations from Amharic text messages.
- **Model Fine-tuning**: Adapt multilingual models (e.g., XLM-Roberta, BERT-tiny-Amharic) for Amharic NER.
- **Model Evaluation**: Compare model performance using precision, recall, and F1-score.
- **Object Detection**: Use YOLO to identify objects in product images.
- **Integration**: Develop a pipeline for real-time processing and storage in a MySQL database.

---

## Dataset Overview
- **Source**: Ethiopian e-commerce Telegram channels.
- **Types**:
  - **Text**: Amharic-language messages.
  - **Images**: Product visuals and advertisements.
  - **Metadata**: Sender information, timestamps, and message IDs.
- **Labeling Format**: 
  - CoNLL for text entities.
  - Annotated bounding boxes for image data.

---

## Technologies Used
### Programming Language
- Python

### Libraries
- **NLP**: Hugging Face Transformers, SpaCy, NLTK
- **Object Detection**: PyTorch, YOLOv5, OpenCV
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Database**: MySQL
- **Web API**: FastAPI

### Tools
- **ETL Frameworks**: DBT (Data Build Tool)
- **Deployment**: Flask, Streamlit
- **Collaboration**: Git, GitHub
- **Development Environment**: Jupyter Notebook, VS Code, Google Colab

---

## Repository Structure
```plaintext
├── .github/
│   └── workflows/
│       └── ci_cd.yml          # CI/CD for testing and deployment
├── README.md                  # Project documentation
├── requirements.txt           # Dependencies
├── src/
│   ├── __init__.py
│   ├── data_scraping.py       # Telegram scraping pipeline
│   ├── preprocessing.py       # Text preprocessing and tokenization
│   ├── ner_training.py        # Model fine-tuning for NER
│   ├── object_detection.py    # YOLO-based image analysis
│   ├── model_evaluation.py    # Performance evaluation
│   ├── api.py                 # FastAPI endpoint definitions
│   └── database.py            # MySQL integration for entity storage
├── data/
│   ├── raw/                   # Collected raw data
│   ├── processed/             # Cleaned and labeled data
│   └── examples/              # Sample annotated datasets
├── notebooks/
│   ├── eda.ipynb              # Exploratory Data Analysis
│   ├── preprocessing.ipynb    # Preprocessing workflows
│   ├── model_training.ipynb   # NER model training
│   ├── object_detection.ipynb # YOLO experiments
│   └── api_testing.ipynb      # API testing and validation
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py       # Unit tests for project components
├── results/
│   ├── metrics/               # Model evaluation results
│   ├── logs/                  # Logs for scraping and processing
│   └── visualizations/        # Analysis and charts
```
## **Usage Guide**
### Prerequisites
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: `env\Scripts\activate`
   pip install -r requirements.txt
   ```
   ## **Author**
**Yonatan Abrham**  
- Email: [email2yonatan@gmail.com](mailto:email2yonatan@gmail.com)  
- LinkedIn: [Yonatan Abrham](https://www.linkedin.com/in/yonatan-abrham1/)  
- GitHub: [YonInsights](https://github.com/YonInsights)  
Feel free to connect for collaborations or queries.

---

## **Acknowledgements**
- Heartfelt thanks to 10 Academy for providing an excellent internship opportunity.
- Appreciation for the open-source tools and the community that made this project possible.

---

