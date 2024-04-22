# build:
#     cd server && docker build . -t track-viewer-server
#     cd client && docker build . -t track-viewer-client
YML=docker-compose.yml
ifneq ($(shell docker info --format '{{json .SecurityOptions}}'| grep -w rootless),)
    USERID=0
    GROUPID=0
else
    USERID=$(shell id -u)
    GROUPID=$(shell id -g)
endif

# create COMP
COMP=USERID=$(USERID) GROUPID=$(GROUPID) docker-compose -f $(YML)


image:
	$(COMP) build

up:
	$(COMP) up -d

run: 
	$(COMP) exec  track-viewer-server /bin/bash

down:
	$(COMP) down
