# dosar [![Build Status](https://travis-ci.org/opensciencegrid/dosar.svg?branch=master)](https://travis-ci.org/opensciencegrid/dosar)

### Development

```shell
docker run --rm -it -p 8001:8001 -v ${PWD}:/docs squidfunk/mkdocs-material
```

ARM
```shell
docker run --rm -it -p 8000:8000 -v  ${PWD}:/docs ghcr.io/afritzler/mkdocs-material
```

### Test Links Locally
 
```shell
# Build the site into /site directory
docker run --rm -v  ${PWD}:/docs ghcr.io/afritzler/mkdocs-material build
 O
# Test the links
docker run --rm -it \
  -v $(pwd)/documentation:/src \
  klakegg/html-proofer:3.19.2 \
  --allow-hash-href --check-html --empty-alt-ignore --disable-external
```
