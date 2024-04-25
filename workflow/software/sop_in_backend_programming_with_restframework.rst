The SOP for the backend programming with django-restframework
===============================================================================

.. note::

    ** 聲明 **

    本文件的閱讀對象為敝司業主、潛在業主、熱忱的未來應聘者及任何對敝司抱有興趣者，\
    目的除宣揚敝司管理制度及經營理念外，也是作為敝司員工的程式設計準則之一。

在 django-restframework 的框架下，每個 Api Endpoint 的建立，應利用以下幾個制式的類別組合而成:

* In authentication.py, put Classes inherited from rest_framework.authentication.\*Authentication, ex: rest_framework.authentication.SessionAuthentication
* In filters.py, put Classes inherited from rest_framework_filters.filters.FilterSet
* In permissions.py, put Classes inherited from rest_framework.\*permissions, ex: rest_framework.permissions.BasePermission
* In renderers.py, put Classes inherited from rest_framework.renderers.BrowsableAPIRenderer or rest_pandas.renderers.PandasExcelRenderer or rest_pandas.renderers.PandasCSVRenderer
* In responses.py, put Classes inherited from rest_framework.response.Response
* In serializers.py, put Classes inherited from rest_framework.serializers.\*Serializer, ex: rest_framework.serializers.ModelSerializer
* In urls.py, put Classes inherited from rest_framework.routers.APIRootView and rest_framework.routers.DefaultRouter instances
* In views.py, put Classes inherited from rest_framework.viewsets.ModelViewSet or rest_pandas.views.PandasViewSet

最終得到 https://example.domain.name/whaterver-app/whatever-module/whatever-tag/whatever-version/whatever-model/ 的 endpoints 網址。

每一個 Endpoint ，慣例上，應該要對應一個 Model(ex: taiwan_einvoice.views.TurnkeyServiceModelViewSet)，或是某條件下被 filter 過的 object set(ex: taiwan_einvoice.views.TurnkeyServiceGroupModelViewSet)。

Browsable Api
-------------------------------------------------------------------------------

**具備 Browsable Api 功能** 是 django-restframework 優於 django-tastypie 的最大特點，\
第二特點才是「使用人數 **遠高** 於後者」。

以下是最精簡建構一個 Browsable Api 所需的相關程式碼:

.. code-block:: html

    <!-- api.html -->
    {% extends "rest_framework/base.html" %}{% load i18n %}
    {% block title %}{% trans "Your Brand" %}{% endblock %}
    {% block branding %}
        <a class='navbar-brand' rel="nofollow" href='/'>
            {% trans "Your Named Api Services" %}
        </a>
    {% endblock %}

.. code-block:: python

    # views.py
    from django.conf import settings
    from rest_framework.renderers import BrowsableAPIRenderer
    from rest_framework.permissions import IsAuthenticated
    from my.models import MyModel
    from my.filters import MyFilter
    from my.serializers import MySerializer
    from my.permissions import MyPermission
    class MyBrowsableAPIRenderer(BrowsableAPIRenderer):
        template = "some-where/api.html"
    class MyModelModelViewSet(viewsets.ModelViewSet):
        permission_classes = (IsAuthenticated, MyPermission)
        queryset = MyModel.objects.all()
        filter_class = MyFilter
        serializer_class = MySerializer
        renderer_classes = (JSONRenderer, MyBrowsableAPIRenderer,
                            ) if settings.DEBUG else (JSONRenderer, )
        http_method_names = ('get', )

    # urls.py
    from django.urls import include, re_path
    from rest_framework import routers
    from my.views import MyModelModelViewSet
    class MyRouter(routers.DefaultRouter):
        pass 
    router = MyRouter()
    router.register(r'mymodel', views.MyModelModelViewSet, basename="mymodel")
    version = 'v1'
    urlpatterns = [
        re_path(r'^api/{}/'.format(version),
                include((router.urls, "myapi"),
                        namespace="myapi")),
    ]

    #INFO Endpoint of MyModel: https://example.domain.name/whaterver-app/my/api/v1/mymodel/ 

在開發階段， **必定要使用 RESTFramework 的 Browsable Api 頁面進行自身 Api 的測試** ，\
而無須依賴外部 Api 工具，如: POSTMAN 。外部 Api 工具可以作雙重驗證使用，\
但 RESTFramework 的 Browsable Api 是必備的。

待完成開發階段，發佈至「正式網站」時，再依「服務提供性質」，\
適當地移除或是保留 Browsable Api 頁面，例如採用下列語法:

.. code-block:: python

    class MyModelModelViewSet(viewsets.ModelViewSet):
        renderer_classes = [JSONRenderer, MyBrowsableAPIRenderer,
                           ] if settings.DEBUG else [JSONRenderer, ]
        def initial(self, request, *args, **kwargs):
            if request.user.is_superuser and MyBrowsableAPIRenderer not in self.renderer_classes:
                self.renderer_classes += [MyBrowsableAPIRenderer, ]
            super().initial(request, *args, **kwargs)

