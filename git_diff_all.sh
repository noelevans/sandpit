#!/bin/bash

git status -s | awk '{print substr($2, 1)}' | xargs -I{} git diff "{}"

