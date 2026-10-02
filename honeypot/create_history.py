import os

os.makedirs('/cowrie/cowrie-git/honeyfs/root', exist_ok=True)

history = """apt-get update
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
"""

with open('/cowrie/cowrie-git/honeyfs/root/.bash_history', 'w') as f:
    f.write(history)

print('Bash history created successfully')