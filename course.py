class Course:
    def __init__(self, name, trimester, credits, grade=None):
        self.name = name
        self.trimester = trimester
        self.credits = credits
        self.grade = grade  # Optional grade attribute

    def to_dict(self):
        return {
            'name': self.name,
            'trimester': self.trimester,
            'credits': self.credits,
            'grade': self.grade
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['trimester'], data['credits'], data['grade'])

