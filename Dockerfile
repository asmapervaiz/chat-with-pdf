FROM python
WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt
RUN apt-get update
# Expose the FastAPI default port
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


