FROM python:alpine
WORKDIR /quickvpn
COPY ./requirements.txt /quickvpn/requirements.txt
RUN apk update && \
    apk add gcc python3-dev libc-dev libffi-dev && \
    pip install --no-cache-dir --upgrade -r /quickvpn/requirements.txt && \
    apk del --purge gcc python3-dev libc-dev libffi-dev && \
    rm -rf /tmp/* $HOME/.cache
COPY ./app /quickvpn/app
CMD [ "uvicorn","app.main:app","--proxy-headers","--host", "0.0.0.0","--port","80" ]