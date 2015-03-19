# rice/error.py
#
# Defines a various Exception classes.
#

# Default error.
class Error(Exception):
  pass

# For corrupted files and downloads.
class CorruptionError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

