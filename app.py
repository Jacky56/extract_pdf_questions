from transformers import pipeline as build, AutoTokenizer, AutoModelForSequenceClassification
import pdfplumber
from typing import List, Iterable
import json
from os import listdir
from datetime import datetime

MODEL = "shahrukhx01/question-vs-statement-classifier"
TOKENIZER = "shahrukhx01/question-vs-statement-classifier"
PDF_DIR = "/pdf"

def get_pipeline(tokenizer: str=TOKENIZER, model: str=MODEL):
    pipeline = build(
        task='text-classification',
        tokenizer=tokenizer, 
        model=model)
    return pipeline

def get_pdf(dir: str) -> List[str]:
    pdf = pdfplumber.open(dir)
    s = "".join([page.extract_text() for page in pdf.pages])
    sequences = [e for e in s.replace(":", "?\n").split("\n") if e]
    return sequences

def clean_result(sequences_results: Iterable) -> List[dict]:
    a = []
    for sequence, result in sequences_results:
        score = result["score"] if result["label"] == "LABEL_1" else 1 - result["score"] 
        d = {
            "sequence": sequence,
            "interrogation_score": score 
        }
        a.append(d)
    return a

if __name__ == "__main__":
    pdfs = [pdf for pdf in listdir(PDF_DIR) if ".pdf" in pdf]
    pipeline = get_pipeline()
    a = []
    for pdf in pdfs:
        sequences = get_pdf(f"{PDF_DIR}/{pdf}")
        results = pipeline(sequences)
        output = clean_result(zip(sequences,results))
        a.append(output)
        json.dump(output, open(f"{PDF_DIR}/{int(datetime.now().timestamp())}_{pdf}.json", "w"), indent=4)
    print(json.dumps(a, indent=4))