#!/bin/bash
HOST="guvi.com"
PORT=9000

if nc -zvw3 $HOST $PORT 2>&1 | grep -q succeeded; then
  echo "✅ Port $PORT is open on $HOST"
else
  echo "❌ Port $PORT is closed or unreachable on $HOST"
fi
