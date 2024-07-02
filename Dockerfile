# Use the official Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /home/rannia/Projects

# Copy the current directory contents into the container at /home/rannia/Projects
COPY . /home/rannia/Projects

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "dashboard1.py"]

