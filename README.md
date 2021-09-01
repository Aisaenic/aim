# AIM
## Description
AIM is an investigative machine meant for intel-gathering purposes on an IP, CIDR range, or domain. It is meant to aggregate data from different sources and provide a succint report for users.

## Usage
Build Docker Image:
```bash
docker build -t ${image_name} .
```
Check Docker Image With Set Name Exists:
```bash
docker images
```
Run Docker Image:
```bash
docker run -it --rm ${image_name} [OPTIONS] TARGETS
```
