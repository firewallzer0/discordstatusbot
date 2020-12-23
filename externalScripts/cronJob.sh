#!/bin/sh
speedtest-cli --json > latest.json
scp latest.json dt@10.10.10.175:/opt/data