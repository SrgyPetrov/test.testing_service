from django.db.models import QuerySet


class AnswerQuerySet(QuerySet):

    def valid(self):
        return self.filter(is_valid=True)

    def invalid(self):
        return self.filter(is_valid=False)
