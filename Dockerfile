FROM  python:3-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 53/tcp
CMD ["python3", "index.py"] 