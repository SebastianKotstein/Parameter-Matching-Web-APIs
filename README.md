# Semantic Parameter Matching in Web APIs with Transformer-based Question Answering
This repository is the official implementation of the paper ["Semantic Parameter Matching in Web APIs with Transformer-based Question Answering"](https://ieeexplore.ieee.org/document/10254746) (see citation) and contains notebooks for fine-tuning and evaluating a pre-trained BERT model to the task of semantic parameter matching in Web APIs. 
Additional materials (datasets, model checkpoints, and reports of executed notebooks) can be found on [Zenodo](https://zenodo.org/records/8019625).
The fine-tuned model (best checkpoint with an top-k accuracy of 81.46% for k=1) is available on [Hugging Face](https://huggingface.co/SebastianKotstein/restberta-qa-parameter-matching).

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




