from io import BufferedReader
from transformers import pipeline as build, AutoTokenizer, AutoModelForSequenceClassification
import pdfplumber
from typing import List, Iterable, Union
import json
from os import listdir
from datetime import datetime
import pickle

MODEL = "shahrukhx01/question-vs-statement-classifier"
TOKENIZER = "shahrukhx01/question-vs-statement-classifier"
PICKLE_DIR = "./model.pickle"

def load_pickle_model(dir: str=PICKLE_DIR):
    pipeline = pickle.load(open(dir, "rb"))
    return pipeline

def download_pipeline(tokenizer: str=TOKENIZER, model: str=MODEL):
    pipeline = build(
        task='text-classification',
        tokenizer=tokenizer, 
        model=model)
    return pipeline

def read_pdf(path_or_fp: Union[str, BufferedReader]) -> List[str]:
    pdf = pdfplumber.open(path_or_fp)
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

# PDF_DIR = "/pdf"
# if __name__ == "__main__":
#     pdfs = [pdf for pdf in listdir(PDF_DIR) if ".pdf" in pdf]
#     pipeline = download_pipeline()
#     a = []
#     for pdf in pdfs:
#         sequences = get_pdf(f"{PDF_DIR}/{pdf}")
#         results = pipeline(sequences)
#         output = clean_result(zip(sequences,results))
#         a.append(output)
#         json.dump(output, open(f"{PDF_DIR}/{int(datetime.now().timestamp())}_{pdf}.json", "w"), indent=4)
#     print(json.dumps(a, indent=4))
