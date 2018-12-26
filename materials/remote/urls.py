from django.urls import path, re_path
from materials.remote import views

urlpatterns = [
    re_path(r'adv/(?P<nid>\d+)/$', views.AdvProgrammeAPIViews.as_view({'get': 'adv_list'})),
    re_path(r'welfare_primary/(?P<nid>\d+)/$', views.WelfarePrimaryProgrammeAPIView.as_view({'get': 'welfare_primary_list'})),
    re_path(r'welfare_secondary/(?P<nid>\d+)/$', views.WelfareSecondaryProgrammeAPIView.as_view({'get': 'welfare_secondary_list'})),
    re_path(r'qr_code/(?P<nid>\d+)/$', views.QrCodeProgrammeAPIView.as_view({'get': 'qr_code_list'})),
    re_path(r'template/(?P<nid>\d+)/$', views.TemplateProgrammeAPIView.as_view({'get': 'template_list'})),
]
