########################################################
# This is the dev Dockerfile for the client            #
# It assumes a mounted volume at /home/node/app that   #
# contains the content of client/                      #
# It should support hot code reloading as you develop  #
# in the codebase                                      #
########################################################

FROM node:16-alpine

# set working directory
WORKDIR /home/node/app
RUN chown -R node:node /home/node/app

# set the global node dir to be in the user dir
RUN mkdir /home/node/.npm-global
ENV PATH=/home/node/.npm-global/bin:$PATH
ENV NPM_CONFIG_PREFIX=/home/node/.npm-global
ENV NODE_OPTIONS=--max_old_space_size=8192

# copy package.jsons
COPY --chown=node:node package*.json .

# install dependencies
RUN npm -g config set user node
RUN npm install

# copy the app
COPY --chown=node:node . .

# add bins
COPY --chown=node:node ./bin/dev /home/node/app/bin

# expose the dev port
EXPOSE 3000
# expose styleguidist
EXPOSE 6060

# run as node user
USER node

# start app
ENTRYPOINT /home/node/app/bin/dev
