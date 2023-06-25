import sqlalchemy.types as types


class ChoiceType(types.TypeDecorator):
    impl = types.String

    def __init__(self, choices, **kwargs):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kwargs)

    def process_bind_param(self, value, dialect):
        print(value)
        print(self.choices.items())
        return [k for k, v in self.choices.items() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices.get(value)
