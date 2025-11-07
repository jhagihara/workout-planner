FROM ubuntu:latest
LABEL authors="jessh"

ENTRYPOINT ["top", "-b"]