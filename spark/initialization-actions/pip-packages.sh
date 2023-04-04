#!/bin/bash

# Installs required pip packages from a private repository, since the
# Dataproc property dataproc:pip.packages only works for public packages.
# See https://cloud.google.com/dataproc/docs/tutorials/python-configuration

# Setup keyring in order to connect to the private repository with service account
# See https://cloud.google.com/artifact-registry/docs/python/authentication#keyring
readonly PYTHON_REGISTRY_PROJECT_ID=$(/usr/share/google/get_metadata_value attributes/python-registry-project-id)
readonly PYTHON_REGISTRY_REGION=$(/usr/share/google/get_metadata_value attributes/python-registry-region)
readonly PYTHON_REGISTRY_NAME=$(/usr/share/google/get_metadata_value attributes/python-registry-name)
readonly PYTHON_REGISTRY_URL=https://${PYTHON_REGISTRY_REGION}-python.pkg.dev/${PYTHON_REGISTRY_PROJECT_ID}/${PYTHON_REGISTRY_NAME}

echo -e "Installing key ring:\e"
pip install \
    keyring==23.13.1 \
    keyrings.google-artifactregistry-auth==1.1.2

cat > ${HOME}/.pypirc <<EOF
[distutils]
index-servers =
    ${PYTHON_REGISTRY_NAME}

[${PYTHON_REGISTRY_NAME}]
repository: ${PYTHON_REGISTRY_URL}
EOF

# install dependencies manually while remote repositories is in preview
# See https://cloud.google.com/artifact-registry/docs/repositories/remote-repo
pip install \
    pyspark==3.1.3 \
    delta-spark==1.0.1

pip install \
    air-quality-spark==0.0.7 \
    --index-url ${PYTHON_REGISTRY_URL}/simple/

echo "Finished installing pip packages on worker node."
