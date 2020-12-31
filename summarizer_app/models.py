from django.db import models
import time
from celery import shared_task, Task
from core.celery import celery

from users.models import User
from .managers import SummarizationManager

from text_summarizer import get_summary


class PatchedCeleryTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

    def on_success(self, retval, task_id, args, kwargs):

        summarizer_task = SummarizerTask.objects.get(celery_task_id=task_id)
        summarizer_task.task_status = SummarizerTask.DONE
        summarizer_task.save()

        Summary.update_summary_from_task(
            celery_task_id=task_id, summary=retval)


@shared_task(bind=True, base=PatchedCeleryTask, max_retries=3)
def get_summary_task(self, text):

    summary = get_summary(text)
    # Hack for now
    return '. '.join(summary)


class SummarizerTask(models.Model):

    PENDING = 0
    FAILED = 1
    DONE = 2

    TASK_STATUS_CHOICES = (
        (PENDING, 'pending'),
        (FAILED, 'failed'),
        (DONE, 'done'),
    )

    celery_task_id = models.CharField(max_length=50, unique=True)
    task_status = models.IntegerField(choices=TASK_STATUS_CHOICES, default=PENDING)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def start_new_task(cls, text):

        celery_task = get_summary_task.delay(text)
        obj = SummarizerTask.objects.create(celery_task_id=celery_task.task_id)

        return obj


class Summary(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="summaries"
    )

    summary_id = models.CharField(max_length=8, unique=True)
    celery_task = models.ForeignKey(SummarizerTask, on_delete=models.CASCADE)
    summary = models.TextField()
    website_icon_url = models.CharField(max_length=128)
    page_url = models.CharField(max_length=64)
    webpage_title = models.CharField(max_length=64)

    created = models.DateTimeField(auto_now_add=True)
    save_summary = models.BooleanField(default=False)

    objects = SummarizationManager()

    def summary_available(self):

        return self.celery_task.task_status == SummarizerTask.DONE

    @classmethod
    def create_new_summarization(cls, text, website_icon_url, page_url, webpage_title):

        summarization_task = SummarizerTask.start_new_task(text)
        summary_obj = Summary.objects.create(
            celery_task=summarization_task,
            website_icon_url=website_icon_url,
            page_url=page_url,
            webpage_title=webpage_title
        )

        return summary_obj.summary_id

    @classmethod
    def update_summary_from_task(cls, celery_task_id, summary):

        obj = cls.objects.get(celery_task__celery_task_id=celery_task_id)
        obj.summary = summary
        obj.save()

    @classmethod
    def save_summary_for_user(cls, user_email, summary_id):

        request_user, new = User.objects.get_or_create(email=user_email)

        summary_obj = cls.objects.get(summary_id=summary_id)

        summary_obj.user = request_user
        summary_obj.save_summary = True
        summary_obj.save()

    @classmethod
    def get_all_summaries_of_user(cls, user_email):

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            raise Summary.DoesNotExist

        summary_objects = user.summaries.filter(save_summary=True).all()

        return [summary.serialize() for summary in summary_objects]

    def serialize(self):

        return {
            'summary_id': self.summary_id,
            'summary': self.summary,
            'website_icon_url': self.website_icon_url,
            'page_url': self.page_url,
            'webpage_title': self.webpage_title,
            'created': self.created.isoformat()
        }
