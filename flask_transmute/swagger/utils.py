import schematics


base_type_to_json_schema_type = {
    schematics.types.base.IntType: {
        'type': 'integer',
    },
    schematics.types.base.BooleanType: {
        'type': 'boolean'
    },
    schematics.types.base.DateType: {
        'type': 'string',
        'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
    },
    schematics.types.base.DecimalType: {
        'type': 'string'
    },
    schematics.types.base.StringType: {
        'type': 'string'
    },
    schematics.types.base.UUIDType: {
        'type': 'string'
    },
    schematics.types.base.DateTimeType: {
        'type': 'string',
        'format': 'date-time'
    },
    schematics.types.base.NumberType: {
        'type': 'number'
    },
    schematics.types.base.FloatType: {
        'type': 'number'
    },
    schematics.types.base.MultilingualStringType: {
        'type': 'string'
    },
    schematics.types.base.SHA1Type: {
        'type': 'string'
    },
    schematics.types.base.LongType: {
        'type': 'integer'
    },
    schematics.types.base.UTCDateTimeType: {
        'type': 'string',
        'format': 'date-time'
    },
    schematics.types.base.MD5Type: {
        'type': 'string'
    },
    schematics.types.base.TimestampType: {
        'type': 'number'
    },
    schematics.types.base.GeoPointType: {
        'type': 'array',
        'items': {
            'type': 'integer'
        },
        'minItems': 2,
        'maxItems': 2
    },
}
