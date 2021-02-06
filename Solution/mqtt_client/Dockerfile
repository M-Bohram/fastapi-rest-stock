FROM python
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY main.py main.py
COPY . .
CMD ["python", "main.py"]