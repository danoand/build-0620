**Start Flask App in the Background and Log to File**

`sudo nohup python3 app.py > log.txt 2>&1 &`

**Tail the Log File**

`tail -f log.txt`

**Pull the Latest Code from GitHub (remote git repo)**

`git pull https://github.com/danoand/build-0620.git`

**List the Process Id of the App Running on Port 5000**

`lsof -i :5000`

**Reload with an Updated Caddyfile to Allow CORS Requests**

```
cd /app/caddy
caddy reload --config Caddyfile
```
