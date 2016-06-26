[![Requirements Status](https://requires.io/github/Azulinho/tempURL/requirements.svg?branch=master)](https://requires.io/github/Azulinho/tempURL/requirements/?branch=master)
[![Build Status](https://travis-ci.org/Azulinho/tempURL.svg?branch=master)](https://travis-ci.org/Azulinho/tempurl)
[![Coverage Status](https://coveralls.io/repos/azulinho/tempurl/badge.svg?branch=master&service=github)](https://coveralls.io/github/azulinho/tempurl?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a787afaa255e496886e9d25ac30fe20c)](https://www.codacy.com/app/mail_34/tempURL?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Azulinho/tempURL&amp;utm_campaign=Badge_Grade)



TempURL
=========

UbberSimple pub/sub service with only one purpose in mind.

To provide a 'safeish' way for applications to download configuration files or secrets during initialization.

Deployment:
============

    docker-compose up -d


Usage:
=========

    curl -X POST -F file=@config.ini 'http://127.0.0.1:6222/api?tempurl=kjadfadsf&ttl=3600'
    OK

    curl -X GET http://127.0.0.1:6222/api?tempurl=kjadfadsf
    [inifile]
    x=y

    curl -X GET http://127.0.0.1:6222/api?tempurl=kjadfadsf
    NOT FOUND

    curl -X POST -F file=@config.ini 'http://127.0.0.1:6222/api?tempurl=kjadfadsf&ttl=1'
    OK

    sleep 2

    curl -X GET http://127.0.0.1:6222/api?tempurl=kjadfadsf
    NOT FOUND
