# docker build -t python-selenium-chrome .
# docker run -dit --name scraping-gallito python-selenium-chrome
FROM python:3.12-slim

RUN apt-get update && apt-get install -y wget unzip git

WORKDIR /app

RUN git clone -b main https://github.com/hentype85/Python-Selenium-Docker.git .
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN wget -c https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb

RUN apt-get clean

CMD ["python", "main.py"]