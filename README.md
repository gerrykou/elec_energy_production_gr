# elec_energy_production_gr
Greek Electrical Energy Grid Production per Fuel and Unit

## Run Tests in Docker-compose
```
docker-compose -f ./docker-compose.yml build
docker-compose -f ./docker-compose.yml run test
docker-compose -f ./docker-compose.yml down
```

## Run Tests in Docker
```
docker build . -t elec-energy-production-gr:latest
docker run elec-energy-production-gr:latest
```
## Run app in Docker
```
docker run --rm -it -v ${PWD}/data:/app/data elec-energy-production-gr:latest python3 src/app.py
```

## Debug Docker
```
docker run --rm -it -v ${PWD}/data:/app/data elec-energy-production-gr:latest bash 
```

## Run Locally

### Setup the Virtual Environment
```
python3 -m virtualenv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```   

### Run Tests
```
pytest -rP
```
### Run the app
```
python3 src/app.py
```
