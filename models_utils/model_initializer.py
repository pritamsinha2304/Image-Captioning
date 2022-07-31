""" Initialize the Model """

from transformers import ViTFeatureExtractor, GPT2Tokenizer, \
    VisionEncoderDecoderModel, VisionEncoderDecoderConfig
from .filepaths import FilePaths
from .json_to_dict import JsonToDict


class ModelInitializer:
    """Initializes all the model files
    """
    def __init__(self) -> None:
        pass

    def __get_feature_extractor_config(self):
        return JsonToDict(FilePaths.feature_config_fp).convert()

    def initialize_feature_extractor(self):
        """Initliaze the Feature Extractor

        Returns:
            ViTFeatureExtractor
        """
        feature_extractor = ViTFeatureExtractor(
            **self.__get_feature_extractor_config()
            )
        return feature_extractor

    def __get_tokenizer_config(self):
        return JsonToDict(FilePaths.tokenizer_config_fp).convert()

    def initialize_tokenizer(self):
        """Initializes the Tokenizer

        Returns:
            GPT2Tokenizer
        """
        vocab_fp = FilePaths.vocab_fp
        merges_fp = FilePaths.merges_fp
        tokenizer = GPT2Tokenizer(vocab_file=vocab_fp,
                                  merges_file=merges_fp,
                                  **self.__get_tokenizer_config())
        return tokenizer

    def __get_model_config(self):
        return JsonToDict(FilePaths.config_fp).convert()

    def __initialize_model_config(self):
        model_config = VisionEncoderDecoderConfig(**self.__get_model_config())
        return model_config

    def initialize_model(self):
        """Initializes the Model

        Returns:
            VisionEncoderDecoderModel
        """
        model = VisionEncoderDecoderModel.from_pretrained(
            pretrained_model_name_or_path=FilePaths.model_fp,
            config=self.__initialize_model_config()
            )
        return model

    def __call__(self):
        """Initializes feature extractor, tokenizer and the model

        Returns:
            ViTFeatureExtractor, GPT2Tokenizer, VisionEncoderDecoderModel
        """
        feature_extractor, tokenizer, model =\
            self.initialize_feature_extractor(),\
            self.initialize_tokenizer(),\
            self.initialize_model()
        return feature_extractor, tokenizer, model
