#!/usr/bin/env bash

uv run -m src.main

cd public && python -m http.server 8888

