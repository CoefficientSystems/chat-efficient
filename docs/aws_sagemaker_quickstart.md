# Quickstart

This document contains instructions to get up & running with this repo using AWS SageMaker.

## Part 1: Create a SageMaker Notebook

From the AWS Console:
- Go to Service Quotas and request a GPU quota increase for `ml.g4dn.xlarge` for 1 GPU for both
  notebook instance usage and for Studio KernelGateway Apps.
- Launch a SageMaker Notebook from SageMaker > Notebook > Notebook instances > Create notebook instance
- Select `ml.g4dn.xlarge` instance type (see [https://aws.amazon.com/sagemaker/pricing/] for pricing)


## Part 2: Install Python dependencies

Create a new terminal and run the following:

```sh
# Switch to a bash shell
bash

# Change to the repo root
cd ~/SageMaker/chat-efficient

# Activate a Python 3.10 environment pre-configured with PyTorch
conda activate pytorch_p310

# Check Python version
python --version

# Install the repo's declared dependencies
pip install -r requirements.txt

# What GPUs are installed on this instance?
nvidia-smi

# Install llama-cpp-python
# Reference: https://llama-cpp-python.readthedocs.io/en/latest/
pip uninstall llama-cpp-python -y
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python

# Download the Llama-2 model from Hugging Face (7 billion parameters, 4.08GB file size, up to 7.2GB RAM required to run)
huggingface-cli download TheBloke/Llama-2-7b-Chat-GGUF llama-2-7b-chat.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
mv ./llama-2-7b-chat.Q4_K_M.gguf ./models/

# Alternatively, if you have enough memory, you can download the 13B Llama-2 model (7.87GB file size, up to 10.37GB RAM required)
huggingface-cli download TheBloke/Llama-2-13b-Chat-GGUF llama-2-13b-chat.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
mv ./llama-2-13b-chat.Q4_K_M.gguf ./models/
```

Test it out in `ipython`:

```python
from llama_cpp import Llama
llm = Llama(model_path="./models/llama-2-7b-chat.Q4_K_M.gguf")
output = llm("Q: Name the planets in the solar system? A: ", max_tokens=64, stop=["Q:", "\n"], echo=True)
print(output)
print(output['choices'][0]['text'])
```

Type ctrl+D to quit.


## Part 3: Add OpenAI key

```sh
cp .env.template env
# Edit the file "env" to specify your OpenAI key. Save & close.
mv env .env

# These will now be loaded as environment variables when we run `load_dotenv()` from the python-dotenv package.
```