Avoid to expose information too much
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在 Browsable Api 的資訊揭露上，主要分三個部份討論。

Display the field of every instance
...............................................................................

在瀏覽 https://example.domain.name/whatever-app/whatever-module/api/v1/whatever-model/20/ 所輸出的 json/xml/plaintext/... ，\
其欄位內容要符合「連線使用者身份」的權限。

這部份要注意的是 Serializer Class 的設定。範例如下:

.. code-block:: python

    class CreateTimeOnlyForCreatorField(serializers.ReadOnlyField):
        def get_attribute(self, instance):
            if instance.creator == self.context['request'].user:
                return super(CreateTimeOnlyForCreatorField, self).get_attribute(instance)
            return None
    class MySerializer(serializers.ModelSerializer):
        create_time = CreateTimeOnlyForCreatorField()
        resource_uri = serializers.HyperlinkedIdentityField(
            view_name="my_api_root:my-detail",
            lookup_field='pk')
        class Meta:
            model = MyModel
            fields = '__all__' if settings.DEBUG else ('resource_uri', 'create_time', 'id')

POST Form in API format
...............................................................................

在 https://example.domain.name/whatever-app/whatever-module/api/v1/whatever-model/?format=api 頁面上，\
所存在的 POST Form ，就某些「下拉式選項所出現的 Option 」，其 Option Value 要符合「連線使用者身份」權限所能觀看的值。

這部份要注意的是 Serializer Class 的設定。範例如下:

.. code-block:: python

    class SomeRelatedField(serializers.PrimaryKeyRelatedField):
        def get_queryset(self):
            request = self.context.get('request', None)
            if request and request.user.is_superuser:
                return SomeModel.objects.all().order_by('id')
            elif 'api' == request.GET.get('format', '') or 'api' == request.POST.get('format', ''):
                return SomeModel.objects.none()
            else:
                return get_objects_for_user(request.user if request else AnonymousUser,
                                            ("module_name.view_model_permision",
                                            "module_name.edit_model_permision",
                                            "module_name.delete_model_permision",
                                            ),
                                            any_perm=True,
                                            with_superuser=True,
                                            accept_global_perms=False,
                                            ).order_by('id')
    class MySerializer(serializers.ModelSerializer):
        resource_uri = serializers.HyperlinkedIdentityField(
            view_name="my_api_root:my-detail",
            lookup_field='pk')
        some = SomeRelatedField(required=True, allow_null=False)
        class Meta:
            model = MyModel
            fields = '__all__' if settings.DEBUG else ('resource_uri', 'some', 'id')

Filter Form in API format
...............................................................................

在瀏覽 https://example.domain.name/whatever-app/whatever-module/api/v1/whatever-model/ 所提供的 Filter Form ，\
就某些「下拉式選項所出現的 Option 」，其 Option Value 要符合「連線使用者身份」權限所能觀看的值。

這部份要注意的是 Filter/ViewSet Class 的設定。範例如下:

.. code-block:: python

    class PopedomFilter(rest_framework_filters.FilterSet):
        class Meta:
            model = Popedom
            fields = {
                'name': ('icontains', ),
            }
    def popedom_queryset_by_request_user(request):
        if request.user.is_superuser or request.user.is_staff:
            return Popedom.objects.all().order_by('name')
        else:
            return get_objects_for_user(request.user,
                                        ("collection.view_popedom",
                                        "collection.own_popedom",
                                        "collection.update_popedom",
                                        "collection.create_device_box_under_this_popedom",
                                        ),
                                        any_perm=True,
                                        with_superuser=True,
                                        accept_global_perms=False,
                                        ).order_by('id')
    class MyFilter(rest_framework_filters.FilterSet):
        popedom = rest_framework_filters.RelatedFilter(PopedomFilter,
                                                       label=_('Popedom'),
                                                       field_name="popedom",
                                                       queryset=popedom_queryset_by_request_user)
        class Meta:
            model = MyModel
            fields = {
                'name': ('icontains', ),
            }
    class MyModelViewSet(viewsets.ModelViewSet):
        queryset = MyModel.objects.all()
        filter_class = MyFilter

Permission Control 
-------------------------------------------------------------------------------

利用 \*ViewSet 撰寫 api 時，permission_classes 裡面每個 permission 預設都是 and 的關係，\
必須要全部通過才會執行相關 action ，若要使用 OR 關係時可以引用 ho600_lib.permissions.Or。

\*ViewSet 除了加上應該要有的 permission_classes 之外，\
也應該要在 \*.ViewSet.get_queryset 函式裡面限制可以暴露給該使用者的資料，做另一層防護。

權限控制以 django 內建權限架構及 django-guardian 為基礎，在判斷權限時，\
以 request.user 為出發點，來判斷他/她能不能 **CRUD** 某個物件，\
並儘量不要摻雜其他判斷條件。

