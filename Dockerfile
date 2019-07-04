FROM alpine
COPY ** /vectorizer/
RUN apk update && apk add python3 build-base python3-dev zlib-dev libpng-dev libpng-dev jpeg-dev gcc curl && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py && cd /vectorizer/ && pip install -r requirements.txt
WORKDIR /vectorizer/
EXPOSE 8000/tcp
EXPOSE 8000/udp
CMD ["gunicorn", "myapp:app"]