""".. Ignore pydocstyle D400.

==============
Celery Manager
==============

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import sys

from django.conf import settings

from resolwe.flow.models import Process
from resolwe.flow.tasks import celery_run
from resolwe.utils import BraceMessage as __

from .base import BaseManager

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


try:
    import celery  # pylint: disable=unused-import
except ImportError:
    logger.error("Please install Celery using 'pip install celery'", file=sys.stderr)
    sys.exit(1)


class Manager(BaseManager):
    """Celery-based manager for job execution."""

    def run(self, data, dest_dir, argv, verbosity=1):
        """Run process.

        For details, see
        :meth:`~resolwe.flow.managers.base.BaseManager.run`.
        """
        queue = 'ordinary'
        if data.process.scheduling_class == Process.SCHEDULING_CLASS_INTERACTIVE:
            queue = 'hipri'

        logger.debug(__(
            "Manager '{}.{}' running {} in celery queue {}, EAGER is {}.",
            self.__class__.__module__,
            self.__class__.__name__,
            repr(argv),
            queue,
            getattr(settings, 'CELERY_ALWAYS_EAGER', None)
        ))
        celery_run.apply_async((data.id, dest_dir, argv, verbosity), queue=queue)