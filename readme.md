# Backer Upper
A utility to recursively back up local files to an S3 bucket *if* the local files are newer than what exists in the bucket *or* do not exist in the bucket.

Setup:
- `cp .env.example .env`
- fill in the env vars
- `pip install requirements.txt`

Run:
`python3 backup.py`

---

## Env vars:

### `AWS_ACCESS_KEY_ID`
In the AWS Console: *your username* > Security Credentials > Access keys (access key ID and secret access key) > Create New Access Key. Or use the access key ID you've already acquired.

---

### `AWS_SECRET_ACCESS_KEY`
In the AWS Console: *your username* > Security Credentials > Access keys (access key ID and secret access key) > Create New Access Key. Or use the secret access key you've already acquired.

---

### `BUCKET_NAME`
Name of your s3 bucket

---

### `BASE_DIR`
On your local machine, the full path *up to* the starting directory you want to back up.

#### Example:
On your local disk:
<span style="color:red">/Users/my_home_dir/my/base/dir/</span><span style="color:green">this/is/my/content.txt</span>

In .env: `BASE_DIR=/Users/my_home_dir/my/base/dir/`

What appears in your S3 bucket:
```
this
└───is
    └───my
        └───content.txt
```

---

### `TIMEZONE`
The [tz database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) name for your timezone (ex. America/Los_Angeles)

---

### Notes
- Deleteing a local file will not delete it from S3
- Storing AWS credentials in plain text is really good and stuff
