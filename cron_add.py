from app.models import Times
import sqlalchemy
from datetime import datetime
from app import db, create_app
from flask_login import current_user, login_user
from crontab import CronTab
import subprocess

sw3_on='python /home/pi/T1/tasks/sw3_on.py'
sw3_off='python /home/pi/T1/tasks/sw3_off.py'

def cron_job_setup(time,commandn):
	t= time.split(':')
	h=t[0]
	m=t[1]
	cron = CronTab(user='root')
	job1 = cron.new(command=commandn)
	job1.hour.on(int(h))
	job1.minute.on(int(m))
	cron.write()

def cron_me():
	data = subprocess.Popen(["crontab", "-r"], stdout=subprocess.PIPE).communicate()[0]
	#app = create_app()
	#app.app_context().push()
	recent_time = Times.query.order_by(sqlalchemy.desc(Times.timestamp)).first()
	t1 = recent_time.switch1on1
	cron_job_setup(t1,sw3_on)
	t2 = recent_time.switch1off1
	cron_job_setup(t2,sw3_off)
	t3 = recent_time.switch1on2
	cron_job_setup(t3,sw3_on)
	t4 = recent_time.switch1off2
	cron_job_setup(t4,sw3_off)
	print 'done'




