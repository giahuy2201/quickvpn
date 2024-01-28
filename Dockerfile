FROM python:alpine
WORKDIR /quickvpn
COPY pyproject.toml poetry.lock .
RUN apk update && \
    apk add gcc python3-dev libc-dev libffi-dev && \
    pip install poetry && \
    poetry install --no-root --only main && \
    apk del --purge gcc python3-dev libc-dev libffi-dev && \
    rm -rf /tmp/* $HOME/.cache
COPY ./app /quickvpn/app
CMD [ "poetry","run","uvicorn","app.main:app","--proxy-headers","--host", "0.0.0.0","--port","80" ]