# LLMads
This is one of the projects from the LLM Hackathon for Applications in Materials and Chemistry 2024. We explore the application of LLMs for automated parsing of raw files from simulations and experiments. Taking the example of XRD measurement files from three different vendors: Bruker, Rigaku, and Pananalytical, we use the pre-trained Llama3 model to read the raw files and generate output that can be used to populate Pydantic BaseModels classes.

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
python3.9 -m venv .pyenv
source .pyenv/bin/activate
pip install -e .[dev]
```
