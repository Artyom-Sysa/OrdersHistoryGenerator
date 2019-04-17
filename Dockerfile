FROM python:3.7.3-alpine3.9
 
COPY . .
    
RUN pip install -r ./requirements.txt 

CMD [ "python", "Launcher.py"]
