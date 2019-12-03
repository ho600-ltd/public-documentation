如何在 Jenkins 伺服器執行本地端的 AWS codebuild 專案建置 Sphinx 式文件網站?
===============================================================================

在軟體建置的階段上，敝司的經驗可以分成下列幾種:

1. 全部由 Jenkins 建置
#. 部份由 Atlassian pipeline 建置，另外由 Jenkins 建置
#. 部份由 AWS codebuild 建置，另外由 Jenkins 建置
#. 全部由 AWS codebuild 建置

第 1 種是敝司最早期的建置方式，在 AWS EC2 上安裝設定 1 台 Jenkins 伺服器，\
讓它把軟體建置加發佈一次跑完。

優點是設定簡單；\
缺點是無法同時滿足多個專案的建置、發佈需求，因為 Jenkins 本身跑在 JVM 上，\
有基本的記憶體需求，若有多個專案同時建置，那容易會造成記憶體/CPU的需求尖峰，\
與我們在雲端運算的使用宗旨相背。\
微調方法是讓建置工作在開發者本地端的 Jenkins 伺服器處理，\
發佈工作則是送到 AWS EC2 上的 Jenkins 伺服器處理。\
建置 Jenkins 與發佈 Jenkins 當然得多了溝通工作。

.. code-block:: text

    LOCAL_CODEBUILD_IMAGE_NAME="amazon/aws-codebuild-local:latest"
    BUILD_IMAGE_NAME="ho600/docker-hub:ubuntu2.0"
    EXCUTOR="hoamon"
    AWS_CONFIGURATION_DIR="/Users/hoamon/.aws"

    SOURCE_DIR="/Users/hoamon/VSCProjects"
    REPOSITORY_NAME="dominate-bc-aws"
    BUILDSPEC_FILE="docs/buildspec.yml"


    SECONDARY_SOURCE_1="cash_flow_2"
    SOURCE_2_DIR="/Users/hoamon/VSCProjects"
    REPOSITORY_2_NAME="cash-flow-2"

    ARTIFACTS=${SOURCE_DIR}"/artifacts_out"

    SSH_KEY_PASSWORD="..."
    SSH_KEY_ID="APK..."

    cat << EOF > ${REPOSITORY_NAME}.env
    WHATEVER=_WHATVALUE_
    SSH_KEY_PASSWORD=${SSH_KEY_PASSWORD}
    SSH_KEY_ID=${SSH_KEY_ID}
    EOF

    sudo -u ${EXCUTOR} docker run -v /var/run/docker.sock:/var/run/docker.sock \
    -e "IMAGE_NAME=${BUILD_IMAGE_NAME}" \
    -e "ARTIFACTS=${ARTIFACTS}" \
    -e "SOURCE=${SOURCE_DIR}/${REPOSITORY_NAME}" \
    -e "SECONDARY_SOURCE_1=${SECONDARY_SOURCE_1}:${SOURCE_2_DIR}/${REPOSITORY_2_NAME}" \
    -e "BUILDSPEC=${SOURCE_DIR}/${REPOSITORY_NAME}/${BUILDSPEC_FILE}" \
    -v "${SOURCE_DIR}:/LocalBuild/envFile/" \
    -e "ENV_VAR_FILE=${REPOSITORY_NAME}.env" \
    -e "AWS_CONFIGURATION=${AWS_CONFIGURATION_DIR}" \
    -e "INITIATOR=${EXCUTOR}" ${LOCAL_CODEBUILD_IMAGE_NAME}