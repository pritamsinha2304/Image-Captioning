""" Module for storing file paths """

from dataclasses import dataclass
import os


@dataclass
class FilePaths:
    """Stores all the config filepath as `dataclass`
    """
    config_fp: str = os.path.join("models", "config.json")
    merges_fp: str = os.path.join("models", "merges.txt")
    vocab_fp: str = os.path.join("models", "vocab.json")
    tokenizer_config_fp: str = os.path.join("models",
                                            "tokenizer_config.json")
    feature_config_fp: str = os.path.join("models",
                                          "preprocessor_config.json")
    model_fp: str = os.path.join("models", "pytorch_model.bin")
    processor_config_fp: str = os.path.join("models",
                                            "processor_config.json")
    model_generate_config_fp: str = os.path.join("models",
                                                 "model_generate_config.json")
