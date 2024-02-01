# Semantic Parameter Matching in Web APIs with Transformer-based Question Answering
This repository is the official implementation of the paper ["Semantic Parameter Matching in Web APIs with Transformer-based Question Answering"](https://ieeexplore.ieee.org/document/10254746) (see citation) and contains notebooks for fine-tuning and evaluating a pre-trained BERT model to the task of semantic parameter matching in Web APIs. 
Additional materials (datasets, model checkpoints, and reports of executed notebooks) can be found on [Zenodo](https://zenodo.org/records/8019625).
The fine-tuned model (best checkpoint with a top-k accuracy of 81.46% for k=1) is available on [Hugging Face](https://huggingface.co/SebastianKotstein/restberta-qa-parameter-matching).

## Web API and UI for Inference
We implemented a Flask application that places our model behind a Web API and UI for inference.
To use this application, navigate to [tools](https://github.com/SebastianKotstein/Parameter-Matching-Web-APIs/tree/master/tools) and create a docker image with:
```
docker build -t restberta-core .
```
Start the docker container with:
```
docker run -d -p 80:80 --name pm-cpu restberta-core .
```
If you want to start the application for another Web API integration task, i.e., with another RESTBERTa model (e.g., for endpoint discovery, see [RESTBERTa](https://github.com/SebastianKotstein/RESTBERTa)), specify the model as ENV parameter:
```
docker run -d -p 80:80 -e MODEL=SebastianKotstein/restberta-qa-endpoint-discovery --name ed-cpu restberta-core
```
### Web UI
To open the Web UI, use a browser and navigate to http://localhost:80.

### Web API
Use the following cURL to make a prediction:
```
curl -L 'http://localhost:80/predict' \
-H 'Accept: application/vnd.skotstein.restberta-core.results.v1+json' \
-H 'Content-Type: application/vnd.skotstein.restberta-core.schemas.v1+json' \
-d ' {
 "schemas":[
    {
      "schemaId": "s00",
      "name": "My schema",
      "value": "state units auth.key location.city location.city_id location.country location.lat location.lon location.postal_code",
      "queries": [
        {
          "queryId": "q0",
          "name": "My query",
          "value": "The ZIP of the city",
          "verboseOutput": true
        }
      ]
    }
  ]
}'
```

## Citation
```bibtex
@INPROCEEDINGS{10.1109/SOSE58276.2023.00020,
  author={Kotstein, Sebastian and Decker, Christian},
  booktitle={2023 IEEE International Conference on Service-Oriented System Engineering (SOSE)}, 
  title={Semantic Parameter Matching in Web APIs with Transformer-based Question Answering}, 
  year={2023},
  volume={},
  number={},
  pages={114-123},
  doi={10.1109/SOSE58276.2023.00020}}
```




