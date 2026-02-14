FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Europe/London \
    CALIBRE_NO_NATIVE_FILEDIALOGS=1 \
    QT_QPA_PLATFORM=offscreen \
    QTWEBENGINE_DISABLE_SANDBOX=1 \
    QTWEBENGINE_CHROMIUM_FLAGS="--no-sandbox --disable-gpu --disable-dev-shm-usage"

# Pre-configure timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

# Install dependencies
RUN apt-get update && \
    apt-get install -y -qq --no-install-recommends \
    ca-certificates \
    wget \
    xz-utils \
    xdg-utils \
    libfreetype6 \
    libegl1 \
    libopengl0 \
    libglx0 \
    libgl1 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxkbcommon-x11-0 \
    libxcb-xinerama0 \
    libxcb-xinput0 \
    libfontconfig1 \
    libdbus-1-3 \
    libxcb-glx0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Download and install Calibre
RUN wget -nv https://download.calibre-ebook.com/linux-installer.sh && \
    sh linux-installer.sh install_dir=/opt/calibre && \
    rm linux-installer.sh

ENV PATH="/opt/calibre:${PATH}"

WORKDIR /output

ENTRYPOINT ["ebook-convert"]
