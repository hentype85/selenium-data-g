# Python-Selenium-Docker

### Entorno virtual de python
crear: `python -m venv .`
```
C:\Users\...\Desktop\Python-Selenium-Docker> python -m venv . 
```
activar: `.\scripts\activate`
```
C:\Users\...\Desktop\Python-Selenium-Docker> .\Scripts\activate 
```
desactivar: `deactivate`
```
(Python-Selenium-Docker) PS C:\Users\...\Desktop\Python-Selenium-Docker> deactivate
```
crear requirements.txt:
```
pip freeze > requirements.txt
```

### Dockerfile
```
docker build -t python-selenium-chrome .
docker run -dit --name scraping-gallito python-selenium-chrome
```