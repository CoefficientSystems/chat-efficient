# Project-specific setup

This document contains setup instructions specifically for this project only. This design enables
us to keep other docs easily aligned with future upstream changes to
[coefficient-cookiecutter](https://github.com/CoefficientSystems/coefficient-cookiecutter/).


## llama-cpp-python

Follow the instructions here: https://abetlen.github.io/llama-cpp-python/macos_install/

```sh
pip uninstall llama-cpp-python -y
CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install -U llama-cpp-python --no-cache-dir
pip install 'llama-cpp-python[server]'
```

Download a model file, see the following for advice:
  - [https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF#provided-files]
  - [https://huggingface.co/TheBloke/Llama-2-13B-Chat-GGUF#provided-files]
  - [https://huggingface.co/TheBloke/Llama-2-70B-Chat-GGUF#provided-files]

```sh
# Llama-2 (7 billion parameters, 4.08GB file size, up to 7.2GB RAM required to run)
huggingface-cli download TheBloke/Llama-2-7b-Chat-GGUF llama-2-7b-chat.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
mv ./llama-2-7b-chat.Q4_K_M.gguf ./models/

# Llama-2 (13 billion parameters, 7.87GB file size, up to 10.37GB RAM required to run)
huggingface-cli download TheBloke/Llama-2-13b-Chat-GGUF llama-2-13b-chat.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
mv ./llama-2-13b-chat.Q4_K_M.gguf ./models/

# Llama-2 (70 billion parameters, 41.42GB file size, up to 44GB RAM required to run)
huggingface-cli download TheBloke/Llama-2-70b-Chat-GGUF llama-2-70b-chat.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
mv ./llama-2-70b-chat.Q4_K_M.gguf ./models/
```

Run the webserver:

```sh
# config your gguf model path
# make sure it is gguf and Q3
export MODEL=./models/llama-2-7b-chat.Q4_K_M.gguf
python3 -m llama_cpp.server --model $MODEL  --n_gpu_layers 1

# Note: If you omit the --n_gpu_layers 1 then CPU will be used
```

Try the Python API:

```python
from llama_cpp import Llama
llm = Llama(model_path="./models/llama-2-7b-chat.Q4_K_M.gguf")
output = llm("Q: Name the planets in the solar system? A: ", max_tokens=64, stop=["Q:", "\n"], echo=True)
print(output)
print(output['choices'][0]['text'])
```


## Jupyter kernel

```sh
python -m ipykernel install --user --name chatefficient --display-name "Python (chatefficient)"
```
