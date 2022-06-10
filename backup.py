import boto3
import os
import time
import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.getenv('BASE_DIR')
TIMEZONE = os.getenv('TIMEZONE')
BUCKET_NAME = os.getenv('BUCKET_NAME')

session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
s3 = session.resource('s3')
s3_objects = {}
local_objects = {}

bucket = s3.Bucket(BUCKET_NAME)
for obj in bucket.objects.all():
    s3_objects[obj.key] = obj.last_modified

s3_keys = s3_objects.keys()

tz = datetime.datetime.now(pytz.timezone(TIMEZONE)).strftime('%z')

hours = int(tz[:-2])
fraction = float(tz[-2:]) / 60.0
fraction = fraction * -1 if tz.startswith('-') else fraction
tz_offset = float((hours + fraction) * -1 + 1)
tz_offset = 60 * 60 * (tz_offset)

for root, subdirs, files in os.walk(BASE_DIR):
    for file in files:
        f = os.path.join(root, file)
        f_local = f[len(BASE_DIR):].strip('/')
        t_remote = time.mktime(s3_objects[f_local].timetuple())
        t_local = os.path.getmtime(f) + tz_offset
        if (not f_local in s3_keys):
            print('adding:  ', f_local)
            s3.meta.client.upload_file(f, BUCKET_NAME, f_local)
        elif (t_remote < t_local):
            print('updating:', f_local)
            s3.meta.client.upload_file(f, BUCKET_NAME, f_local)
        else:
            print('ok:      ', f_local)
