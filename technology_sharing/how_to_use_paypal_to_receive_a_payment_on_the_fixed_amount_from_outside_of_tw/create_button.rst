創建「付款按鈕」
-------------------------------------------------------------------------------

.. figure:: how_to_use_paypal_to_receive_a_payment_on_the_fixed_amount_from_outside_of_tw/create_button/create_button01.png

    完成註冊後，可直接設定收款資訊

.. figure:: how_to_use_paypal_to_receive_a_payment_on_the_fixed_amount_from_outside_of_tw/create_button/create_button02.png

    或是從後台連結進入「設定收款頁」，主要有兩種: 付款按鈕、以信件傳送收款連結

.. figure:: how_to_use_paypal_to_receive_a_payment_on_the_fixed_amount_from_outside_of_tw/create_button/create_button03.png

    「付款按鈕」可直接要求「付款方以 PayPal 帳戶支付」，或是先列出「信用卡付款選項供付款方選擇」

.. figure:: how_to_use_paypal_to_receive_a_payment_on_the_fixed_amount_from_outside_of_tw/create_button/create_button04.png

    Option A 是與「電子商務系統」整合，非本文說明範圍。請使用 Option B

.. figure:: how_to_use_paypal_to_receive_a_payment_on_the_fixed_amount_from_outside_of_tw/create_button/create_button05.png

    設定按鈕: 選擇「直接購買」按鈕形式，並有兩種尺寸供購買者選取、運費另加、 10% 稅金等

.. figure:: how_to_use_paypal_to_receive_a_payment_on_the_fixed_amount_from_outside_of_tw/create_button/create_button06.png

    可觀看「按鈕實際在網頁上的形式」。複製左側源始碼到自己的網頁上，即可顯示如右側的按鈕

.. figure:: how_to_use_paypal_to_receive_a_payment_on_the_fixed_amount_from_outside_of_tw/create_button/create_button07.png

    瀏覽已創建的付款按鈕

.. figure:: how_to_use_paypal_to_receive_a_payment_on_the_fixed_amount_from_outside_of_tw/create_button/create_button08.png

    瀏覽按鈕的源始碼

若是使用「將商品加入購物車按鈕」，其源始碼範例如下:

.. code-block:: html

    <form target="paypal" action="https://www.paypal.com/cgi-bin/webscr" method="post">
    <input type="hidden" name="cmd" value="_s-xclick">
    <input type="hidden" name="hosted_button_id" value="JWW6DDCT5Z772">
    <table>
    <tr><td><input type="hidden" name="on0" value="Hours">Hours</td></tr><tr><td><select name="os0">
        <option value="4 hours per time">4 hours per time ¥12,000 JPY</option>
        <option value="8 hours per day(1 hour break in the middle)">8 hours per day(1 hour break in the middle) ¥23,888 JPY</option>
    </select> </td></tr>
    </table>
    <input type="hidden" name="currency_code" value="JPY">
    <input type="image" src="https://www.paypalobjects.com/en_US/TW/i/btn/btn_cart_LG.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">
    <img alt="" border="0" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" width="1" height="1">
    </form>

將以上程式碼複製貼上你的網頁，其顯示成果如下灰色區塊( **按鈕可實際操作** ):

.. raw:: html

    <div style="background-color: gray;">
    <form target="paypal" action="https://www.paypal.com/cgi-bin/webscr" method="post">
    <input type="hidden" name="cmd" value="_s-xclick">
    <input type="hidden" name="hosted_button_id" value="JWW6DDCT5Z772">
    <table>
    <tr><td><input type="hidden" name="on0" value="Hours">Hours</td></tr><tr><td><select name="os0">
        <option value="4 hours per time">4 hours per time ¥12,000 JPY</option>
        <option value="8 hours per day(1 hour break in the middle)">8 hours per day(1 hour break in the middle) ¥23,888 JPY</option>
    </select> </td></tr>
    </table>
    <input type="hidden" name="currency_code" value="JPY">
    <input type="image" src="https://www.paypalobjects.com/en_US/TW/i/btn/btn_cart_LG.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">
    <img alt="" border="0" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" width="1" height="1">
    </form>
    </div>

.. figure:: how_to_use_paypal_to_receive_a_payment_on_the_fixed_amount_from_outside_of_tw/create_button/create_button09.png

    在「瀏覽加入購物車按鈕源始碼的下方」有「創建瀏覽購物車按鈕」的設定

創建瀏覽購物車按鈕後，可見源始碼範例如下:

.. code-block:: html

    <form target="paypal" action="https://www.paypal.com/cgi-bin/webscr" method="post" >
    <input type="hidden" name="cmd" value="_s-xclick">
    <input type="hidden" name="encrypted" value="-----BEGIN PKCS7-----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-----END PKCS7-----">
    <input type="image" src="https://www.paypalobjects.com/en_US/TW/i/btn/btn_viewcart_LG.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">
    <img alt="" border="0" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" width="1" height="1">
    </form>

將以上程式碼複製貼上你的網頁，其顯示成果如下灰色區塊( **按鈕可實際操作** ):

.. raw:: html

    <div style="background-color: gray;">
    <form target="paypal" action="https://www.paypal.com/cgi-bin/webscr" method="post" >
    <input type="hidden" name="cmd" value="_s-xclick">
    <input type="hidden" name="encrypted" value="-----BEGIN PKCS7-----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-----END PKCS7-----">
    <input type="image" src="https://www.paypalobjects.com/en_US/TW/i/btn/btn_viewcart_LG.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">
    <img alt="" border="0" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" width="1" height="1">
    </form>
    </div>

.. figure:: how_to_use_paypal_to_receive_a_payment_on_the_fixed_amount_from_outside_of_tw/create_button/create_button10.png

    付款方所見的購物車頁