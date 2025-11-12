from django.core.management.base import BaseCommand
from wagtail.models import Site

from home.models import FooterSettings


class Command(BaseCommand):
    help = 'Seeds footer settings with initial content'

    def handle(self, *args, **options):
        # Get the default site
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            self.stdout.write(
                self.style.ERROR('No default site found. Please create a site first.')
            )
            return

        # Seed footer settings
        footer_settings, created = FooterSettings.objects.get_or_create(
            site=site
        )

        if not created:
            self.stdout.write(
                self.style.WARNING('Footer settings already exist. Updating content...')
            )

        footer_settings.heading = 'Resolve'

        # Column 1: Taglines
        footer_settings.column_1 = [
            {
                'type': 'paragraph',
                'value': '<p>Makes machines empower humans</p>',
            },
            {
                'type': 'paragraph',
                'value': '<p>Made by 👨 and 🤖 in Europe</p>',
            }
        ]

        # Column 2: Contact information
        footer_settings.column_2 = [
            {
                'type': 'definition_list',
                'value': {
                    'items': [
                        {
                            'term': 'LinkedIn',
                            'definition': '<p><a target="_blank" href="https://www.linkedin.com/in/johanschuijt/">https://www.linkedin.com/in/johanschuijt/</a></p>',
                        },
                        {
                            'term': 'GitHub',
                            'definition': '<p><a target="_blank" href="https://github.com/monneyboi/">https://github.com/monneyboi/</a></p>',
                        },
                        {
                            'term': 'Email',
                            'definition': '<p><a href="mailto:johan@resolve.works">johan@resolve.works</a></p>',
                        },
                        {
                            'term': 'Phone',
                            'definition': '<p><a href="tel:+31651952461">+31 651 952 461</a></p>',
                        },
                    ]
                }
            }
        ]

        # Column 3: Business registration
        footer_settings.column_3 = [
            {
                'type': 'definition_list',
                'value': {
                    'items': [
                        {
                            'term': 'Address',
                            'definition': '<p>Harju maakond, Tallinn, Lasnamäe linnaosa, Sepapaja tn 6, 15551</p>',
                        },
                        {
                            'term': 'VAT',
                            'definition': '<p>EE102834268</p>',
                        },
                        {
                            'term': 'Register',
                            'definition': '<p><a href="https://ariregister.rik.ee/eng/company/17154517/RESOLVE-SERVICES-OÜ" target="_blank">https://ariregister.rik.ee</a></p>',
                        },
                    ]
                }
            },
            {
                'type': 'paragraph',
                'value': '<p>Estonian e-residency program</p>',
            }
        ]

        footer_settings.save()

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded footer settings!')
        )
