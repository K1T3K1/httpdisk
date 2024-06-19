FROM python:3.11.3 as base

FROM base AS builder

COPY ./src/requirements.txt requirements.txt
RUN pip install --no-cache-dir --no-warn-script-location -r requirements.txt
COPY . .
RUN pip install --no-cache-dir --no-warn-script-location --no-deps .

WORKDIR ./src/httpdisk

CMD ["httpdisk"]
