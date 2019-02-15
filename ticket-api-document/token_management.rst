token 管理
===============================================================================


token 與登入者身份之間的關連
-------------------------------------------------------------------------------

每個人皆有一個獨一無二的 token，這個 token 可以拿來做身份驗證。

使用者未登入的狀況下可將 token 當成 query parameter 帶入，如以下形式：

.. code-block:: txt

    https://dev-rx.ho600.com/ticket/api/v2/ticket/?token=abbc088af094a4f61f3710724c3fa0863c35c47d

如果 token 正確，伺服器會將這次的連線當成是 **該 token 對應的使用者** 發送的。

由於 token 可被拿來作身分驗證，必須要注意 **絕對不要讓別人知道你個人的 token** ，若有被盜用的疑慮則需要重設 token。

.. hint::

    ticket 系統上附件的下載網址通常會長得像以下形式：

    https://dev-rx.ho600.com/download_attachment/32733/

    使用者成功登入且擁有瀏覽該附件的權限的話，則會直接重導向到該附件真正的下載網址，這類網址會長的像以下這樣：

    #.  AWS 檔案儲存空間

        https://dev-sr-ticket2.s3.amazonaws.com/media/private_uploaded_files/YANX/FANW/IRDP/leopard-leopard-spots-animal-wild-39857.jpeg?AWSAccessKeyId=AKIAIV2WIS2GLO3XSNTA&Signature=LezqUYT8LczjoF%2Fk9Mkbi9%2BQcB0%3D&Expires=1550218302

    #.  GOOGLE 檔案儲存空間

        https://commondatastorage.googleapis.com/dev-sr-associate-ticket/ticket-attachments/00/00/00/36/00/09/20190215080431.904598/antler-antler-carrier-fallow-deer-hirsch.jpg


    使用者未登入的話，https://dev-rx.ho600.com/download_attachment/32733/ 會將使用者導向登入頁，\
    登入過後會直接重導向到該附件真正的下載網址。

    當在 trask.com 提供給使用者 ticket 系統上附件的下載網址時，不能夠給予像下面這種，帶有個人 token 的連結：

    https://dev-rx.ho600.com/download_attachment/32733/?token=sdfc088af094a4f61f3710724c3fa0863c35c47d

    雖然上面這種帶有個人 token 的附件下載網址可以讓任何使用者不用登入就可以下載附件，\
    但這違反了一個規則： **絕對不要讓別人知道你個人的 token** 。

    比較好的做法是，要在 trask.com 開發一個網頁，將 https://dev-rx.ho600.com/download_attachment/32733/?token=sdfc088af094a4f61f3710724c3fa0863c35c47d \
    重導向的附件真正的下載網址抓回來，trask.com 必須要將這個網址直接告訴使用者，\
    **絕對不能夠提供給使用者任何含有 token 的網址提供給使用者** 。



如何取得個人 token
-------------------------------------------------------------------------------

1.  到頂端工具列選取 _開發人員選項_ 。

    .. figure:: token_management_1_1.png

#. 至 {管理 token} 區塊選擇 [複製] 即會把 token 複製到剪貼簿。

    .. figure:: token_management_1_2.png


如何更換個人 token
-------------------------------------------------------------------------------

1.  到頂端工具列選取 _開發人員選項_ 。

    .. figure:: token_management_2_1.png

#.  至 {管理 token} 區塊選擇 [重設] 。

    .. figure:: token_management_2_2.png

#.  此時跳出 +您確定要重設 token 嗎？ 舊的 token 將無法被使用 的 modal ，選擇 [重設] 即會產生新的一筆個人 token。

    .. figure:: token_management_2_3.png


