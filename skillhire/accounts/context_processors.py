from interviews.models import Interview

def interview_notifications(request):
    if request.user.is_authenticated:

        candidate_notifications = Interview.objects.filter(
            candidate=request.user,
            status='scheduled'
        )

        recruiter_notifications = Interview.objects.filter(
            job__posted_by=request.user,
            status__in=['accepted', 'rejected']
        )

        combined = (candidate_notifications | recruiter_notifications).order_by('-created_at')

        notifications = list(combined[:5])

        return {
            'notifications': notifications,
            'notification_count': len(notifications)
        }

    return {}