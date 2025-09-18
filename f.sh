#!/bin/bash
black -l 120 --exclude migrations .
isort --gitignore --skip-glob  migrations .
mypy .
