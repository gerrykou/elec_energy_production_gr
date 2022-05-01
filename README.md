# elec_energy_production_gr
Electrical energy grid production per fuel and unit

## Run Tests in Docker
```
docker build . -t elec-energy-production-gr:latest
docker run elec-energy-production-gr:latest
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
