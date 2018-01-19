Steps from PostgreSQL to MariaDB
===============================================================================

Our Django apps are used to connect PostgreSQL db, until we want to hire more programmers.   The reason is the same as we transfer version control tool from hg to git: MySQL/MariaDB, and git are familiar to more developers.

Because Django is a strong web framework, it has a data convertion tool on json format.  We can dump data from PostgreSQL, and restore the json data to MariaDB by dumpdata/loaddata commands of Django.  Compare to commercial solutions, we can ensure that the converted data runs better on Django.

In PostgreSQL side
-------------------------------------------------------------------------------

"is_suspend" is a special field in our project.  Codes as below are only needed for our system.

.. code-block:: python

    ShopOption.all_objects.filter(is_suspend=True).update(is_suspend=False)
    WorkOrder.all_objects.filter(is_suspend=True).delete()
    Order.all_objects.filter(is_suspend=True).delete()

Reduce the table size before data converting:

.. code-block:: sql

    delete from multi_sites_uniquesession where update_time < '2018-01-18 00:00:00+00:00';
    delete from django_session where expire_date < '2018-01-18 00:00:00+00:00';

There are some CHARSET/COLLATION issues in Mariadb 10.2.  If we want to support "utf8mb4" charset, then we only have utf8mb4_unicode_ci collation can be choosed.  And utf8mb4_unicode_ci has a few behaviors that we don't like:

1. auto-convert full-width char to half-width char.
#. ignore the space char in the begin or end of value.
#. case insensitive

In PostgreSQL, we usually use zh_TW.UTF-8, ja_JP.UTF-8 collation, and values are well defined unique, but it will raise IntegrityError when it is stored in MariaDB.

So that we need to adjust some values in original PG db:

.. code-block:: sql

    update trade_address set street = replace(street, '（', ' (') where street like '%（%';
    update trade_address set street = replace(street, '）', ') ') where street like '%）%';
    update trade_address set street = replace(street, '－', ' - ') where street like '%－%';
    update trade_address set street = regexp_replace(street, ' $', '。') where street ~ ' $';
    update trade_address set street = 'T e s t' where street = 'Test';
    update trade_address set street = concat(street, id) where street like '%test%';
    update trade_address set street = concat(street, id) where street like '%TEST%';
    update trade_address set street = replace(street, '０', ' 0 ') where street like '%０%';
    update trade_address set street = replace(street, '１', ' 1 ') where street like '%１%';
    update trade_address set street = replace(street, '２', ' 2 ') where street like '%２%';
    update trade_address set street = replace(street, '３', ' 3 ') where street like '%３%';
    update trade_address set street = replace(street, '４', ' 4 ') where street like '%４%';
    update trade_address set street = replace(street, '５', ' 5 ') where street like '%５%';
    update trade_address set street = replace(street, '６', ' 6 ') where street like '%６%';
    update trade_address set street = replace(street, '７', ' 7 ') where street like '%７%';
    update trade_address set street = replace(street, '８', ' 8 ') where street like '%８%';
    update trade_address set street = replace(street, '９', ' 9 ') where street like '%９%';

    update trade_consumer set address = replace(address, '（', ' (') where address like '%（%';
    update trade_consumer set address = replace(address, '）', ') ') where address like '%）%';
    update trade_consumer set address = replace(address, '－', ' - ') where address like '%－%';
    update trade_consumer set address = replace(address, 'Test', 'T e s t') where address like '%Test%';
    update trade_consumer set address = replace(address, '０', ' 0 ') where address like '%０%';
    update trade_consumer set address = replace(address, '１', ' 1 ') where address like '%１%';
    update trade_consumer set address = replace(address, '２', ' 2 ') where address like '%２%';
    update trade_consumer set address = replace(address, '３', ' 3 ') where address like '%３%';
    update trade_consumer set address = replace(address, '４', ' 4 ') where address like '%４%';
    update trade_consumer set address = replace(address, '５', ' 5 ') where address like '%５%';
    update trade_consumer set address = replace(address, '６', ' 6 ') where address like '%６%';
    update trade_consumer set address = replace(address, '７', ' 7 ') where address like '%７%';
    update trade_consumer set address = replace(address, '８', ' 8 ') where address like '%８%';
    update trade_consumer set address = replace(address, '９', ' 9 ') where address like '%９%';

    update trade_consumer set cellphone = replace(cellphone, '０', ' 0 ') where cellphone like '%０%';
    update trade_consumer set cellphone = replace(cellphone, '１', ' 1 ') where cellphone like '%１%';
    update trade_consumer set cellphone = replace(cellphone, '２', ' 2 ') where cellphone like '%２%';
    update trade_consumer set cellphone = replace(cellphone, '３', ' 3 ') where cellphone like '%３%';
    update trade_consumer set cellphone = replace(cellphone, '４', ' 4 ') where cellphone like '%４%';
    update trade_consumer set cellphone = replace(cellphone, '５', ' 5 ') where cellphone like '%５%';
    update trade_consumer set cellphone = replace(cellphone, '６', ' 6 ') where cellphone like '%６%';
    update trade_consumer set cellphone = replace(cellphone, '７', ' 7 ') where cellphone like '%７%';
    update trade_consumer set cellphone = replace(cellphone, '８', ' 8 ') where cellphone like '%８%';
    update trade_consumer set cellphone = replace(cellphone, '９', ' 9 ') where cellphone like '%９%';

    update trade_consumer set phone = replace(phone, '０', ' 0 ') where phone like '%０%';
    update trade_consumer set phone = replace(phone, '１', ' 1 ') where phone like '%１%';
    update trade_consumer set phone = replace(phone, '２', ' 2 ') where phone like '%２%';
    update trade_consumer set phone = replace(phone, '３', ' 3 ') where phone like '%３%';
    update trade_consumer set phone = replace(phone, '４', ' 4 ') where phone like '%４%';
    update trade_consumer set phone = replace(phone, '５', ' 5 ') where phone like '%５%';
    update trade_consumer set phone = replace(phone, '６', ' 6 ') where phone like '%６%';
    update trade_consumer set phone = replace(phone, '７', ' 7 ') where phone like '%７%';
    update trade_consumer set phone = replace(phone, '８', ' 8 ') where phone like '%８%';
    update trade_consumer set phone = replace(phone, '９', ' 9 ') where phone like '%９%';

    update trade_consumer set name = regexp_replace(name, ' $', '。') where name ~ ' $';
    update trade_consumer set email = regexp_replace(email, ' $', '。') where email ~ ' $';
    update trade_consumer set cellphone = regexp_replace(cellphone, ' $', '。') where cellphone ~ ' $';
    update trade_consumer set phone = regexp_replace(phone, ' $', '。') where phone ~ ' $';
    update trade_consumer set address = regexp_replace(address, ' $', '。') where address ~ ' $';

    update trade_consumer set name = regexp_replace(name, '　$', ' 。') where name ~ '　$';
    update trade_consumer set email = regexp_replace(email, '　$', ' 。') where email ~ '　$';
    update trade_consumer set cellphone = regexp_replace(cellphone, '　$', ' 。') where cellphone ~ '　$';
    update trade_consumer set phone = regexp_replace(phone, '　$', ' 。') where phone ~ '　$';
    update trade_consumer set address = regexp_replace(address, '　$', ' 。') where address ~ '　$';

    update trade_consumer set cellphone = '09XX-YYYYYY' where id = 10855;
    update trade_consumer set phone = '09XX-YYYYYY' where id = 15491;

    update maillist_recipient set email = 'ZZZZ000@ZZZ.com.tw' where email = 'zzzz000@ZZZ.com.tw ';

