FROM nikaro/alpine-dev

RUN \
    # install required tools
    sudo apk add \
        jq \
        py3-pip \
        wkhtmltopdf \
        xorg-server \
        # to avoid building cryptography package
        py3-cryptography \
        && \
    python3 -m pip install --user poetry && \
    :
