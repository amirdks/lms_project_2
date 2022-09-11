from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from poll_module.models import PollOptions, Poll


def poll_render_to_string(pk):
    poll = get_object_or_404(Poll, pk=pk)
    poll_options = PollOptions.objects.filter(poll_id=poll.id)
    body = render_to_string('poll_module/include/poll_options_list_component.html',
                            context={'poll_options': poll_options, 'poll': poll})
    return body
