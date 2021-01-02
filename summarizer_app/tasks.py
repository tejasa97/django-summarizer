from celery import shared_task
from .models import SummarizerTask
from datetime import datetime, timedelta


@shared_task
def delete_unsaved_summaries(hours=1):
    """Deletes all summaries that are old and not checked in to save
    """

    time_ago = datetime.now() - timedelta(hours=hours)
    summary_tasks = SummarizerTask.objects.filter(
        created__lte=time_ago, summary__save_summary=False)

    print(f"Deleting {len(summary_tasks)} unsaved summaries older than an hour")

    summary_tasks.delete()
