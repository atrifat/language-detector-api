import os
from dotenv import load_dotenv
import pandas as pd
from flask import Flask, request, jsonify
import datetime
import logging
import functools

from fast_langdetect import detect_multilingual
from langdetect import detect_langs

load_dotenv()

ENABLE_API_TOKEN = os.getenv("ENABLE_API_TOKEN", "false") == "true"
API_TOKEN = os.getenv("API_TOKEN", "")
APP_ENV = os.getenv("APP_ENV", "production")
LISTEN_HOST = os.getenv("LISTEN_HOST", "0.0.0.0")
LISTEN_PORT = os.getenv("LISTEN_PORT", "5000")
LANGUAGE_DETECTION_MODEL = os.getenv("LANGUAGE_DETECTION_MODEL", "langdetect")
LOW_MEMORY_MODE = os.getenv("LOW_MEMORY_MODE", "false") == "true"

APP_VERSION = "0.0.1"

# Setup logging configuration
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
if APP_ENV == "production":
    logging.basicConfig(
        level=logging.INFO,
        datefmt=LOGGING_DATE_FORMAT,
        format=LOGGING_FORMAT,
    )
else:
    logging.basicConfig(
        level=logging.DEBUG,
        datefmt=LOGGING_DATE_FORMAT,
        format=LOGGING_FORMAT,
    )

if ENABLE_API_TOKEN and API_TOKEN == "":
    raise Exception("API_TOKEN is required if ENABLE_API_TOKEN is enabled")

app = Flask(__name__)


def is_valid_api_key(api_key):
    if api_key == API_TOKEN:
        return True
    else:
        return False


def api_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if ENABLE_API_TOKEN:
            if request.json:
                api_key = request.json.get("api_key")
            else:
                return {"message": "Please provide an API key"}, 400
            # Check if API key is correct and valid
            if request.method == "POST" and is_valid_api_key(api_key):
                return func(*args, **kwargs)
            else:
                return {"message": "The provided API key is not valid"}, 403
        else:
            return func(*args, **kwargs)

    return decorator


def perform_detect_language(query):
    result = []
    temp_result = []
    default_result = {"confidence": 0, "language": "en"}

    try:
        temp_result = (
            detect_multilingual(query, low_memory=LOW_MEMORY_MODE)
            if LANGUAGE_DETECTION_MODEL == "fast_langdetect"
            else detect_langs(query)
        )
        for i, item in enumerate(temp_result):
            score = (
                round(item["score"] * 100, 2)
                if LANGUAGE_DETECTION_MODEL == "fast_langdetect"
                else round(item.prob * 100, 2)
            )
            language = (
                item["lang"]
                if LANGUAGE_DETECTION_MODEL == "fast_langdetect"
                else item.lang
            )

            if score >= 1:
                result.append({"confidence": score, "language": language})

        if len(temp_result) == 0:
            result.append(default_result)

    except:
        result.append(default_result)
    finally:
        if len(result) == 0:
            result.append(default_result)

    return result


@app.errorhandler(Exception)
def handle_exception(error):
    res = {"error": str(error)}
    return jsonify(res)


@app.route("/detect", methods=["POST"])
@api_required
def predict():
    data = request.json
    q = data["q"]
    start_time = datetime.datetime.now()
    result = perform_detect_language(q)
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    logging.debug("elapsed detection time: %s", str(elapsed_time))
    return jsonify(result)


@app.route("/", methods=["GET"])
def index():
    response = {"message": "Use /detect route to get detection result"}
    return jsonify(response)


@app.route("/app_version", methods=["GET"])
def app_version():
    response = {"message": "This app version is ".APP_VERSION}
    return jsonify(response)


if __name__ == "__main__":
    app.run(host=LISTEN_HOST, port=LISTEN_PORT)
