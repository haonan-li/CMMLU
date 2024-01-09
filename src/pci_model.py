import asyncio
from pci_transgpt import pci_generate


class LLM:
    def __init__(self, model_name, model_key, **kwargs):
        self.model_name = model_name
        self.model_key = model_key
        self.kwargs = kwargs
        self.usr_contents = None

    def run(self, usr_contents):
        self.usr_contents = usr_contents
        return self.call_llm()

    def get_model_type(self):
        model_type = {
            **{k: "pci" for k in ["pci_transgpt"] },
        }
        if self.model_name in model_type:
            return model_type.get(self.model_name)
        raise ValueError(f"LLM model name not supported: '{self.model_name}'")

    def call_llm(self):
        generate_funcs = {
            "pci": pci_generate,
        }

        model_type = self.get_model_type()
        generate_func = generate_funcs.get(model_type)
        if generate_func:
            self.kwargs.update({
                'usr_contents': self.usr_contents,
                'model_name': self.model_name,
                'model_key': self.model_key
            })

            response = generate_func(**self.kwargs)
            return response

        raise KeyError(f"LLM model type not supported: '{model_type}'")


