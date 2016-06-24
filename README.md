TempURL
=========

UbberSimple pub/sub service with only one purpose in mind.
To provide a 'safeish' way for applications to download configuration files or secrets during initialization.

Deployment:
============

    docker-compose up -d


Usage:
=========

    curl -H "Content-Type: application/json" -X POST  -d '{"tempurl":"kasjdfkjsdf123", "data": "kjsdfkjsdf" }' http://127.0.0.1:6222/upload
    OK

    curl -H "Content-Type: application/json" -GET  -d '{"tempurl":"kasjdfkjsdf123" }' http://127.0.0.1:6222/download
    kjsdfkjsdf

    curl -H "Content-Type: application/json" -GET  -d '{"tempurl":"kasjdfkjsdf123" }' http://127.0.0.1:6222/download
    Nothing here to see

