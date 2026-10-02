apt-get update
apt-get upgrade -y
systemctl status nginx
systemctl restart nginx
ufw status
ufw allow 80/tcp
ufw allow 443/tcp
tail -f /var/log/nginx/access.log
mysql -u root -p
mysqldump -u root -p university_db > backup.sql
ls -la /var/www/html
nano /etc/nginx/sites-available/default
systemctl reload nginx
df -h
free -m
uptime
last
who
netstat -tulpn
ps aux