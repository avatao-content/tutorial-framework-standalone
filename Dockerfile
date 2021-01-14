FROM avatao/baseimage-tutorial-framework:ragdoll-20210114

# Define variables to use later
ENV TFW_EHMAIN_DIR="${TFW_DIR}/builtin_event_handlers" \
    TFW_APP_YML="/.tutorial/tfw.yml" \
    CONTROLLER_PORT=5555

# Copy TFW related stuff to a dedicated directory
COPY src ${TFW_EHMAIN_DIR}/

COPY etc /etc
COPY error_page/502.html ${TFW_FRONTEND_DIR}
COPY tfw_init.sh /.tfw/

# Hide TFW related code from user
RUN chown -R root:root ${TFW_SERVER_DIR} ${TFW_DIR} &&\
    chmod -R 700 ${TFW_SERVER_DIR} ${TFW_DIR} &&\
    chmod 600 /etc/ssh/tfw_id_rsa
    
VOLUME ["/home/${AVATAO_USER}", "/.tutorial"]

USER root