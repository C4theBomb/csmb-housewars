from django.db.models import Manager, F


class Session1Activities(Manager):
    def below_quota(self):
        signupIDs = [act.id for act in self.get_queryset() if act.quota >
                     act.session1_signups]

        return self.filter(id__in=signupIDs).order_by('time', 'name')


class Session2Activities(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(time=30)

    def below_quota(self):
        signupIDs = [act.id for act in self.filter(time=30) if act.quota >
                     act.session2_signups]

        return self.filter(id__in=signupIDs).order_by('name')
