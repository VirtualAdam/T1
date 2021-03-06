from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.models import User, Post, Times
from app.translate import translate
from app.bar import bp
import subprocess
import paho.mqtt.publish as publish


switch1="sw1"
switch2="sw2" 
switch3="sw3"
switch4="sw4"
switch5="sw5"
door1 = 'garagedoor1'
door2 = 'garagedoor2'

outlet1_on = "1332531"
outlet1_off = "1332540"
outlet2_on = "1332675"
outlet2_off = "1332684"
outlet3_on = "1332995"
outlet3_off = "1333004"
outlet4_on = "1334531"
outlet4_off = "1334540"
outlet5_on = "1340675"
outlet5_off = "1340684"

gateway = '192.168.1.7'

tel = {'jack': 4098, 'sape': 4139}


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/switches', methods=['GET', 'POST'])
@login_required
def switches():
    return render_template('switches.html')
@bp.route('/switches/<deviceName>/<action>')
def do(deviceName, action):
    if deviceName == "switch1":
        actuator = switch1
        if action == "on":
            flash(_(actuator+' on'))
            publish.single("switches", outlet1_on, hostname=gateway, qos=0)
        if action == "off":
            flash(_(actuator+' off'))
            publish.single("switches", outlet1_off, hostname=gateway, qos=0)
    if deviceName == "switch2":
        actuator = switch2
        if action == "on":
            flash(_(actuator+' on'))
            publish.single("switches", outlet2_on, hostname=gateway, qos=0)
        if action == "off":
            flash(_(actuator+' off'))
            publish.single("switches", outlet2_off, hostname=gateway, qos=0)
    if deviceName == "switch3":
        actuator = switch3
        if action == "on":
            flash(_(actuator+' on'))
            publish.single("switches", outlet3_on, hostname=gateway, qos=0)
        if action == "off":
            flash(_(actuator+' off'))
            publish.single("switches", outlet3_off, hostname=gateway, qos=0)
    if deviceName == "switch4":
        actuator = switch4
        if action == "on":
            flash(_(actuator+' on'))
            publish.single("switches", outlet4_on, hostname=gateway, qos=0)
        if action == "off":
            flash(_(actuator+' off'))
            publish.single("switches", outlet4_off, hostname=gateway, qos=0)
    if deviceName == "switch5":
        actuator = switch5
        if action == "on":
            flash(_(actuator+' on'))
            publish.single("switches", outlet5_on, hostname=gateway, qos=0)
        if action == "off":
            flash(_(actuator+' off'))
            publish.single("switches", outlet5_off, hostname=gateway, qos=0)
    if deviceName == "door1":
        actuator = door1
        if action == "on":
            flash(_(actuator+' pressed'))
            publish.single("garagedoor", 'door1', hostname=gateway, qos=0)
    if deviceName == "door2":
        actuator = door2
        if action == "on":
            flash(_(actuator+' pressed'))
            publish.single("garagedoor", 'door2', hostname=gateway, qos=0)
    return render_template('switches.html', title=_('Switches'))

