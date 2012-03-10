import formencode

class _Schema_Base(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = False

class FormLogin(_Schema_Base):
    email_address = formencode.validators.Email(not_empty=True)
    password = formencode.validators.UnicodeString(not_empty=True)
    remember_me = formencode.validators.Bool()
    
class FormSignup(_Schema_Base):
    email_address = formencode.validators.Email(not_empty=True)
    username = formencode.validators.UnicodeString(not_empty=True)