例如: 某人要刪除某一任務，而功能需求又限制只能刪除創建時間超過 3 年以上的任務，\
則「權限判斷」應僅止於在 \*ViewSet.permission_classes 及 \*ViewSet.get_queryset 處理，\
前者處理「某人有沒有某個 permission_codename 或某人在某個物件上有沒有某個 permission_codename」，\
後者是把「某人具備某個 permission_codename 的物件全部撈出來」，兩者要同時存在，且不可互相抵觸。\
而「只有創建時間超過 3 年以上的任務可刪除」的條件，必須置於 \*ViewSet.perform_destroy 函式之中。以下為範例程式:

.. code-block:: python

    class IsSuperuserOrStaff(BasePermission):
        def has_permission(self, request, view):
            res = False
            res = (request.user.is_authenticated()
                   and (request.user.is_superuser
                        or request.user.is_staff))
            return res
        def has_object_permission(self, request, view, obj):
            res = False
            res = (request.user.is_authenticated()
                   and (request.user.is_superuser
                        or request.user.is_staff))
            return res
    class DealWithTicketPermission(BasePermission):
        ANY_PERM = True
        WITH_SUPERUSER = False
        ACCEPT_GLOBAL_PERMS = False
        GET_USE_GROUP_PERMS = True
        ACTION_PERMISSION_MAPPING = {
            "create": ("ticket.create_ticket", ),
            "list": ("ticket.view_ticket", "ticket.own_ticket",
                     "ticket.update_ticket", ),
            "retrieve": ("ticket.view_ticket", "ticket.own_ticket",
                         "ticket.update_ticket", ),
            "partial_update": ("ticket.own_ticket",
                               "ticket.update_ticket", ),
            "update": ("ticket.own_ticket",
                       "ticket.update_ticket", ),
            "destroy": ("ticket.own_ticket", ),
        }
        def has_permission(self, request, view):
            res = False
            if 'create' == view.action:
                res = request.user.has_perm(self.ACTION_PERMISSION_MAPPING[view.action])
            elif view.action in self.ACTION_PERMISSION_MAPPING:
                res = True
            return res
        def has_object_permission(self, request, view, obj):
            qs = Q()
            for _i in self.ACTION_PERMISSION_MAPPING.get(view.action, []):
                app_label, codename = _i.split('.')
                qs = qs | Q(content_type__app_label=app_label, codename=codename)
            res = False
            if view.action in self.ACTION_PERMISSION_MAPPING:
                if get_user_perms(request.user, obj
                                 ).filter(qs).exists():
                    res = True
            return res
    class TicketModelViewSet(viewsets.ModelViewSet):
        permission_classes = (Or(IsSuperuserOrStaff, DealWithTicketPermission), )
        queryset = Ticket.objects.all()
        filter_class = TicketFilter
        serializer_class = TicketSerializer
        renderer_classes = (JSONRenderer, BrowsableAPIRenderer, ) if settings.DEBUG else (JSONRenderer, )
        http_method_names = ('get', 'delete', )
        def get_queryset(self):
            return get_objects_for_user(self.request.user,
                                        DealWithTicketPermission.ACTION_PERMISSION_MAPPING[self.action],
                                        any_perm=DealWithTicketPermission.ANY_PERM,
                                        use_groups=DealWithTicketPermission.GET_USE_GROUP_PERMS,
                                        with_superuser=DealWithTicketPermission.WITH_SUPERUSER
                                                       or DealWithTicketPermission.ACCEPT_GLOBAL_PERMS,
                                        accept_global_perms=DealWithTicketPermission.ACCEPT_GLOBAL_PERMS,
                                       ).order_by('id')
        def perform_destroy(self, obj):
            if obj.is_expired:
                return super().perform_destroy(obj)
            else:
                raise SomeException('...')
    
    # models.py
    class Ticket(models.Model):
        ...
        @property
        def is_expired(self):
            if (datetime.datetime.utcnow() - self.create_time) > datetime.datetime.timedelta(years=3):
                return True
            else:
                return False

將判斷「任務是否過期」的條件置入 Model 中，這是原有 Django 開發所制定的規範，\
與 RESTful Api 無關。也就是說，在整個系統上，可能有一堆地方都要去判斷 Ticket instance 是否過期，\
這個 "\> 3年" 的判斷式只應該存在於一處，而最佳的地方就是在 Model 內定義。


.. note::

    **To ho600 employees** ,

    XXXModule.permissions 中通常會有一個 DealwithXXXProjectRelatedPermission or DealwithXXXShopRelatedPermission \
    之類的 class ，主要原因在於「權限設計上，慣於把使用者操作 XXXModule 的權限先全歸類到 Project or Shop class」，\
    例如: "project.view_ticket", "shop.view_order" 的 codename 是設定在 Project/Shop class 內，\
    而不使用 "ticket.view_ticket", "order.view_order"，\
    且 ticket objects 必定歸屬於某個 project object 、 order objects 必定歸屬於某個 shop object 。

    在 taiwan_einvoice module 中，雖然權限 codename 是定義在 TurnkeyService Model 之下，\
    就並未創建 DealwithTaiwanTurnkeyServiceRelatedPermission 的父權限類別給其他 \
    EInvoice, UploadBatch permission classes 繼承。