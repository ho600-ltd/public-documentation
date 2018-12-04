設定工作環境
===============================================================================

生成、備份 ssh/pgp 私錀
-------------------------------------------------------------------------------

產生 PGP Key:

.. code-block:: bash

    $ gpg --full-gen-key # 生成過程中會遇到以下提問：
    Please select what kind of key you want:
    (1) RSA and RSA (default)
    (2) DSA and Elgamal
    (3) DSA (sign only)
    (4) RSA (sign only)
    Your selection?

    # 選擇類型 (1) RSA and RSA (default)。
    # 然後輸入 name, email ，可以不用填 comment。
    # 輸入 passphrase 增加安全性。

    $ gpg --keyserver pgp.mit.edu --send-keys <Your_PGP_public_key_fingerprint>
    # gpg key 生成完成後發布 public key 到 https://pgp.mit.edu/ ，會在 https://pgp.mit.edu/ 留下紀錄：

備份 PGP Key:

.. code-block:: bash

    $ gpg --list-keys --keyid-format LONG # 顯示所有公錀
    $ gpg --armor --export <Your_PGP_public_key_fingerprint> > public.key # 備份公錀
    $ gpg --export-secret-key -a <Your_PGP_public_key_fingerprint> > private.key # 備份私錀
    $ zip -er private.key.zip private.key
    Enter password:
    Verify password:
      adding: private.key (deflated 47%)
    # 將 private.key.zip 儲存到一個安全、私密的地方，為日後回復私錀之用，請務必記住 zip 解密密碼及拿得回原始的 private.key.zip 檔

產生 SSH key:

.. code-block:: bash

    $ ssh-keygen -t rsa -b 4096
    Generating public/private rsa key pair.
    Enter file in which to save the key (/Users/User1/.ssh/id_rsa): 
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    Your identification has been saved in /Users/User1/.ssh/id_rsa.
    Your public key has been saved in /Users/User1/.ssh/id_rsa.pub.
    The key fingerprint is:
    SHA256:a1SrSNJH6Xe/ncTpG+wKtHls3L8ZKj4hE8mYM0faUco User1@MacBookPro
    $ chmod 400 /Users/User1/.ssh/id_rsa

備份 SSH Private Key:

.. code-block:: bash

    $ zip -er id_rsa.zip id_rsa
    Enter password:
    Verify password:
      adding: id_rsa (deflated 47%)
    # 將 id_rsa.zip 儲存到一個安全、私密的地方，為日後回復私錀之用，請務必記住 zip 解密密碼及拿得回原始的 id_rsa.zip 檔

放置 SSH 公錀至 bitbucket.org:

1. 登入 Bitbucket 網頁
#. 點選 Avatar > bitbucket settings > Security > SSH keys > Add key
#. 加入 id_rsa.pub 的內容
#. 隨意 clone 個人名下所管理的儲存庫看看是否可正常抓取

方便操作 Bitbucket 上的專案，可修改 ssh config:

.. code-block:: bash

    $ cat << EOF >> /Users/User1/.ssh/config
    Host bitbucket.org
    IdentityFile /Users/User1/.ssh/id_rsa
    User <your_username>
    EOF

資料庫資料備份
-------------------------------------------------------------------------------

開發員在經手的系統上，所以使用「測試」或「真實」資料庫資料，\
都應自行備份在安全的地方，但在備份前， **為確保資料安全性/機密性** ，\
皆須先以個人 PGP 公錀加密後，才可備份到其他主機或雲端硬碟。

.. code-block:: bash

    $ gpg -r <your_own_email_address> -e XXX.sql
    File 'XXX.sql.gpg' exists. Overwrite? (y/N)y

災難處理
-------------------------------------------------------------------------------

PGP 私錀遺失:

在 PGP 私錀遺失且無法回復後，必須對敝司系統開發過程中所使用之設定檔 *-settings.py.gpg 進行重新解密，\
再以新 PGP 公錀做加密後，更新回版本控制器中。

通常敝司的做法是 live branch 及 test branch 各有一個 *-settings.py.gpg ，\
各自在 live / test branch 做解密、加密即可。

SSH 私錀遺失:

只有重新製作新私錀，並更新其他系統上所放置之舊公錀。