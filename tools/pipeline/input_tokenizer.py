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

from transformers import AutoTokenizer

class InputTokenizer: 

    def __init__(self, base_model: str, max_length: int = 512, doc_stride: int = 128):
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        #self.tokenizer.save_pretrained("/home/user/2023_02_16_QA/checkpoints")
        self.max_length = max_length
        self.doc_stride = doc_stride


    def mask_offset_mapping(self, sequence_ids, context_index, offset_mapping):
        """
        Masks the passed 'offset_mapping', i.e., replaces all entries with 'None' that represent tokens that are not part of the context.
        The method returns the masked offset mapping.
        
        Parameters
        ----------
        sequence_ids :
            Vector that defines for each token whether the token is part of the question, of the context, or is a special token.
            An entry representing a token that is part of the context must have the value specified in 'context_index'
        context_index : int
            Value that is used to mark a token as part of the context in 'sequence_ids'
        offset_mapping
            Vector that contains for each token its start and end index on character level in the original input (consisting of question, context, and special characters). 
        
        Returns
        -------
        Masked 'offset_mapping'; entries that represent tokens that are not part of the context have the value 'None'
        """
        masked_offset_mapping = [(o if sequence_ids[k] == context_index else None) for k, o in enumerate(offset_mapping)]
        return masked_offset_mapping


    def tokenize(self, batch):

        # Tokenizes the QA samples of the passed batch. Each QA sample may result into multiple tokenized samples if the input sequence, consisting of query and paragraph, exceeds the model's input size (typically 512 tokens). 
        # If a QA sample must be split into multiple tokenized samples, only the paragraph will be split by the tokenizer so that every resulting tokenized sample will contain the original query plus another fragment of the original paragraph. 
        # Note that the resulting fragments overlap by the number of tokens specifiec in 'doc_stride'. Example: If a 'doc_stride' of 128 is set, the second fragment will start with the last 128 tokens of the first fragment, and so further.
        tokenized_samples = self.tokenizer(
            batch["query"],
            batch["paragraph"],
            truncation="only_second",
            max_length=self.max_length,
            stride=self.doc_stride,
            return_overflowing_tokens=True,
            return_offsets_mapping=True,
            padding="max_length",
        )

        # ID of the sample (string), e.g. "7fed77b9abe24a2db869c8b9919a1e9b"
        tokenized_samples["qa_sample_id"] = []
        #  Title of the sample (string), e.g. "my very urgent question"
        tokenized_samples["qa_sample_title"] = []
        # Query, i.e., query, of the sample (string), e.g. "The name of a user"
        tokenized_samples["qa_sample_query"] = []

        # ID of the paragraph (string), e.g. "7fed77b9abe24a2db869c8b9919a1e9b"
        tokenized_samples["qa_sample_paragraph_id"] = []
        # Title of the paragraph (string), e.g. "schema XYZ"
        tokenized_samples["qa_sample_paragraph_title"] = []
        # Context of the sample (string), e.g. "users[*].id users[*].name _links.href _links.rel"
        tokenized_samples["qa_sample_paragraph"] = []

        # fragment of the tokenized sample
        tokenized_samples["tokenized_sample_fragment"] = []
        # input tokens of the tokenized sample ([string])
        tokenized_samples["tokenized_sample_tokens"] = []
        # Index of the CLS token (int)
        tokenized_samples["tokenized_sample_cls_index"] = []


        







