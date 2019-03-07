from cfb.namespace import Namespace
from cfb.reflection.BaseType import BaseType
from cfb.constants import SIZE_OF_UOFFSET, BASE_TYPE_SIZE, BASE_TYPE_RUST_TYPE, BASE_TYPE_DEFAULT
from cfb.struct import struct_padded_fields


class Context(object):
    def __init__(self, schema):
        self.schema = schema
        self.root = Namespace.from_schema(schema)

    def field_default(self, field):
        index = field.Type().Index()
        if index == -1:
            return BASE_TYPE_DEFAULT[field.Type().BaseType()]
        return self.enum_default(self.schema.Enums(index))

    def enum_default(self, enum):
        for i in range(enum.ValuesLength()):
            val = enum.Values(i)
            if val.Value() == 0:
                return '{0}::{1}'.format(self.base_name(enum), val.Name().decode('utf-8'))

    def field_present(self, field):
        base_type = field.Type().BaseType()
        if base_type == BaseType.Obj:
            return 'self.{0}.is_present()'.format(self.field_name(field))
        if base_type == BaseType.Bool:
            return 'self.{0}'.format(self.field_name(field))
        if base_type == BaseType.String or base_type == BaseType.Vector:
            return '!self.{0}.is_empty()'.format(self.field_name(field))

        return 'self.{0} != {1}'.format(self.field_name(field), self.field_default(field))

    def field_type(self, field):
        index = field.Type().Index()
        base_type = field.Type().BaseType()

        if index == -1:
            if base_type == BaseType.Vector:
                return "Vec<{0}>".format(self.rust_type(field.Type().Element()))

            return self.rust_type(base_type)
        else:
            if base_type == BaseType.Obj:
                return self.base_name(self.schema.Objects(index))
            else:
                return self.base_name(self.schema.Enums(index))

    def rust_type(self, cfb_type):
        return BASE_TYPE_RUST_TYPE[cfb_type]

    def field_size(self, field):
        base_type = field.Type().BaseType()
        if base_type == BaseType.Obj:
            obj = self.schema.Objects(field.Type().Index())
            if obj.IsStruct():
                return obj.Bytesize()

            return SIZE_OF_UOFFSET

        return BASE_TYPE_SIZE[field.Type().BaseType()]

    def field_alignment(self, field):
        base_type = field.Type().BaseType()
        if base_type == BaseType.Obj:
            obj = self.schema.Objects(field.Type().Index())
            if obj.IsStruct():
                return obj.Minalign()

            return SIZE_OF_UOFFSET

        return BASE_TYPE_SIZE[base_type]

    def table_alignment(self, table):
        return max(self.field_alignment(table.Fields(i)) for i in range(table.FieldsLength()))

    def element_aligment(self, field):
        element = field.Type().Element()
        if element == BaseType.Obj:
            obj = self.schema.Objects(field.Type().Index())
            if obj.IsStruct():
                return obj.Minalign()

            return SIZE_OF_UOFFSET

        return BASE_TYPE_SIZE[element]

    def full_name(self, object):
        return object.Name().decode('utf-8').replace('.', '::')

    def base_name(self, object):
        return object.Name().decode('utf-8').split('.')[-1]

    def field_name(self, field):
        return field.Name().decode('utf-8')

    def is_string(self, field):
        return field.Type().BaseType() == BaseType.String

    def is_vector(self, field):
        return field.Type().BaseType() == BaseType.Vector

    def is_element_scalar(self, field):
        element = field.Type().Element()
        if element == BaseType.Vector or element == BaseType.String or element == BaseType.Union:
            return False
        if element == BaseType.Obj:
            return self.schema.Objects(ty.Index()).IsStruct()

        return True

    def lifetime(self, object):
        for f in (object.Fields(i) for i in range(object.FieldsLength())):
            base_type = f.Type().BaseType()
            if base_type == BaseType.String:
                return "<'c>"

        return ''

    def struct_padded_fields(self, struct):
        return struct_padded_fields(self, struct)

    def fields_sorted_by_alignement(self, object):
        return list(sorted((object.Fields(i) for i in range(object.FieldsLength())),
                           key=lambda f: (self.field_alignment(f),
                                          self.field_size(f)),
                           reverse=True))

    def fields_sorted_by_offset(self, object):
        return list(sorted((object.Fields(i) for i in range(object.FieldsLength())),
                           key=lambda f: f.Offset(),
                           ))
