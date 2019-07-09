
怎樣在 ssllabs.com 上獲得 A+ 的安全性平等

===============================================================================


一般來說，只要有使用 https，則在 https://www.ssllabs.com/ 上可以獲得 A 的安全性平等。

若要讓 A 的安全性平等能提升至 A+ ，則在 nginx 的設定上使用 HSTS。

HSTS 策略可以讓瀏覽器強制使用HTTPS與網站進行通訊，以減少連線劫持風險。

設定方法也很簡單，在 nginx.conf 加上以下敘述即可啟用HSTS 策略：

.. note::

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;


另可在 nginx.conf 加上以下敘述防止 XSS：

.. note::

    add_header X-XSS-Protection "1; mode=block";

