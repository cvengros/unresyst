"""The constants used in Unresyst"""

_ = lambda x: x

MAX_LENGTH_NAME = 40
"""The maximum length of the name in the universal representation."""

MAX_LENGTH_CLASS_NAME = 20
"""The maximum length of the class name."""

MAX_LENGTH_ENTITY_TYPE = 2
"""The maximum length of the entity type string"""

MAX_LENGTH_RELATIONSHIP_TYPE = 5
"""The maximum length of the relationship type string"""

ENTITY_TYPE_SUBJECT = 'S'
"""The subject entity type"""

ENTITY_TYPE_OBJECT = 'O'
"""The object entity type"""

ENTITY_TYPE_SUBJECTOBJECT = 'SO'
"""The subject object entity type"""

ENTITY_TYPE_CHOICES = (
    # a subject:
    (ENTITY_TYPE_SUBJECT, _('Subject')),
    
    # an object:
    (ENTITY_TYPE_OBJECT, _('Object')),
    
    # when subject domain is the same as object domain
    (ENTITY_TYPE_SUBJECTOBJECT, _('Subject == Object')),
)
"""Choices for the entity_type field"""

RELATIONSHIP_TYPE_SUBJECT_OBJECT = 'S-O'
"""Subject-object relationship type"""

RELATIONSHIP_TYPE_SUBJECT_SUBJECT = 'S-S'
"""Subject-subject relationship type"""

RELATIONSHIP_TYPE_OBJECT_OBJECT = 'O-O'
"""Object-object relatioship type"""

RELATIONSHIP_TYPE_SUBJECTOBJECT_SUBJECTOBJECT = 'SO-SO'
"""Subjectobject-subjectobject relatioship type"""

RELATIONSHIP_TYPE_CHOICES = (
    # a subject-object relationship
    (RELATIONSHIP_TYPE_SUBJECT_OBJECT, _('Subejct-Object')),
    
    # a subject-subject relationship
    (RELATIONSHIP_TYPE_SUBJECT_SUBJECT, _('Subject-Subject')),
    
    # an object-object relationship
    (RELATIONSHIP_TYPE_OBJECT_OBJECT, _('Object-Object')),
    
    # a relationship for recommender where subject domain equals object domain
    (RELATIONSHIP_TYPE_SUBJECTOBJECT_SUBJECTOBJECT, _('SubjectObject-SubjectObject')),
)
"""Choices for the relationship_type field"""

DEFAULT_RECOMMENDATION_COUNT = 10
"""The defaul count of the obtained recommended objects"""
