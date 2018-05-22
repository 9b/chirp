#!/bin/bash

while sleep 1
do
    mongo --quiet --eval 'db.accounts.update({}, {$set: {groups: ["admin"]}});' chirp >/dev/null
done
