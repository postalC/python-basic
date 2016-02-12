
# python-basic
Python Basic

## How to run
`ensure your environment is setup correctly`

```
sudo yum -y install gcc gcc-c++ python-devel blas-devel lapack-devel
sudo yum -y install numpy numpy-f2py scipy

pip install -r requirements.txt

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
docker build -t sbuzz3:0.1 Dockerfile3 .

docker create -t -i \
-p 5000:5000 \
-h sbuzz \
--name sbuzz3 \
sbuzz3:0.1
```
