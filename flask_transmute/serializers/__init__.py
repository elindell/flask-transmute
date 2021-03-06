from .exceptions import SerializerException
from .basetype_serializers import *
from .cache import SerializerCache
from .or_serializer import Or


def get_serializer(cls):
    global _global_serializer_cache
    return _global_serializer_cache[cls]

_global_serializer_cache = SerializerCache()
