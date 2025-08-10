# Use an official Python runtime as a parent image
FROM python:3.11.13-bookworm

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install uv

# Copy the Streamlit application files into the container at /app
COPY . .
RUN uv pip install --system .

# Expose the port that Streamlit runs on (default is 8501)
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "src/TimeCard.py"]