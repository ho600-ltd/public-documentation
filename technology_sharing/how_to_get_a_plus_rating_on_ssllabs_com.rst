如何在 ssllabs.com 上獲得 A+ 的安全性評等?
===============================================================================

一般來說，只要有使用 https ，則在 https://www.ssllabs.com/ 上可以獲得 A 的安全性評等。\
若要讓 A 的安全性評等能提升至 A+ ，目前須在 nginx 的設定上使用 HSTS 。 HSTS \
策略可以讓瀏覽器強制使用 HTTPS 與網站進行通訊，以減少連線劫持風險。

設定方法也很簡單，在 nginx.conf 加上以下敘述即可啟用 HSTS 策略：

.. code-block:: ini

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

另可在 nginx.conf 加上以下敘述防止 XSS :

.. code-block:: ini

    add_header X-XSS-Protection "1; mode=block";

並且注意，在多層次的 nginx 伺服器下，不要重覆設定相同的 add_header ，\
此舉會令 ssllabs 回報 Server providers more than one HSTS header 訊息，\
致使只拿到 A 級分。

以下是 https://www.ssllabs.com/ssltest/analyze.html?d=www.ho600.com 的結果:

.. figure:: how_to_get_a_plus_rating_on_ssllabs_com/1.png

設定檔範例如下:

.. code-block:: ini

    #ssl_protocols TLSv1.3 TLSv1.2 TLSv1.1;
    ssl_protocols TLSv1.2 TLSv1.3; # TLSv1.3 requires nginx >= 1.13.0 else use TLSv1.2

    ssl_dhparam /etc/ssl/certs/certsdhparam-20190718.pem; # openssl dhparam -out /etc/nginx/dhparam.pem 4096
    ssl_session_cache shared:SSL:10m;
    ssl_prefer_server_ciphers on;

    ssl_stapling on;
    ssl_stapling_verify on;

    resolver 8.8.4.4 8.8.8.8 valid=300s;
    resolver_timeout 10s;

    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384; # 4*100 A

    ssl_ecdh_curve secp384r1; # Requires nginx >= 1.1.0
    ssl_session_timeout  10m;
    ssl_session_tickets off; # Requires nginx >= 1.5.9

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options nosniff;
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
    add_header X-XSS-Protection "1; mode=block";

延伸閱讀:

    * https://cipherli.st/
    * https://raymii.org/s/tutorials/Strong_SSL_Security_On_nginx.html
