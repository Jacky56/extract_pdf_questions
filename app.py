from fastapi import FastAPI, File, UploadFile
from common import load_pickle_model, read_pdf, clean_result

app = FastAPI()
pipeline = load_pickle_model()

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file
        sequences = read_pdf(contents)
        results = pipeline(sequences)
        output = clean_result(zip(sequences,results))
        return output
    except Exception as e :
        print(e)
        return {
            "message": "There was an error uploading the file",
            "error": e
        }
