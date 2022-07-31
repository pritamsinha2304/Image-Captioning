"""Processes the uploaded data and return result
"""

from .json_to_dict import JsonToDict
from .filepaths import FilePaths


class MainProcessor:
    """Processes the data and return the result
    """
    def __init__(self, feature_extractor, tokenizer, model) -> None:
        self.feature_extractor = feature_extractor
        self.tokenizer = tokenizer
        self.model = model

    def __get_pixel_values(self, img_arr):
        features = self.feature_extractor(images=[img_arr],
                                          return_tensors='pt')
        pixels_tensor = features.pixel_values
        return pixels_tensor

    def __get_model_generate_config(self):
        return JsonToDict(FilePaths.model_generate_config_fp).convert()

    def __get_output_ids(self, pixels_tensor):
        output_ids = self.model.generate(pixels_tensor,
                                         **self.__get_model_generate_config())
        return output_ids

    def __get_decoded_result(self, output_ids):
        preds = self.tokenizer.batch_decode(output_ids,
                                            skip_special_tokens=True)
        preds = [pred.strip() for pred in preds]
        return preds

    def process(self, img_arr):
        """Takes on image buffer and return the decoded result

        Args:
            image_buffer (_type_): _description_

        Returns:
            List[str]: Returns list of decoded result
        """
        pixels_tensor = self.__get_pixel_values(img_arr)
        output_ids = self.__get_output_ids(pixels_tensor=pixels_tensor)
        preds = self.__get_decoded_result(output_ids=output_ids)
        return preds
