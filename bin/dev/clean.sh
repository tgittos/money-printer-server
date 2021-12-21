#!/bin/bash

echo "Removing __pycache__, .pyc and .pyo files..."
find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
echo "Done"