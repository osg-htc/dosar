This website is built using [MKdocs](https://www.mkdocs.org/).

### Adding Pages

[https://www.mkdocs.org/getting-started/#adding-pages](https://www.mkdocs.org/getting-started/#adding-pages)

### Development

You can use the following commands to run the website locally so that you can preview your changes before
you push them to git. 

### Docker

```shell
docker run --rm -it -p 8001:8001 -v ${PWD}:/docs squidfunk/mkdocs-material
```

ARM
```shell
docker run --rm -it -p 8000:8000 -v  ${PWD}:/docs ghcr.io/afritzler/mkdocs-material
```

