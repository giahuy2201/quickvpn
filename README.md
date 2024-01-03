# quickvpn

A quick 'n dirty way to deploy your on-demand vpn server on Linode.
## Development
```
pipenv install
export PYTHONPATH=$PWD/app
pipenv run uvicorn main:app --reload
```
## Usage
Rename `config/sample.env` to `.env` with your parameters
| Parameter | Function |
| :----: | --- |
| `LINODE_TOKEN` | Linode API token |
| `CF_TOKEN` | Cloudflare API token with permission to edit zone |
| `CF_DOMAIN` | Your Cloudflare DNS record to assign to your server IP e.g. vpn.example.com |
| `CF_ZONEID` | Cloudflare ZoneId of your domain |
### docker-compose (recommended)
```bash
---
version: '3.5'
services:
  quickvpn:
    image: giahuy2201/quickvpn:latest
    container_name: quickvpn
    restart: unless-stopped
    volumes:
      - ./config:/quickvpn/config
    ports:
      - 8000:80
```
### docker cli
```bash
docker run -d \
  --name=quickvpn \
  -p 8000:80 \
  -v /path/to/quickvpn/config:/config \
  --restart unless-stopped \
  giahuy2201/quickvpn:latest
```
