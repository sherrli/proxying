# proxying
Containerized Charles Proxy - record selenium driver interactions inside container

## use
```
git clone https://github.com/sherrli/proxying.git
```
Copy your charles license `com.xk72.charles.config` to `proxying` folder, make sure to set `<port>8888</port>`.
```
cd proxying
docker-compose build
docker-compose up -d
docker exec -it charles-proxy python3 script.py
```
Do `docker ps -a` and get container id of `portal-test` container.
```
docker cp <container-id>:/home/ubuntu/test_allsides.chlsj .
```
Now you can analyze `test_allsides.chlsj` results on your local machine.
