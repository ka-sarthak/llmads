# LLMads
A python package that allows you to use modern large-language-models (LLMs) to parse your
documents into structured data models. Currently the data models supported by the package
are suited for X-Ray Diffraction (XRD) data.

## Usage
To use our LLM-based parser on your data XRD data files, follow these steps:

1. Clone the GitHub repo in your local.
    ```sh
    git clone git@github.com:ka-sarthak/llmads.git
    ```
2. Create a virtual environment in the cloned folder and install the `llmads` package.
    ```sh
    cd llmads
    python -m venv .pyenv
    source .pyenv/bin/activate
    pip install .
    ```
3. Change the configs in `llmads.yaml` file present in the root folder. In particular,
  modify the `test_file_path` to your XRD file.
4. Run the parser.
    ```sh
    llmads parse
    ```

To use the LLM models, you need API keys for ChatGroq. Add your API keys in the `.env`
file in the root folder.
```
GROQ_API_KEY=<YOUR_API_KEY>
```
These keys will be loaded automatically by the `config` module. Read more
[here](https://github.com/theskumar/python-dotenv) how it is
done using `dotenv` package.

## Background
The project started during the LLM Hackathon for Applications in Materials and Chemistry 2024.

We explore the application of LLMs for automated parsing of raw files from simulations and experiments. Taking the example of XRD measurement files from three different vendors: Bruker, Rigaku, and Pananalytical, we use the pre-trained Llama3 model to read the raw files and generate output that can be used to populate Pydantic BaseModels classes.

We use chunking of the raw input data and aim towards progressively improving the output from one chunk to the next. This improvement can be in terms of filling in new data as the model comes across it or refining the previously found data.

However, we also observed that the performance of the pre-trained model depends heavily on the chunk size: the model starts to hallucinate new quantities that are not specified in the Pydantic model if the chunk size is non-optimal.

Additionally, we observed that parsing long vectors as `list[float]` is challenging for the model. On the other hand, it performed better when populating point quantities like `float` or `str`.

> Key takeaway: LLMs are capable of generating sensible structured data that can be used to populate pre-defined schemas. But they are unreliable.

## Development
The package is still under development and we welcome your contributions. To start with
development, create a virtual python environment and activate it. Then install the current
package with its `dev` dependencies in editable mode. The following commands can be used
for this.

```sh
python -m venv .pyenv
source .pyenv/bin/activate
pip install -e .[dev]
```
