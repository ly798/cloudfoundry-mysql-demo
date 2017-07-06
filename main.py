"""
A simple app to show mysql service integration.
"""
from flask import Flask
import os
import json
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))

# Get mysql credentials, env demo:
#{
# "VCAP_SERVICES": {
#  "p-mysql": [
#   {
#    "credentials": {
#     "hostname": "10.0.2.112",
#     "jdbcUrl": "jdbc:mysql://10.0.2.112:3306/cf_70820e38_a40d_492d_9e04_523b9623f20a?user=1WMlxsSk7CbaPVBr\u0026password=mt8Hzzi1GWx5a13h",
#     "name": "cf_70820e38_a40d_492d_9e04_523b9623f20a",
#     "password": "mt8Hzzi1GWx5a13h",
#     "port": 3306,
#     "uri": "mysql://1WMlxsSk7CbaPVBr:mt8Hzzi1GWx5a13h@10.0.2.112:3306/cf_70820e38_a40d_492d_9e04_523b9623f20a?reconnect=true",
#     "username": "1WMlxsSk7CbaPVBr"
#    },
#    "label": "p-mysql",
#    "name": "mysql_01",
#    "plan": "100mb",
#    "provider": null,
#    "syslog_drain_url": null,
#    "tags": [
#     "mysql"
#    ],
#    "volume_mounts": []
#   }
#  ]
# }
#}
if 'VCAP_SERVICES' in os.environ:
    services = json.loads(os.getenv('VCAP_SERVICES'))
    mysql_env = services['p-mysql'][0]['credentials']
else:
    mysql_env = dict(hostname='localhost', port=6379, password='')
mysql_env['port'] = int(mysql_env['port'])

# Connect to mysql
Base = declarative_base()
engine = create_engine('mysql+pymysql://%s:%s@%s:3306/%s' %
                       (mysql_env['username'], mysql_env['password'],
                        mysql_env['hostname'], mysql_env['name']))
DBSession = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


# Define model
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))


@app.route('/')
def index():
    if DBSession:
        session = DBSession()
        users = session.query(User).all()
        session.close()
        return '%s\n' % '\n'.join('id: %s, name: %s' % (user.id, user.name)
                                  for user in users)
    else:
        return 'No connection available!'


@app.route('/<uid>')
def get_name(uid):
    if DBSession:
        session = DBSession()
        user = session.query(User).filter(User.id == int(uid)).one()
        session.close()
        return "id: %s, name: %s\n" % (user.id, user.name)
    else:
        abort(503)


@app.route('/<uid>/<name>')
def add_user(uid, name):
    if DBSession:
        session = DBSession()
        new_user = User(id=int(uid), name=name)
        session.add(new_user)
        session.commit()
        session.close()
        return "Insert:\n - id: %s, name: %s\n" % (uid, name)
    else:
        abort(503)


if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)
