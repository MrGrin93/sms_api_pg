#!/bin/bash

generate_post_data()
{
  cat <<EOF
{
    "number":"$sms_num",
    "text": "$sms_txt",
    "ul":"tetst"
    "ul_number": "+79261234567"
}
EOF
}
ip="172.24.2.130"
data=$(generate_post_data)
echo "data: $data"

curl  --data "$data" http://$ip:8000/api/sms/ -H "Content-Type: application/json"