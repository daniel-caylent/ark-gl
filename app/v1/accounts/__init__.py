"""This module contains all the lambda endpoints for the accounts business requirements"""

from .get.get import handler as get
from .post.post import handler as post
from .get_by_id.get import handler as get_by_id
from .put.put import handler as put
from .commit.put import handler as commit
from .upload.post import handler as upload
from .copy_all.post import handler as copy_all
