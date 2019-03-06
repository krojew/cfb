from cfb.namespace import Namespace
from cfb.reflection.BaseType import BaseType

SCALARS_SIZE = dict([
    (BaseType.Bool, 1),
    (BaseType.Byte, 1),
    (BaseType.Short, 2),
    (BaseType.Int, 4),
    (BaseType.Long, 8),
    (BaseType.UByte, 1),
    (BaseType.UShort, 2),
    (BaseType.UInt, 4),
    (BaseType.ULong, 8),
    (BaseType.Float, 4),
    (BaseType.Double, 8),
])


class Context(object):
    def __init__(self, schema):
        self.schema = schema
        self.root = Namespace.from_schema(schema)

    def if_not_default(self, field):
        return 'self.{0} != 0'.format(self.name_of(field))

    def size_of(self, field):
        return SCALARS_SIZE[field.Type().BaseType()]

    def alignment_of(self, field):
        return SCALARS_SIZE[field.Type().BaseType()]

    def max_alignment_of(self, object):
        return max(self.alignment_of(object.Fields(i)) for i in range(object.FieldsLength()))

    def name_of(self, entity):
        return entity.Name().decode('utf-8')
