
from flask import Flask, request, jsonify
from pipeline.pipeline import Pipeline
import json


app = Flask(__name__)
pipeline = Pipeline("SebastianKotstein/restberta-qa-parameter-matching",20,2)

@app.route("/",methods=["POST"])
def api():
    args = request.args
    top_answers_n = None

    suppress_duplicates = False
    if "duplicates" in args and args["duplicates"] == "suppress":
        suppress_duplicates = True

    if "top" in args and args["top"]:
        top_answers_n = int(args["top"])

    return jsonify(pipeline.process(request.json,top_answers_n,suppress_duplicates))

'''
if __name__ == '__main__':
    pipeline = Pipeline("SebastianKotstein/restberta-qa-parameter-matching",20,2)

    input = {
        "schemas":[
            {
                "schemaId": "s1",
                "name": "testSchema",
                "value": "auth.key location.city location.city_id location.country location.lat location.lon location.postal_code state units", 
                "queries":[
                    {
                        "queryId": "q1",
                        "name": "first query",
                        "value": "The ZIP",
                        "verboseOutput":False
                    },
                    {
                        "queryId": "q2",
                        "name": "second query",
                        "value": "The auth token",
                        "verboseOutput":False
                    }
                    
                ]
            },
            {
                "schemaId": "s2",
                "name": "schemaWoQueries",
                "value": "none",
                "queries":[]
            }
        ]
    }

    results = pipeline.process(input)
    print(json.dumps(results, indent=2))
'''
