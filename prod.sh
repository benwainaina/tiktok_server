source .app_env/bin/activate
serviceName="tiktokfans"
pm2 stop $serviceName
pm2 delete $serviceName
pm2 start uvicorn --name $serviceName --interpreter python3 -- server:SERVER --host 0.0.0.0 --port 8003
