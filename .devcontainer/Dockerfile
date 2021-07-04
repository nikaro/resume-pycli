FROM nikaro/alpine-dev

# add local user bin to path
ENV PATH "${HOME}/go/bin:${PATH}"

RUN \
    # install required tools
    sudo apk add \
        jq \
        go \
        py3-pip \
        wkhtmltopdf \
        xorg-server \
        # to avoid building cryptography package
        py3-cryptography \
        && \
    python3 -m pip install --user poetry && \
    go install github.com/git-chglog/git-chglog/cmd/git-chglog@latest && \
    :
