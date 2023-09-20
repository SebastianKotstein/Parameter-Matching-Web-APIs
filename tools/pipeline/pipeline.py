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


from .input_tokenizer import InputTokenizer
from .qa_model import QAModel
from .output_interpreter import OutputInterpreter
from .lru_cache import LRUCache

class Pipeline:
    def __init__(self, model_checkpoint, best_size = 20, cache_size = 1000) -> None:
        self.tokenizer = InputTokenizer("microsoft/codebert-base")
        self.model = QAModel(model_checkpoint)
        self.interpreter = OutputInterpreter(best_size)
        if cache_size:
            self.cache = LRUCache(cache_size,True)
        else:
            self.cache = None
    
    def process(self, input_dict, top = None, suppress_duplicates = False):
        batch = self.json_to_batch(input_dict)
        if len(batch["qa_sample_id"]):
            tokenized_samples = self.tokenizer.tokenize(batch)
            output, batch_size = self.model.predict(tokenized_samples)
            results = self.interpreter.interpret_output(tokenized_samples,output,batch_size)
        else:
            results = self.interpreter.create_empty_results_dict()
        merged_output = self.merge_results_w_input_json(input_dict,results)
        return self.limit_results(merged_output,top,suppress_duplicates)

    def limit_results(self, input_dict, top = None, suppress_duplicates = False):
        for schema in input_dict["schemas"]:
            for query in schema["queries"]:
                if query["result"]:
                    if suppress_duplicates:
                        query["result"]["answers"] = self.suppress_duplicates(query["result"]["answers"])
                        for tokenized_sample in query["result"]["tokenizedSamples"]:
                            tokenized_sample["answers"] = self.suppress_duplicates(tokenized_sample["answers"])
                    if top and len(query["result"]["answers"])>top:
                        query["result"]["answers"] = query["result"]["answers"][0:top]
                        for tokenized_sample in query["result"]["tokenizedSamples"]:
                            if len(tokenized_sample["answers"])>top:
                                tokenized_sample["answers"] = tokenized_sample["answers"][0:top]
        return input_dict
    
    def suppress_duplicates(self, answers):
        without_duplicates = {}
        for answer in answers:
            if answer["property"] is not None:
                if answer["property"]["name"] not in without_duplicates:
                    without_duplicates[answer["property"]["name"]] = answer
            else:
                if "<no-answer>" not in without_duplicates:
                    without_duplicates["<no-answer>"] = answer
        return [x for x in without_duplicates.values()]

    
    def json_to_batch(self, input_dict):
        
        if self.cache:
            batch = {
                "qa_sample_id":[],
                "qa_sample_title":[],
                "qa_sample_query":[],
                "qa_sample_paragraph_id":[],
                "qa_sample_paragraph_title":[],
                "qa_sample_paragraph":[],
                "verbose_output":[]
            }
            for schema in input_dict["schemas"]:
                for query in schema["queries"]:
                    if not self.cache.has(schema["value"],query["value"],query["verboseOutput"]):
                        batch["qa_sample_id"].append(query["queryId"])
                        batch["qa_sample_title"].append(query["name"])
                        batch["qa_sample_query"].append(query["value"])
                        batch["qa_sample_paragraph_id"].append(schema["schemaId"])
                        batch["qa_sample_paragraph_title"].append(schema["name"])
                        batch["qa_sample_paragraph"].append(schema["value"])
                        batch["verbose_output"].append(query["verboseOutput"])
            return batch
        else:
            return {
                "qa_sample_id":[query["queryId"] for schema in input_dict["schemas"] for query in schema["queries"]],
                "qa_sample_title":[query["name"] for schema in input_dict["schemas"] for query in schema["queries"]],
                "qa_sample_query": [query["value"] for schema in input_dict["schemas"] for query in schema["queries"]],
                "qa_sample_paragraph_id": [schema["schemaId"] for schema in input_dict["schemas"] for _ in schema["queries"]],
                "qa_sample_paragraph_title": [schema["name"] for schema in input_dict["schemas"] for _ in schema["queries"]],
                "qa_sample_paragraph": [schema["value"] for schema in input_dict["schemas"] for _ in schema["queries"]],
                "verbose_output": [query["verboseOutput"] for schema in input_dict["schemas"] for query in schema["queries"]]
            }
    
    def merge_results_w_input_json(self, input_dict, results):
        for schema in input_dict["schemas"]:
            for query in schema["queries"]:
                if self.cache and self.cache.has(schema["value"],query["value"],query["verboseOutput"]):
                    query["result"] = self.cache.load(schema["value"],query["value"])
                    query["result"]["isCached"]= True
                else:
                    for i in range(len(results["qa_sample_id"])):
                        if results["qa_sample_paragraph_id"][i] == schema["schemaId"] and results["qa_sample_id"][i] == query["queryId"]:
                            result = {
                                "answers": results["answers"][i],
                                "tokenizedSamples": results["tokenized_samples"][i]
                            }
                            query["result"] = result
                            query["result"]["isCached"]= False

                            if self.cache:
                                self.cache.store(schema["value"],query["value"],result,query["verboseOutput"])
        return input_dict

    
    def results_to_json(self, results_dict):
        results = {"results":[]}
        for i in range(len(results_dict["qa_sample_id"])):
            result = {
                "answers": results_dict["answers"][i],
                "tokenizedSamples": results_dict["tokenized_samples"][i]
            }
            results["results"].append(result)
        return results   