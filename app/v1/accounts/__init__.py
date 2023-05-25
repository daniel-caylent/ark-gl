"""This module contains all the lambda endpoints for the accounts business requirements"""

from .get.get import handler as get
from .post.post import handler as post
from .get_by_id.get import handler as get_by_id
from .put.put import handler as put
from .state.put import handler as state
