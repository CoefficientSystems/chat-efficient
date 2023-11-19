# Project-specific setup

This document contains setup instructions specifically for this project only. This design enables
us to keep other docs easily aligned with future upstream changes to
[coefficient-cookiecutter](https://github.com/CoefficientSystems/coefficient-cookiecutter/).


## llama-cpp-python

Follow the instructions here: https://abetlen.github.io/llama-cpp-python/macos_install/

```sh
CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install -U llama-cpp-python --no-cache-dir
pip install 'llama-cpp-python[server]'
```

Download one of these:
- https://huggingface.co/vicuna/ggml-vicuna-13b-1.1/blob/main/ggml-vic13b-q4_0.bin
- https://huggingface.co/vicuna/ggml-vicuna-13b-1.1/blob/main/ggml-vic13b-uncensored-q4_0.bin
- https://huggingface.co/TheBloke/LLaMa-7B-GGML/blob/main/llama-7b.ggmlv3.q4_0.bin
- https://huggingface.co/TheBloke/LLaMa-13B-GGML/blob/main/llama-13b.ggmlv3.q4_0.bin

I went with `TheBloke/LLaMa-7B-GGML`.

Run the webserver:

```sh
# config your ggml model path
# make sure it is ggml v3
# make sure it is q4_0
export MODEL=./models/llama-2-13b-chat.ggmlv3.q4_0.bin
python3 -m llama_cpp.server --model $MODEL  --n_gpu_layers 1

# Note: If you omit the --n_gpu_layers 1 then CPU will be used
```

Try the Python API:

```python
from llama_cpp import Llama
llm = Llama(model_path="./models/llama-2-13b-chat.ggmlv3.q4_0.bin")
output = llm("Q: Name the planets in the solar system? A: ", max_tokens=64, stop=["Q:", "\n"], echo=True)
print(output)
print(output['choices'][0]['text'])
```


## Jupyter kernel

```sh
python -m ipykernel install --user --name chatefficient --display-name "Python (chatefficient)"
```
