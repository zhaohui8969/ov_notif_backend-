#!/usr/bin/env bash
#python3 ./ov_log_monit.py  --bear_hook "https://hook.bearychat.com/=bwGiZ/incoming/1c5c53191dbb9371f29eda1004719f03" --openvpn_service_list "127.0.0.1:7505" "127.0.0.1:7506"
python3 ./ov_log_monit.py --openvpn_service_list "127.0.0.1:7505" "127.0.0.1:7506" --host "0.0.0.0" --port "7789" --app_key "whoami"
