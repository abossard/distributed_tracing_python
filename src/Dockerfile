FROM python:3
ARG MODULE=gateway
WORKDIR /usr/src/app
EXPOSE 8080

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV MODULE ${MODULE}
CMD gunicorn -w 4 --bind 0.0.0.0:8080 $MODULE:app
