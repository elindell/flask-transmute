import schematics

from .utils import base_type_to_json_schema_type


class Definitions(object):
    """
    this class handler returning the correct swagger type spec.
    it will handler returning the proper schema value.
    """

    def __init__(self):
        self._element_name = 'definitions'
        self._definitions = {}

    def get(self, schematics_type_instance):
        if not isinstance(schematics_type_instance, schematics.types.base.BaseType):
            raise Exception('{0} is not a schematics type'.format(schematics_type_instance))

        if not schematics_type_instance.is_compound:
            for primitive_type_class in base_type_to_json_schema_type:
                if isinstance(schematics_type_instance, primitive_type_class):
                    return base_type_to_json_schema_type[primitive_type_class]
            return {
                'type': 'string'
            }

        if isinstance(schematics_type_instance, schematics.types.compound.ListType):
            element_json_schema_type = self.get(schematics_type_instance.field)
            return {
                'type': 'array',
                'items': element_json_schema_type,
                'collectionFormat': 'multi'
            }
        if isinstance(schematics_type_instance, schematics.types.compound.DictType):
            value_json_schema_type = self.get(schematics_type_instance.field)
            return {
                'type': 'object',
                'additionalProperties': value_json_schema_type
            }

        model_class = schematics_type_instance.model_class
        model_class_str = '{}.{}'.format(
            model_class.__module__,
            model_class.__name__)
        ref = {
            '$ref': '#/{0}/{1}'.format(self._element_name, model_class_str)
        }

        if model_class not in self._definitions:
            required_fields = []
            properties = {}
            for field_name in schematics_type_instance.fields:
                field_schematics_type = schematics_type_instance.fields[field_name]
                properties[field_name] = self.get(field_schematics_type)
                if field_schematics_type.required:
                    required_fields.append(field_name)
            schema = {
                'type': 'object',
                'properties': properties,
            }
            if required_fields:
                schema['required'] = required_fields
            self._definitions[model_class_str] = schema

        return ref

    def add_to_spec(self, spec):
        spec[self._element_name] = self._definitions
