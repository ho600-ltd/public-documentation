如何在 Jenkins 伺服器執行本地端的 AWS codebuild 專案建置 Sphinx 式文件網站?
===============================================================================

.. note::

    本文閱讀對象: 能在 AWS codebuild console 操作建置作業。

在軟體建置的方法上，敝司的操作經驗可以分成下列幾種:

1. 全部由 Jenkins 建置
#. 部份由 Atlassian Pipelines 建置，另外由 Jenkins 建置
#. 部份由 AWS codebuild 建置，另外由 Jenkins 建置
#. 全部由 AWS codebuild 建置
    * 在開發者本機端，則由 Jenkins 啟動 codebuild 建置

**第 1 種** 是敝司最早期的建置方式，在 AWS EC2 上安裝設定 1 台 Jenkins 伺服器，\
讓它把軟體建置加發佈一次跑完。

優點是設定簡單；\
缺點是無法同時滿足多個專案的建置、發佈需求，因為 Jenkins 本身跑在 JVM 上，\
有基本的記憶體需求，若有多個專案同時建置，那容易造成記憶體/CPU的需求尖峰過高，\
與我們在雲端運算的使用宗旨相背。\
微調方法是讓建置工作在開發者本地端的 Jenkins 伺服器處理，\
發佈工作則是送到 AWS EC2 上的 Jenkins 伺服器處理。\
建置 Jenkins 與發佈 Jenkins 之間當然得多了溝通工作。

**第 2 種** 是 Atlassian 在它們著名的 `Bitbucket Cloud <https://bitbucket.org/>`_ 服務中推出 Pipelines 後，\
敝司所採用的方式。將敝司軟體專案中，\
可獨立建置的全靜態網站或 Sphinx 文件式網站建置、發佈任務委由 Pipelines 處理。

優點是有效降低 Jenkins on EC2 的資源尖峰；\
缺點是 Bitbucket pipelines 與 AWS 是分屬不同的環境，設定步驟會多一點。\
但也由於我們所獨立建置的網站成果都是放在 S3 上面，所以麻煩程度並不會太高。\
另外，還有一個缺點，在建置過程中，若是需要用到資料庫，那就頭痛了，\
我們的測試資料庫都在 AWS 中，要讓 Pipelines 拿到資料、匯入資料庫，是辦得到，\
只是執行時間會多很多，而且設定步驟更加複雜。

**第 3, 4 種** 是在敝司將儲存庫從 Bitbucket Cloud 搬到自建的 Bitbucket Server 後採用的。

Codebuild 的計價方式是以每分鐘為單位，而我們在進行程式碼測試時，\
需要將正式資料庫備份到測試資料庫上，這裡的處置工作，在 CPU/記憶體上的用量不高，\
但耗費時間較久，用 codebuild 處理不划算。另外在建置階段，\
敝司也分成「本機端建置」與「伺服器端建置」，前者是由開發者在自己的開發平台上建置，\
第一時間驗證開發者自己寫的程式碼是否有問題。\
後者是在大家共用的伺服器上建置，這樣才能保有「明確、公用」的建置紀錄，\
在協作工作中，才能有「共通」的用語去指涉目標程式碼。

本文針對第 4 種方法中的開發者本機端如何使用 codebuild 建置 Sphinx-based 文件專案來作說明。

在 AWS console 執行 codebuild 作業
-------------------------------------------------------------------------------

下列是敝司其中一個 sphinx-based 文件庫所自帶的 buildspec.yml:

