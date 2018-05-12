# Metaswitch Tinder

## Development instructions

You will need a postgres database to test against and set the DATABASE_URL environment variable to be its URI.
If you work out how to do that, please submit an MR to document it in this README.

Linux:
```
yum install -y python36
python36 setup.py develop
python36 metaswitch_tinder/main.py example_config.py
```
