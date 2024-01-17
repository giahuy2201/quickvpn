# quickvpn

A quick 'n dirty way to deploy your on-demand vpn server on Linode.
## Development
```
pipenv install
export PYTHONPATH=$PWD/app
pipenv run uvicorn main:app --reload
```
## Usage
| Environment variables | Function |
| :----: | --- |
| `LINODE_TOKEN` | Linode API token |
| `SSH_PASSWD` | A good password to your Linode VPN server |
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
      - 7080:80
    environment:
      - LINODE_TOKEN=
      - SSH_PASSWD=
      - CF_TOKEN=
      - CF_DOMAIN=
      - CF_ZONEID=
```
### docker cli
```bash
docker run -d \
  --name=quickvpn \
  -p 7080:80 \
  -v /path/to/quickvpn/config:/config \
  -e LINODE_TOKEN='YOUR_LINODE_TOKEN' \
  -e SSH_PASSWD='YOUR_SSH_PASSWD' \
  -e CF_TOKEN='YOUR_CF_TOKEN' \
  -e CF_DOMAIN='YOUR_CF_DOMAIN' \
  -e CF_ZONEID='YOUR_CF_ZONEID' \
  --restart unless-stopped \
  giahuy2201/quickvpn:latest
```
