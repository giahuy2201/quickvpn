FROM python:alpine
WORKDIR /quickvpn
COPY ./requirements.txt /quickvpn/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /quickvpn/requirements.txt
COPY ./app /quickvpn/app
CMD [ "uvicorn","app.main:app","--proxy-headers","--host", "0.0.0.0","--port","80" ]