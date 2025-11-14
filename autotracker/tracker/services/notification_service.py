from __future__ import annotations
from tracker.models import Episode, NotificationLog
from tracker.services.sms_gateway import get_sms_gateway


def notify_user_new_episode(user, episode: Episode) -> NotificationLog:
    gateway = get_sms_gateway()
    message = f"New episode for {episode.show.title}: {episode.title}. Downloaded: {'Yes' if episode.is_downloaded else 'No'}"
    success = gateway.send_sms(user.profile.phone_number if hasattr(user, 'profile') else '', message)
    status = NotificationLog.SENT if success else NotificationLog.FAILED
    log = NotificationLog.objects.create(
        user=user,
        episode=episode,
        message=message,
        status=status,
    )
    return log
