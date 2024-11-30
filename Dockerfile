FROM python:3.9

WORKDIR /build

ADD requirements.txt .
RUN pip install -r requirements.txt

COPY source ./source
ADD main.pyw .

#ENTRYPOINT ["python", "./main.pyw"]
#ENTRYPOINT [ "python", "-m", "unittest", "discover", "-s", "./source/tests", "-p", "'*.py'"]
ENTRYPOINT [ "python", "-m", "unittest"]
