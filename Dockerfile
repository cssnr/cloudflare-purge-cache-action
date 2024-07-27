FROM python:3.11-alpine

RUN python -m pip install requests

COPY src/main.py /main.py

ENTRYPOINT ["python", "/main.py"]
