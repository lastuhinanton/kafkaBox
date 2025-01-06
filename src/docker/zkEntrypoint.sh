#!/bin/bash

CONFIG_FILE=/opt/kafka/config/zookeeper.properties

[ -n "$ZOOKEEPER_CLIENT_PORT" ] && sed -i "s/^clientPort=.*/clientPort=${ZOOKEEPER_CLIENT_PORT}/" $CONFIG_FILE