Dump json from PG
-------------------------------------------------------------------------------

.. code-block:: bash

    ./manage.py dumpdata -e maillist --indent 1 > all_exclude_maillist.json
    ./manage.py dumpdata maillist --indent 1 > maillist.json

In MariaDB side
-------------------------------------------------------------------------------

Create a new database:

.. code-block:: sql

    CREATE DATABASE ec_bio_enzyme_com CHARACTER SET = 'utf8mb4' COLLATE = 'utf8mb4_unicode_ci';
    CREATE USER ec_bio_enzyme_com@'%' identified by 'password';
    GRANT ALL PRIVILEGES on ec_bio_enzyme_com.* to ec_bio_enzyme_com@'%';
    GRANT ALL PRIVILEGES on test_ec_bio_enzyme_com.* to ec_bio_enzyme_com@'%';

Update DB information in settings.py. Then migrate the new db:

.. code-block:: bash

    ./manage.py migrate

The id of some old values are different form the migration, so we need to truncate data in four tables:

.. code-block:: sql

    SET FOREIGN_KEY_CHECKS = 0;
    TRUNCATE TABLE auth_permission;
    TRUNCATE TABLE django_content_type;
    TRUNCATE TABLE django_site;
    TRUNCATE TABLE auth_user;
    SET FOREIGN_KEY_CHECKS = 1;

We only change the collation in email field, becuase there are so many emails are have upper and lower case in the same time:

.. code-block:: sql

    ALTER TABLE trade_consumer MODIFY COLUMN email varchar(254) COLLATE utf8_bin NOT NULL;
    ALTER TABLE maillist_recipient MODIFY COLUMN email varchar(254) COLLATE utf8_bin NOT NULL;

.. code-block:: bash

    ./manage.py loaddata all_exclude_maillist.json
    ./manage.py loaddata maillist.json

Log table row counts in PG:

.. code-block:: sql

    \o 'count_pg.sql';
    SELECT concat('SELECT concat(''', relname, ''', '', '', count(*)) from ', relname, ';') FROM pg_stat_user_tables ORDER BY relname;

.. code-block:: bash

    psql -U ec_bio_enzyme_com -W ec_bio_enzyme_com < count_pg.sql | grep ", " > pg.log


Check MariaDB table rows:

.. code-block:: sql

    \T "count_mysql.sql";
    SELECT concat('SELECT concat(''', TABLE_NAME, ''', '', '', count(*)) from ', TABLE_NAME, ';') FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'ec_bio_enzyme_com' order by TABLE_ROWS;

.. code-block:: bash

    ./manage.py dbshell < count_pg.sql | grep ", [0-9]" > my.log

.. code-block:: bash

    diff -w pg.log my.log

And we can see the different counts are only involved by "is_suspend = true".

Hooray~ It is Done!