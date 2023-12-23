# quickvpn

A quick-and-dirty way to deploy your on-demand vpn server on Linode.

```
pipenv install
export PYTHONPATH=$PWD/app
pipenv run uvicorn main:app --reload
```