#!/bin/bash

# Get HTTP status code using curl
status_code=$(curl -o /dev/null -s -w "%{http_code}" https://www.guvi.in)

# Print status code
echo "HTTP Status Code: $status_code"

# Check success/failure
if [[ "$status_code" -ge 200 && "$status_code" -lt 300 ]]; then
    echo "✅ Success: Website is reachable."
else
    echo "❌ Failure: Website is not reachable."
fi
