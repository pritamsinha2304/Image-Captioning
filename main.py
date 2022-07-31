""" Main File """

import logging
import logging.config
import io

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware

from starlette.routing import Mount
from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

import yaml
import uvicorn
from transformers.utils import logging as transformers_logging
import numpy as np
import magic
from PIL import Image

from schema import FormData

from models_utils.model_initializer import ModelInitializer
from models_utils.main_processor import MainProcessor


# Loading Log YAML file
with open('log_config.yaml', 'r', encoding='UTF-8') as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)

# Setting transformer verbosity level
transformers_logging.set_verbosity_error()

logging.info("Main Files Loading....")

routes = [
    Mount("/home", StaticFiles(directory="front/dist", html=True),
          name='templates'),
    Mount("/assets", StaticFiles(directory="front/dist/assets"),
          name='static')
]

middleware = [
    Middleware(CORSMiddleware,
               allow_origins=['*'],
               allow_credentials=True,
               allow_methods=["*"],
               allow_headers=["*"])
]

app = FastAPI(routes=routes,
              middleware=middleware,
              docs_url=None,
              redoc_url=None)


# Initialize the Model
try:
    feature_extractor, tokenizer, model = ModelInitializer()()
    logging.info("Feature Extractor, Tokenizer and Model Loaded Successfully")
except ImportError as imp_err:
    logging.error("Exception encountered in ModelProcessorCaller(): %s",
                  imp_err)

# Initialize the Main Processor
try:
    main_processor = MainProcessor(feature_extractor=feature_extractor,
                                   tokenizer=tokenizer,
                                   model=model)
    logging.info("Main Processor Loaded Successfully")
except ImportError as imp_err:
    logging.error("Exception encountered initializing Main Processor: %s",
                  imp_err)


@app.get('/', name='homepage')
async def get_data():
    """GET Request
    """
    return RedirectResponse(url='/home')


@app.post('/post', name='homepage_post')
async def post_data(file: FormData = Depends(FormData.as_form)):
    """POST request

    Args:
        request (Request): _description_
        file (FormData, optional):Defaults to Depends(FormData.as_form).
    """
    if not isinstance(file.imagefileinput, ValueError):
        try:
            # Read the uploaded file
            content = await file.imagefileinput.read()
            logging.info("%s uploaded successfully",
                         file.imagefileinput.filename)
        except OSError as os_err:
            logging.error("Error in reading file: %s", os_err)
            return {
                'response':
                    {
                        'error': str(os_err)
                    }
                }

        # Check the signature
        sig = magic.from_buffer(content, mime=True)
        if sig not in ['image/jpeg', 'image/png']:
            return {
                'response':
                    {
                        'error': str(os_err)
                    }
                }

        # Converting bytearray to array
        try:
            img = Image.open(io.BytesIO(content))
            logging.info("Image read successfully")
        except IOError as io_err:
            logging.error("Error encountered while reading io.BytesIO: %s",
                          str(io_err))
            return {
                'response':
                    {
                        'error': str(io_err)
                    }
                }
        # COnverting png to jpg, because png will have a 4th dimension which
        # indicates 'alpha channel'
        if sig == 'image/png':
            img = img.convert('RGB')

        img_arr = np.asarray(img)
        print(img_arr.shape)

        # Prediction
        preds = main_processor.process(img_arr=img_arr)
        logging.info("Image Captioning Done")
        return {
            'response':
                {
                    'success': str(preds[0])
                }
            }

    logging.error("Validation Error")
    return {
        'response':
            {
                'error': str(file.imagefileinput)
            }
        }


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    """Handles any HTTP Exception

    Returns:
        RedirectResponse
    """
    logging.error("Invalid URL entered: %s, with detail %s and status code %s",
                  str(request),
                  str(exc.detail),
                  str(exc.status_code))
    return RedirectResponse(url='/home')


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
