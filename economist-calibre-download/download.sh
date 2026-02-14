docker build -t calibre-cli .

docker run --rm \
  -v ./:/output \
  --env-file docker.env \
  calibre-cli \
  "The Economist.recipe" \
  /output/economist.epub \
  --username "$ECONOMIST_USERNAME" \
  --password "$ECONOMIST_PASSWORD"

docker run --rm \
  -v ./:/output \
  --env-file docker.env \
  --entrypoint /bin/bash \
  calibre-cli \
  -c 'calibre-smtp \
    --relay smtp.gmail.com \
    --port 587 \
    --username "$EMAIL_ADDRESS" \
    --password "$EMAIL_PASSWORD" \
    --encryption-method TLS \
    --subject "Economist" \
    "$EMAIL_ADDRESS" \
    "$KINDLE_EMAIL" \
    "Your Economist edition" \
    --attachment /output/economist.mobi'
