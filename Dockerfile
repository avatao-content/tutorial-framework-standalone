FROM avatao/baseimage-tutorial-framework:ragdoll-20201201

# Define variables to use later
ENV TFW_EHMAIN_DIR="${TFW_DIR}/builtin_event_handlers" \
    TFW_APP_YML="/home/user/tutorial/app.yml" \
    CONTROLLER_PORT=5555

# Copy TFW related stuff to a dedicated directory
COPY tfw/src ${TFW_EHMAIN_DIR}/

COPY tfw/supervisor /etc/supervisor/conf

# Hide TFW related code from user
RUN chown -R root:root ${TFW_SERVER_DIR} ${TFW_DIR} &&\
    chmod -R 700 ${TFW_SERVER_DIR} ${TFW_DIR}
    
VOLUME ["/home/${AVATAO_USER}"]

USER root