FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src ./src

# Copy the entrypoint script into the container
COPY entrypoint.sh /code

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
# Run the entrypoint script when the container starts
CMD ["./entrypoint.sh"]
