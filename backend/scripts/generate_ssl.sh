#!/bin/bash
set -e

# Create SSL directory if it doesn't exist
mkdir -p deployment/nginx/ssl

# Generate SSL certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout deployment/nginx/ssl/cyber-defense.key \
    -out deployment/nginx/ssl/cyber-defense.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=cyber-defense.com"

# Generate Diffie-Hellman parameters
openssl dhparam -out deployment/nginx/ssl/dhparam.pem 2048

# Set proper permissions
chmod 600 deployment/nginx/ssl/cyber-defense.key
chmod 644 deployment/nginx/ssl/cyber-defense.crt
chmod 644 deployment/nginx/ssl/dhparam.pem

echo "SSL certificates generated successfully" 