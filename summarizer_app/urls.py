from django.urls import path, include
from django.conf.urls import url
from .views import NewSummarizationTask, GetSummary, SaveSummary, GetSummaries

urlpatterns = [
    url(r'^summarize/$', NewSummarizationTask.as_view(), name="summarize"),
    url(r'^summary/(?P<summary_id>.*)/$', GetSummary.as_view(), name="get_summary"),
    url(r'^save-summary/(?P<summary_id>.*)/$', SaveSummary.as_view(), name="save_summary"),
    url(r'^all-summaries/$', GetSummaries.as_view(), name="save_summary"),
]
