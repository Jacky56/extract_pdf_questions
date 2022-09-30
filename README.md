# pdf question predictor

this docker image is used to extract text sequences from pdf files and score 
if they possess interrogative properties.


model used:
- BERT: [shahrukhx01/question-vs-statement-classifier](https://huggingface.co/shahrukhx01/question-vs-statement-classifier)

libraries used:
- [requirements.txt](./requirements.txt)

## how to build container

```bash
docker build -t <name of container> .
```

example:
```bash
docker build -t pdf_question_predictor .
```

## how to run container

```bash
docker run -v <absolute directory to pdf folder>:/pdf <name of container>
```

example:
```bash
docker run -v /usr/banana/pdf:/pdf pdf_question_predictor
```

## result

result `json` files will be published at the mounted volume directory `<absolute directory to pdf folder>`: one `json` file per `pdf`.

`json` name:
```text
<unix timestamp>_<pdf name>.json
```

`json` structure:
```json
[
    {
        "sequence": "\uf0c3 UAT",
        "interrogation_score": 0.0014404654502868652
    },
    {
        "sequence": "How did you hear about us?",
        "interrogation_score": 0.9995403289794922
    },
    {
        "sequence": "Applicant?",
        "interrogation_score": 0.9961137771606445
    },
    ...
    {
        "sequence": "Page 1/14",
        "interrogation_score": 0.0003731846809387207
    }
]
```
