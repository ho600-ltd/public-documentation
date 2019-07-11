怎樣在 ssllabs.com 上獲得 A+ 的安全性平等
===============================================================================


一般來說，只要有使用 https，則在 https://www.ssllabs.com/ 上可以獲得 A 的安全性平等。

若要讓 A 的安全性平等能提升至 A+ ，則在 nginx 的設定上使用 HSTS。

HSTS 策略可以讓瀏覽器強制使用HTTPS與網站進行通訊，以減少連線劫持風險。

設定方法也很簡單，在 nginx.conf 加上以下敘述即可啟用HSTS 策略：

.. code-block:: text

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;


另可在 nginx.conf 加上以下敘述防止 XSS：

.. code-block:: text

    add_header X-XSS-Protection "1; mode=block";

以下是 https://www.ssllabs.com/ssltest/analyze.html?d=bc2019-sitethemes.bookcat-kessai.com 的結果:

.. figure:: how_to_get_a_plus_rating_on_ssllabs_com/1.png


設定檔範例如下:

.. code-block:: text

    ssl_protocols           TLSv1 TLSv1.1 TLSv1.2;# BEST
    ssl_ciphers "ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES128-SHA256:DHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES256-GCM-SHA384:AES128-GCM-SHA256:AES256-SHA256:AES128-SHA256:AES256-SHA:AES128-SHA:DES-CBC3-SHA:HIGH:!aNULL:!eNULL:!EXPORT:!DES:!MD5:!PSK:!RC4";ssl_session_cache shared:SSL:10m;
    ssl_prefer_server_ciphers on;ssl_stapling on;
    ssl_stapling_verify on;resolver 8.8.4.4 8.8.8.8 valid=300s;
    resolver_timeout 10s;add_header Strict-Transport-Security max-age=63072000;
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options nosniff;