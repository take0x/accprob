FROM debian:latest

# Install dependencies
RUN apt-get update -y
RUN apt-get install -y curl wget gnupg

# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update the package list and install chrome
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable

# Prepare for installing Rye
ARG USERNAME=ryeuser
RUN useradd ${USERNAME} --create-home
USER ${USERNAME}
ENV RYE_HOME /home/${USERNAME}/.rye
ENV PATH ${RYE_HOME}/shims:${PATH}

# Install Rye
RUN curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash
RUN rye config --set-bool behavior.use-uv=true

WORKDIR $HOME/app
COPY . .
RUN rye sync --no-lock