.. code-block:: yaml
    :linenos:

    version: 0.2

    env:
      git-credential-helper: yes

    phases:
      install:
        runtime-versions:
          python: 3.7
      pre_build:
        commands:
          - mkdir -p ~/.ssh/
          - unzip -P ${SSH_KEY_PASSWORD} id_rsa_awscodebuild.zip
          - mv id_rsa_awscodebuild ~/.ssh/
          - chmod 400 ~/.ssh/id_rsa_awscodebuild
          - echo 'Host git-codecommit.us-west-2.amazonaws.com \n StrictHostKeyChecking false \n User '${SSH_KEY_ID}' \n IdentityFile ~/.ssh/id_rsa_awscodebuild \n' >> ~/.ssh/config
          - export CODEBUILD_SRC_DIR_primary=$(pwd)
          - export CODEBUILD_SRC_2_DIR=$CODEBUILD_SRC_DIR_id2
          - export COMMIT_CHANGESET=$(git rev-parse HEAD)
          - export SHORT_COMMIT_CHANGESET=$(git rev-parse --short=7 HEAD)
          - export BUILD_TIME=$(date +%Y-%m-%dT%H:%M:%S%z)
          - mkdir -p docs/_build/html
          - echo '{ "CODEBUILD_BUILD_ID"':' "'${CODEBUILD_BUILD_ID}'",\n  "BUILD_TIME"':' "'${BUILD_TIME}'",\n   "COMMIT_CHANGESET"':' "'${COMMIT_CHANGESET}'" }' > docs/_build/html/__version__.json
          - pip install --upgrade pip
          - cp -rf docs/local_settings.py $CODEBUILD_SRC_2_DIR/trunk/local_settings.py
          - cd $CODEBUILD_SRC_2_DIR
          - pip install -r requirements.txt
          - cd $CODEBUILD_SRC_DIR_primary
          - pip install -r docs/requirements.txt
          - pip install --upgrade awscli
      build:
        commands:
          - cd docs/
          - make html
          - aws s3 cp --recursive _build/html s3://our-docs.ho600.com/DOC1/${COMMIT_CHANGESET}/

line 13 的目的，是在解壓縮某些私密的金錀。因為自動化建置、發佈所使用的程式碼儲存位置多是版本控制器，\
並不合適直接將這些隱私資訊以明碼方式放入版本控制器中。常規作法，是把它們用密語壓成 zip 檔，\
再儲存該 zip 檔到版本控制器上，另外把解密密語置入環境變數中。\
以此例來說， ${SSH_KEY_PASSWORD} 就是 AWS codebuild 專案的環境變數之一。

line 23 的目的是嵌入建置資訊到成果網站，\
如: `https://www.ho600.com/__version__.json <https://www.ho600.com/__version__.json>`_ 。

在 line 34 的 make html 中，因為文件庫有引入 $CODEBUILD_SRC_2_DIR 的程式碼，\
所以 $CODEBUILD_SRC_2_DIR 的配置必須是一個可運作的 Django-based 專案。\
這就是 line 25 的主要目的，讓 $CODEBUILD_SRC_2_DIR Django-based 專案擁有一個可運作的 settings.py 設定檔。

line 27 中的 requirements.txt 是 $CODEBUILD_SRC_2_DIR 的相依函式庫設定檔， \
line 29 則是本文件庫所需引入的相依函式庫，內容物通常只有 Sphinx==X.Y.Z 而已。

妥善編輯完 buildspec.yml 後，請先在 AWS codebuild console 中完成成功的建置工作，\
以確認 buildspec.yml 的格式及相關設定是正確的。

在命令列執行 local codebuild 作業
-------------------------------------------------------------------------------

結合 Jenkins 執行 local codebuild 作業
-------------------------------------------------------------------------------

.. code-block:: text

    LOCAL_CODEBUILD_IMAGE_NAME="amazon/aws-codebuild-local:latest"
    BUILD_IMAGE_NAME="ho600/docker-hub:ubuntu2.0"
    EXCUTOR="hoamon"
    AWS_CONFIGURATION_DIR="/Users/hoamon/.aws"

    SOURCE_DIR="/Users/hoamon/VSCProjects"
    REPOSITORY_NAME="dominate-bc-aws"
    BUILDSPEC_FILE="docs/buildspec.yml"


    SECONDARY_SOURCE_1="CODEBUILD_SRC_2"
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