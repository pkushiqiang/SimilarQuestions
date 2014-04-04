from collections import OrderedDict

class Cache(OrderedDict):
  def __init__(self, size_limit):
    self.size_limit = size_limit
    OrderedDict.__init__(self)
    self._check_size_limit()

  def __setitem__(self, key, value):
    OrderedDict.__setitem__(self, key, value)
    self._check_size_limit()

  def _check_size_limit(self):
    if self.size_limit is not None:
      while len(self) > self.size_limit:
        self.popitem(last=False)