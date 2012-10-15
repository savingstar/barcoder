for i in `ps aux | grep [n]ginx | awk {'print $2'}`
do
	kill -9 $i
done
/opt/nginx/sbin/nginx

kill `ps aux | grep [w]ebfront | awk {'print $2'}`; nohup ./webfront.py &
