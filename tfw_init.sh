#!/bin/bash
set -euo pipefail

echo "export HISTFILE=\"${TFW_HISTFILE}\"" >> ${TFW_DIR}/bashrc &&
  cat ${TFW_DIR}/bashrc >> "/home/${AVATAO_USER}/.bashrc"

if [[ -z "${HOTRELOAD-}" ]]; then
  for dir in "${TFW_LIB_DIR}/tfw" "/etc/nginx" "/etc/supervisor"; do
    chown -R root:root "${dir}" && chmod -R 700 "${dir}";
  done
fi

chmod 777 "${TFW_PIPES_DIR}"

cp /.tutorial/app.yml "${TFW_DIR}/builtin_event_handlers/app.yml"
cp /.tutorial/app_fsm.py "${TFW_DIR}/builtin_event_handlers/app_fsm.py"
cp /.tutorial/frontend_config.yaml "${TFW_DIR}/builtin_event_handlers/frontend_config.yaml"

rm -f bashrc requirements.txt tfw_init.sh