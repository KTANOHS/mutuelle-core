#!/bin/bash
daphne -b 0.0.0.0 -p 8000 mutuelle_core.asgi:application \
    --access-log - \
    --proxy-headers