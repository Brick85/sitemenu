from django.db import models
from django.utils.translation import ugettext_lazy as _

class VideoMixin(models.Model):
    VIDEO_URLS_PATTERNS = {
        'youtube': {
            "link": "http://www.youtube.com/watch?v={0}",
            "iframe": "//www.youtube.com/embed/{0}",
        },
        'vimeo': {
            "link": "http://vimeo.com/{0}",
            "iframe": "//player.vimeo.com/video/{0}",
        }
    }

    video_url= models.CharField(_(u"video ID"), blank=True, max_length=256, help_text=_("Support Youtube (http://www.youtube.com/watch?v=ID) and Vimeo (http://vimeo.com/ID)") )

    class Meta:
        abstract = True

    def has_video(self):
        video_id, video_type = self.video_get_id_and_type()
        if video_id and video_type:
            return True
        else:
            return False

    def video_get_id_and_type(self):
        if self.video_url.startswith('https://'):
            self.video_url = self.video_url.replace('https://', 'http://')
        video_type = None
        video_id = None
        if self.video_url.startswith("http://www.youtube.com/watch?v="):
            video_type = "youtube"
            video_id = self.video_url.replace("http://www.youtube.com/watch?v=", "")
        elif self.video_url.startswith("http://vimeo.com/"):
            video_type = "vimeo"
            video_id = self.video_url.replace("http://vimeo.com/", "")
        return (video_id, video_type)

    def video_get_url(self, video_type):
        video_id, video_provider = self.video_get_id_and_type()
        if video_provider not in VideoMixin.VIDEO_URLS_PATTERNS:
            return "wrong_video_provider"
        if video_type not in VideoMixin.VIDEO_URLS_PATTERNS[video_provider]:
            return "wrong_video_type"
        return VideoMixin.VIDEO_URLS_PATTERNS[video_provider][video_type].format(video_id)

    def video_get_link_url(self):
        return self.video_get_url('link')

    def video_get_iframe_url(self):
        return self.video_get_url('iframe')

    def video_get_iframe(self, width, height):
        return """<iframe src="{link}" width="{width}" height="{height}" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>""".format(
            link=self.video_get_url('iframe'),
            width=width,
            height=height
        )
