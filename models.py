class User:
    userSchema = {
        'bsonType': 'object',
        'additionalProperties': True,
        'required': ['email', 'password', 'location', 'is_artist'],
        'properties': {
            'name': {
                'bsonType': 'string',
            },
            'email': {
                'bsonType': 'string'
            },
            'password': {
                'bsonType': 'string',
                'minimum': 8,
                'maximum': 255
            },
            'profile_pic': {
                'bsonType': 'string'
            },
            'bio': {
                'bsonType': 'string'
            },
            'is_artist': {
                'type': 'boolean',
                # 'default': False
            },
            'location': {
                'bsonType': 'object',
                'required': ['city', 'state'],
                'properties': {
                    'city': {
                        'bsonType': 'string'
                    },
                    'state': {
                        'bsonType': 'string'
                    }
                }
            }
        }
    }