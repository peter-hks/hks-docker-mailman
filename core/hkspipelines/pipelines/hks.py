from mailman.pipelines.base import BasePipeline
from public import public
from mailman.core.i18n import _

@public
class HKSPipeline(BasePipeline):
    """HKS Default Pipeline"""

    name = 'hks-posting-pipeline'
    description = _('The default HKS posting pipeline.')

    _default_handlers = (
        'tagger',
        'member-recipients',
        'avoid-duplicates',
        'cleanse',
        'cleanse-dkim',
        'cook-headers',
        'subject-prefix',
        'rfc-2369',
        'to-archive',
        'to-digest',
        'to-usenet',
        'after-delivery',
        'acknowledge',
        # All decoration is now done in delivery.
        # 'decorate',
        'dmarc',
        'to-outgoing',
        )
