from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np
import pandas as pd

from ..utils import resolution
from ..utils.doctools import document
from ..utils.exceptions import PlotnineError
from .stat import stat


@document
class stat_count(stat):
    """
    Counts the number of cases at each x position

    {documentation}

    .. rubric:: Options for computed aesthetics

    size
        - ``..count..`` - Number of observations at a position
        - ``..prop..`` - Ratio of points in the panel at a position

    See Also
    --------
    :class:`~plotnine.stats.stat_bin`
    """
    REQUIRED_AES = {'x'}
    DEFAULT_PARAMS = {'geom': 'histogram', 'position': 'stack',
                      'width': None}
    DEFAULT_AES = {'y': '..count..'}
    CREATES = {'y', 'width'}

    @classmethod
    def compute_group(cls, data, scales, **params):
        x = data['x']
        if ('y' in data) or ('y' in params):
            msg = 'stat_count() must not be used with a y aesthetic'
            raise PlotnineError(msg)

        weight = data.get('weight', np.ones(len(x)))
        width = params['width']
        if width is None:
            width = resolution(x, False) * 0.9
        df = pd.DataFrame({'weight': weight, 'x': x})
        # weighted frequency count
        count = pd.pivot_table(df, values='weight',
                               index=['x'],
                               aggfunc=np.sum)
        count = count.values
        return pd.DataFrame({'count': count,
                             'prop': count / np.abs(count).sum(),
                             'x': x.unique(),
                             'width': width})