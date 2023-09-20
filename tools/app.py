'''
Copyright 2023 Sebastian Kotstein

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''


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
