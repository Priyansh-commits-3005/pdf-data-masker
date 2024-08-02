import fitz  # PyMuPDF
import re
import csv
import io
import base64
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from gliner import GLiNER

# Define regex patterns for age, phone numbers, addresses, and emails
age_regex = r'\b(?:[1-9][0-9]?|100)\b'  # Matches ages 1-100
phone_regex = r'\b(?:\+?\d{1,3})?[\s.-]?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{4}\b'
address_regex = r'\b\d{1,4}\s[A-Za-z0-9\s,.]+\b'  # Basic address pattern
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Email pattern

def base_64_encoding(text):
    return str(base64.b64encode(text.encode("utf-8")).decode("utf-8"))

def mask_entities(text, tagger, language):
    if language == "Korean":
        labels = ["ARTIFACTS", "ANIMAL", "CIVILIZATION", "DATE", "EVENT", "STUDY_FIELD", "LOCATION", "MATERIAL", "ORGANIZATION", "PERSON", "PLANT", "QUANTITY", "TIME", "TERM", "THEORY"]
        try:
            entities = tagger.predict_entities(text, labels)
            entities = [{"word": entity["text"], "entity": entity["label"]} for entity in entities]
        except IndexError as e:
            print(f"Error predicting entities: {e}")
            entities = []
    else:
        entities = tagger(text)
    
    masked_entities = []
    masked_text = text
    for entity in entities:
        if entity['entity'] in ['B-PER', 'B-LOC', 'I-PER', 'I-LOC','B-ORG','I-ORG' "CIVILIZATION", "DATE", "PERSON", "TIME", "ORGANIZATION"]:
            masked_text = masked_text.replace(entity['word'], base_64_encoding(entity['word']))
            masked_entities.append(entity['word'])
    
    return masked_text, masked_entities

def mask_text(text, tagger, language):
    masked_text, masked_entities = mask_entities(text, tagger, language)
    # Mask ages, phone numbers, addresses, and emails using regex
    masked_text = re.sub(age_regex, lambda match: base_64_encoding(match.group(0)), masked_text)
    masked_text = re.sub(phone_regex, lambda match: base_64_encoding(match.group(0)), masked_text)
    masked_text = re.sub(address_regex, lambda match: base_64_encoding(match.group(0)), masked_text)
    masked_text = re.sub(email_regex, lambda match: base_64_encoding(match.group(0)), masked_text)
    return masked_text, masked_entities

def redact_pdf(input_pdf, tagger, language):
    doc = fitz.open(stream=input_pdf.read(), filetype="pdf")
    page_data = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()

        # Mask text for CSV
        masked_text, masked_entities = mask_text(text, tagger, language)

        # Add page data for CSV
        page_data.append({
            "Page": page_num,
            "Original Text": text,
            "Masked Text": masked_text,
            "Entities Masked": ", ".join(masked_entities)  # Convert list to comma-separated string
        })

        # Apply redaction visually in the PDF
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:  # Text block
                for line in block["lines"]:
                    for span in line["spans"]:
                        original_text = span["text"]
                        bbox = fitz.Rect(span["bbox"])

                        # Apply redaction if text matches the patterns
                        if re.search(age_regex, original_text) or re.search(phone_regex, original_text) or re.search(address_regex, original_text) or re.search(email_regex, original_text):
                            page.add_redact_annot(bbox, fill=(0, 0, 0))  # Black out the text
                        elif any(entity in original_text for entity in masked_entities):
                            page.add_redact_annot(bbox, fill=(0, 0, 0))  # Black out the text

        page.apply_redactions()  # Apply all redactions to the page

    # Save the redacted PDF
    output = io.BytesIO()
    doc.save(output, garbage=4, deflate=True)
    output.seek(0)
    return output, page_data

def save_to_csv(data):
    output = io.StringIO()
    fieldnames = ["Page", "Original Text", "Masked Text", "Entities Masked"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for page in data:
        writer.writerow({
            'Page': page['Page'],
            'Original Text': page['Original Text'],
            'Masked Text': page['Masked Text'],
            'Entities Masked': page['Entities Masked']
        })
    return output.getvalue()

def load_language_model(language):
    if language == "Korean":
        model = GLiNER.from_pretrained("taeminlee/gliner_ko")
        return model
    else:
        model_name = "Davlan/bert-base-multilingual-cased-ner-hrl"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForTokenClassification.from_pretrained(model_name)
        return pipeline("ner", model=model, tokenizer=tokenizer)
