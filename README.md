# ChatEfficient: How To Build Your Own Private ChatGPT Using Streamlit, LangChain & Vicuna

[![CI](https://github.com/CoefficientSystems/chat-efficient/actions/workflows/main.yaml/badge.svg)](https://github.com/CoefficientSystems/chat-efficient/actions/workflows/main.yaml)

DIY ChatGPT using Streamlit, LangChain and open-source LLMs

![Demo](images/vicuna-chat.gif)

## 🎬  Watch again

You can watch the [webinar recording via this link](https://app.session.com/coefficientai/Munch-and-Learn-Tutorial:-How-To-Build-Your-Own-Private-ChatGPT-Using-Streamlit-LangChain-and-Vicuna?s=1&passcode=308697).

You can see all our [upcoming and previous events here](https://coefficient.ai/events).

If you'd like to work with Coefficient to build your own AI-powered apps, please reach out to us at
[contact@coefficient.ai](contact@coefficient.ai) or [complete our enquiry form](https://coefficient.ai/contact).

If you'd like to register to be notified about upcoming events, you can also do that [here](https://coefficient.ai/contact).


## ✅ Project cheatsheet

  - **pre-commit:** `pre-commit run --all-files`
  - **pytest:** `pytest` or `pytest -s`
  - **coverage:** `coverage run -m pytest` or `coverage html`
  - **poetry sync:** `poetry install --no-root --sync`
  - **updating requirements:** see [docs/updating_requirements.md](docs/updating_requirements.md)
  - **create towncrier entry:** `towncrier create 123.added --edit`


## 🏗 Initial project setup

1. See [docs/getting_started.md](docs/getting_started.md) or [docs/quickstart.md](docs/quickstart.md)
   for how to get up & running.
2. Check [docs/project_specific_setup.md](docs/project_specific_setup.md) for project specific setup.
3. See [docs/using_poetry.md](docs/using_poetry.md) for how to update Python requirements using
   [Poetry](https://python-poetry.org/).
4. See [docs/detect_secrets.md](docs/detect_secrets.md) for more on creating a `.secrets.baseline`
   file using [detect-secrets](https://github.com/Yelp/detect-secrets).
5. See [docs/using_towncrier.md](docs/using_towncrier.md) for how to update the `CHANGELOG.md`
   using [towncrier](https://github.com/twisted/towncrier).
