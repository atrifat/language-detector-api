# language-detector-api

A Simple PoC (Proof of Concept) of Language Detector API Server. A Lightweight Compatible API Endpoint with LibreTranslate.

## Getting Started

You can start by cloning this repository to run or modify it locally

```
git clone https://github.com/atrifat/language-detector-api
cd language-detector-api
```

Create virtual environment using venv, pyenv, or conda. This is an example using venv to create and activate the environment:

```
python3 -m venv venv
source venv/bin/activate
```

install its dependencies

```
pip install -U -r requirements.txt
```

and run it using command

```
python3 app.py
```

You can also copy `.env.example` to `.env` file and change the environment value based on your needs before running the app.

There is also Dockerfile available if you want to build docker image locally. If you don't want to build docker image locally, you can use the published version in [ghcr.io/atrifat/language-detector-api](https://github.com/atrifat/language-detector-api/pkgs/container/language-detector-api).

Run it:

```
docker run --init --env-file .env -p 5000:5000 -it ghcr.io/atrifat/language-detector-api
```

or run it in the background (daemon):

```
docker run --init --env-file .env -p 5000:5000 -it --name language-detector-api -d ghcr.io/atrifat/language-detector-api
```

If you want to test the API server, you can use GUI tools like [Postman](https://www.postman.com/) or using curl.

```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"api_key":"your_own_api_key_if_you_set_them", "q":"hello world good morning"}' \
  http://localhost:5000/detect
```

The result of classification will be shown as follow:

```
[{"confidence":100.0,"language":"en"}]
```

## License

MIT License

Copyright (c) 2024 Rif'at Ahdi Ramadhani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Author

Rif'at Ahdi Ramadhani (atrifat)
