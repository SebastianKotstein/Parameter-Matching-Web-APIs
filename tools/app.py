from pipeline.input_tokenizer import InputTokenizer
from pipeline.qa_model import QAModel
from pipeline.output_interpreter import OutputInterpreter


if __name__ == '__main__':
    tokenizer = InputTokenizer("microsoft/codebert-base")
    model = QAModel("SebastianKotstein/restberta-qa-parameter-matching")
    interpreter = OutputInterpreter(20)
    

    batch = {
        "qa_sample_id":["1","2"],
        "qa_sample_title":["Test1","Test2"],
        "qa_sample_query":["The ZIP","The token"],
        "qa_sample_paragraph_id": ["P1","P2"],
        "qa_sample_paragraph_title": ["Payload1","Payload2"],
        "qa_sample_paragraph":["auth.key location.city location.city_id location.country location.lat location.lon location.postal_code state units","auth.key location.city location.city_id location.country location.lat location.lon location.postal_code state units"],
        "verbose_output":[False,False]
    }
    tokenized_samples = tokenizer.tokenize(batch)
    output, batch_size = model.predict(tokenized_samples)
    results = interpreter.interpret_output(tokenized_samples,output,batch_size,True)
    print(results)