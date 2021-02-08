"""Apps for Zinnia"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from watson import search as watson
from html2text import html2text


class ZinniaEntrySearchAdapter(watson.SearchAdapter):
    def get_description(self, obj):
        return html2text.html2text(obj.html_preview())


class ZinniaConfig(AppConfig):
    """
    Config for Zinnia application.
    """
    name = 'zinnia'
    label = 'zinnia'
    verbose_name = _('Weblog')

    def ready(self):
        from django_comments.moderation import moderator

        from zinnia.signals import connect_entry_signals
        from zinnia.signals import connect_discussion_signals
        from zinnia.moderator import EntryCommentModerator
        from zinnia.managers import PUBLISHED

        entry_klass = self.get_model('Entry')
        # Register the comment moderator on Entry
        moderator.register(entry_klass, EntryCommentModerator)
        # Connect the signals
        connect_entry_signals()
        connect_discussion_signals()

        watson.register(
            entry_klass.objects.filter(status=PUBLISHED),
            ZinniaEntrySearchAdapter,
            fields=(
                "title",
                "slug",
                "content"
            ),
            store=("search_thumbnail", )
        )
