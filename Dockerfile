FROM python:3.10 AS builder
WORKDIR /app
COPY requirements.txt .
RUN python3 -m venv .venv && .venv/bin/pip install --no-cache-dir -r requirements.txt
RUN python3 -m venv .venv && .venv/bin/pip3 install -U git+https://github.com/yihong0618/MiService

FROM python:3.10-slim

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY xiaogpt/ ./xiaogpt/
COPY xiaogpt.py .
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV XDG_CONFIG_HOME=/config
ENV XIAOGPT_PORT=9527
EXPOSE 9527
ENTRYPOINT [".venv/bin/python3","xiaogpt.py"]
