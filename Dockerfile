FROM frappe/erpnext:v15.2.0

USER root
RUN apt-get update && apt-get install -y git
USER frappe

# Install the app
RUN bench get-app phd_management https://github.com/Aravinda-05/phd-lifecycle-system

# Build assets
RUN bench build
