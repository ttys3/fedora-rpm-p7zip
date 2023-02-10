#!/usr/bin/env bash

set -eou pipefail

fedpkg --release f37 --name p7zip mockbuild --enable-network

