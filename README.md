
# python-basic
Python Basic

## How to run

```
pip install -r lib.txt

python sbuzz.py

# go to http://localhost:5000/
```

## Build Docker with Python2
```
docker build -t sbuzz2:0.1 -f Dockerfile2 .

docker create -t -i \
-p 5000:5000 \
-h sbuzz \
--name sbuzz2 \
sbuzz2:0.1
```


## Build Docker with Python3
```
docker build -t sbuzz:0.1 .

docker create -t -i \
-p 5000:5000 \
-h sbuzz \
--name sbuzz \
sbuzz:0.1
```