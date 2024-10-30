from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from appss.models import Informant

class Command(BaseCommand):
    help = 'Links existing Informants to corresponding User accounts'

    def handle(self, *args, **kwargs):
        # Loop over each Informant record that currently has no linked User
        unlinked_informants = Informant.objects.filter(user__isnull=True)
        for informant in unlinked_informants:
            # Attempt to find a User account based on some criteria (e.g., username, email)
            # This is an example; adjust the matching logic as needed.
            try:
                user = User.objects.get(username=informant.contact_number)  # Or some other matching criteria
                informant.user = user
                informant.save()
                self.stdout.write(self.style.SUCCESS(f'Linked Informant {informant.id} to User {user.username}'))
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'No matching User found for Informant {informant.id}'))
