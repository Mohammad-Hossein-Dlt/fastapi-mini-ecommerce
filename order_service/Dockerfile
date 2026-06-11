FROM python:3.14-alpine3.23

WORKDIR /app

COPY ./sharedlib ./sharedlib
COPY ./order_service .

RUN echo "https://mirror.arvancloud.ir/alpine/v3.23/main" > /etc/apk/repositories
RUN echo "https://mirror.arvancloud.ir/alpine/v3.23/community" >> /etc/apk/repositories
RUN apk update

RUN pip install --upgrade pip
RUN pip install uv
RUN uv sync --upgrade --no-cache
RUN uv pip install ./sharedlib

EXPOSE 80

ENTRYPOINT ["sh", "run.sh"]