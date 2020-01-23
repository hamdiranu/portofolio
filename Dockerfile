
FROM python:3.6.5
MAINTAINER Your Name "hamdi@alterra.id"
RUN mkdir -p /demo
COPY . /demo
RUN pip install -r /demo/requirements.txt
# ENV FLASK_ENV        = FLASK_ENV_LOCAL
# ENV THIS_U_NAME      = THIS_U_NAME_LOCAL
# ENV THIS_PASSWORD    = THIS_PASSWORD_LOCAL
# ENV THIS_ENDPOINT    = THIS_ENDPOINT_LOCAL
# ENV THIS_DB_TEST     = THIS_DB_TEST_LOCAL
# ENV THIS_DB_DEV      = THIS_DB_DEV_LOCAL
WORKDIR /demo
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
