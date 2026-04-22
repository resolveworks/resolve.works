import os

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from wagtail.images.models import Image
from wagtail.models import Page, Site
from wagtail.users.models import UserProfile

from accounts.models import User, WorkExperience
from articles.models import ArticleIndexPage
from home.models import BusinessSettings, ContactSettings, FooterSettings, HomePage


class Command(BaseCommand):
    help = "Seeds the homepage and footer with initial content"

    def handle(self, *args, **options):
        profile_image = self.get_or_create_profile_image()
        user = self.seed_user(profile_image)
        self.seed_homepage(user)
        self.seed_articles()
        self.seed_footer()
        self.seed_business_settings()
        self.seed_contact_settings()
        self.stdout.write(self.style.SUCCESS("Successfully seeded all content!"))

    def get_or_create_profile_image(self):
        """Load or create the profile image."""
        try:
            return Image.objects.get(title="Profile shot of Johan")
        except Image.DoesNotExist:
            image_path = "./images/profile.webp"
            if os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    profile_image = Image(
                        title="Profile shot of Johan",
                        file=ImageFile(f, name="profile.webp"),
                    )
                    profile_image.save()
                    self.stdout.write(self.style.SUCCESS("Created profile image"))
                    return profile_image
            else:
                self.stdout.write(
                    self.style.WARNING(f"Profile image not found at {image_path}")
                )
                return None

    def seed_user(self, profile_image):
        user, created = User.objects.get_or_create(
            username="johan",
            defaults={
                "email": "johan@resolve.works",
                "first_name": "Johan",
                "last_name": "Schuijt",
                "job_title": "Founder",
                "bio": "I am an autodidact software and data engineer who loves turning ambiguous problems into practical, human-centered systems. With 15+ years of experience I spot inefficiencies in processes very quickly. I use LLMs to accelerate development, but never at the expense of clarity, reliability, or ethics.\n\nI work remotely, Europe-focused but global clients welcome.",
                "linkedin_url": "https://www.linkedin.com/in/johanschuijt/",
                "github_url": "https://github.com/monneyboi/",
                "phone": "+31651952461",
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if created:
            self.stdout.write(self.style.SUCCESS("Created user 'johan'"))
        else:
            self.stdout.write(
                self.style.WARNING("User 'johan' already exists, skipping")
            )

        # Set the user's profile avatar
        self.seed_user_avatar(user, profile_image)

        # Seed work experiences
        self.seed_work_experiences(user)

        return user

    def seed_user_avatar(self, user, wagtail_image):
        """Set the user's Wagtail profile avatar from a Wagtail Image."""
        if not wagtail_image:
            return

        user_profile = UserProfile.get_for_user(user)
        if user_profile.avatar:
            self.stdout.write(self.style.WARNING("User avatar already set, skipping"))
            return

        # Copy the image file to the avatar field
        image_path = wagtail_image.file.path
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                user_profile.avatar.save(
                    os.path.basename(image_path),
                    ImageFile(f),
                    save=True,
                )
            self.stdout.write(self.style.SUCCESS("Set user avatar"))

    def seed_work_experiences(self, user):
        """Seed work experience entries for a user."""
        experiences = [
            {
                "company": "OpenSanctions",
                "role": "Data Engineer",
                "start_year": 2025,
                "end_year": None,
            },
            {
                "company": "Follow the Money",
                "role": "Full Stack Developer",
                "start_year": 2021,
                "end_year": 2025,
            },
            {
                "company": "Forest.host",
                "role": "Founder",
                "start_year": 2017,
                "end_year": 2021,
            },
        ]

        for exp in experiences:
            obj, created = WorkExperience.objects.get_or_create(
                user=user,
                company=exp["company"],
                defaults={
                    "role": exp["role"],
                    "start_year": exp["start_year"],
                    "end_year": exp["end_year"],
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created work experience: {exp['company']}")
                )

    def seed_homepage(self, user):
        # Check if HomePage already exists
        if HomePage.objects.filter(slug="home").exists():
            self.stdout.write(self.style.WARNING("HomePage already exists, skipping"))
            return

        # Clear default Wagtail site and welcome page
        Site.objects.all().delete()
        root_page = Page.objects.get(slug="root")
        for page in root_page.get_children():
            page.delete()
        root_page.refresh_from_db()
        self.stdout.write(self.style.SUCCESS("Cleared default Wagtail content"))

        # Create new HomePage
        home_page = HomePage(
            title="IT Consulting for ethical SMBs",
            slug="home",
            seo_title="IT Consulting for ethical SMBs",
            search_description="We help ethical business build modern software to save time without replacing people.",
            owner=user,
        )
        root_page.add_child(instance=home_page)
        self.stdout.write(self.style.SUCCESS("Created new HomePage"))

        # Set the homepage content
        home_page.body = [
            {
                "type": "hero",
                "value": {
                    "heading": "Change your trajectory",
                    "body_text": "We help ethical business build modern software to save time without replacing people.",
                },
            },
            {
                "type": "section",
                "value": {
                    "title": "Understandable process",
                    "background": "light",
                    "content": [
                        {
                            "type": "paragraph",
                            "value": "<p>From roadmap to rollout, we prototype rapidly and build production systems with your team. Our approach is:</p>",
                        },
                        {
                            "type": "features",
                            "value": {
                                "columns": "3",
                                "features": [
                                    {
                                        "heading": "Human-centered",
                                        "description": "<p>We don't aim to replace people, but <b>amplify their capabilities</b>.</p>",
                                    },
                                    {
                                        "heading": "Flexible",
                                        "description": "<p>We meet you where you are, hooking into <b>what you already know.</b></p>",
                                    },
                                    {
                                        "heading": "Transparent",
                                        "description": "<p><b>You are involved</b>, understand the process, and give direction.</p>",
                                    },
                                ],
                            },
                        },
                    ],
                },
            },
            {
                "type": "section",
                "value": {
                    "title": "We resolve",
                    "background": "dark",
                    "content": [
                        {
                            "type": "features",
                            "value": {
                                "columns": "4",
                                "features": [
                                    {
                                        "heading": "Bottlenecks",
                                        "description": "<p>Those specific points where work gets stuck or slowed down</p>",
                                    },
                                    {
                                        "heading": "Repetitive drain",
                                        "description": "<p>Tasks that exhaust people without adding value</p>",
                                    },
                                    {
                                        "heading": "Information silos",
                                        "description": "<p>When knowledge is trapped and hard to access</p>",
                                    },
                                    {
                                        "heading": "Decision delays",
                                        "description": "<p>When people wait for approvals that could be automated</p>",
                                    },
                                    {
                                        "heading": "Scaling friction",
                                        "description": "<p>When growth creates operational chaos</p>",
                                    },
                                    {
                                        "heading": "Tool complexity",
                                        "description": "<p>When systems make work harder instead of easier</p>",
                                    },
                                    {
                                        "heading": "Resource limitations",
                                        "description": "<p>Doing more with the same team size</p>",
                                    },
                                    {
                                        "heading": "Knowledge gaps",
                                        "description": "<p>When expertise is needed but not available</p>",
                                    },
                                    {
                                        "heading": "Workflow confusion",
                                        "description": "<p>When processes are unclear or inconsistent</p>",
                                    },
                                    {
                                        "heading": "Communication overhead",
                                        "description": "<p>When coordination takes more time than the actual work</p>",
                                    },
                                ],
                            },
                        },
                    ],
                },
            },
            {
                "type": "section",
                "value": {
                    "title": "From roadmap to rollout",
                    "background": "light",
                    "content": [
                        {
                            "type": "process_roadmap",
                            "value": {
                                "steps": [
                                    {
                                        "title": "Diagnose",
                                        "description": "Goals, data, constraints, and risks",
                                    },
                                    {
                                        "title": "Prototype",
                                        "description": "Rapid iterations with real user flows",
                                    },
                                    {
                                        "title": "Pilot",
                                        "description": "Roll out to a small group",
                                    },
                                    {
                                        "title": "Scale",
                                        "description": "Adapt, monitor, and train the team",
                                    },
                                ]
                            },
                        }
                    ],
                },
            },
            {
                "type": "section",
                "value": {
                    "title": "Showcase solution",
                    "background": "light",
                    "content": [
                        {
                            "type": "definition_list",
                            "value": {
                                "items": [
                                    {
                                        "term": "Project",
                                        "definition": '<p><a href="https://loom.everypolitician.org">PoliLoom</a>: Structuring politicians\' data for investigators and the accountability sector.</p>',
                                    },
                                    {
                                        "term": "Client",
                                        "definition": '<p><a href="https://www.opensanctions.org/">OpenSanctions</a></p>',
                                    },
                                    {
                                        "term": "Role",
                                        "definition": "<p>Data Engineer (2025–present)</p>",
                                    },
                                ]
                            },
                        },
                        {
                            "type": "features",
                            "value": {
                                "columns": "3",
                                "features": [
                                    {
                                        "heading": "The problem",
                                        "description": "<p>Assemble and verify structured politician data from Wikipedia/Wikidata and the wider web, across languages, ensuring provenance, correctness, and scale.</p>",
                                    },
                                    {
                                        "heading": "Solution highlights",
                                        "description": "<p><b>Two-stage extraction pipeline</b>: LLM extracts free-text positions → hybrid search maps to existing entities → LLM reconciles.</p><p><b>Fast hybrid search</b>: Meilisearch with OpenAI embeddings for combined semantic and lexical entity matching</p><p><b>Source verification</b>: web sources archived as MHTML via Playwright and reviewed through a FastAPI + Next.js confirmation UI</p>",
                                    },
                                    {
                                        "heading": "Impact",
                                        "description": "<p><b>Clarity</b>: From unstructured source documents to structured, linkable records.</p><p><b>Trust</b>: Every extracted fact links back to a specific passage in an archived snapshot of the source.</p><p><b>Scale</b>: Handles Wikidata-sized inputs through an incremental, parallelized pipeline.</p>",
                                    },
                                ],
                            },
                        },
                        {
                            "type": "paragraph",
                            "value": '<p>LLM entity reconciliation actually works well, and with human-in-the-loop verification, it\'s both accurate and accountable. <a href="https://discuss.opensanctions.org/t/poliloom-loom-for-weaving-politicians-data/121">Read the devlog</a>.</p>',
                        },
                    ],
                },
            },
            {
                "type": "section",
                "value": {
                    "title": "About Johan",
                    "background": "light",
                    "content": [
                        {
                            "type": "about_founder",
                            "value": {"user": str(user.pk)},
                        },
                    ],
                },
            },
            {
                "type": "section",
                "value": {
                    "title": "Frequently asked questions",
                    "background": "light",
                    "content": [
                        {
                            "type": "faq",
                            "value": {
                                "items": [
                                    {
                                        "question": "What kinds of problems are you best at solving?",
                                        "answer": "<p>Data problems where information is scattered, unstructured, or trapped in formats that don't talk to each other. Think: extracting structured facts from thousands of documents, connecting data across systems, or building pipelines that turn messy inputs into something reliable and searchable.</p><p>I use LLMs where they genuinely help—extraction, matching, classification—but they're usually one piece of a larger system. If your problem is better solved with a spreadsheet or a well-written SQL query, I'll tell you that.</p>",
                                    },
                                    {
                                        "question": "How involved does our team need to be?",
                                        "answer": "<p>More at the start, less over time. Early on I need access to the people who understand the problem—what's actually painful, what the data looks like, what \"good enough\" means. That might be a few hours in the first week or two.</p><p>During prototyping I'll share work frequently and need feedback. Once we're building for real, involvement drops to occasional check-ins and testing. By handover, the goal is that your team understands what's running and can operate it without me.</p>",
                                    },
                                    {
                                        "question": "What does a typical project timeline look like?",
                                        "answer": "<p>It depends entirely on the problem. A small integration might take a few weeks; a complex data pipeline with verification workflows takes months and evolves as we learn what actually works.</p><p>Rather than give you made-up estimates, I'd point you to the <a href=\"https://discuss.opensanctions.org/t/poliloom-loom-for-weaving-politicians-data/121\">PoliLoom devlog</a>—it shows how a real project unfolded, including the dead ends and course corrections. That's more honest than a tidy timeline.</p><p>What I can promise: I ship early and often. You'll see working pieces within the first few weeks, not a big reveal after months of silence.</p>",
                                    },
                                    {
                                        "question": "Who owns the code?",
                                        "answer": "<p>You do. Everything I build for you is yours—code, configurations, documentation. I prefer to build things that could be open-sourced if you wanted, and I'll actively suggest it when it makes sense. No vendor lock-in, no proprietary dependencies that tie you to me.</p>",
                                    },
                                    {
                                        "question": "Do you also build the user interface, or just the backend?",
                                        "answer": "<p>Both. I design and build the full system—data pipelines, APIs, and the interface people actually use. A clear UI isn't optional; it's what makes the difference between a tool that gets used and one that gets abandoned.</p>",
                                    },
                                    {
                                        "question": "What do you need from us to figure out if we're a good fit?",
                                        "answer": "<p>A conversation about the actual problem—not a polished pitch, just what's frustrating and why it matters. I work best with organizations doing something meaningful: journalism, accountability, public interest, open data, or businesses that genuinely care about doing good work rather than just scaling revenue.</p><p>If your goal is \"add AI to make investors happy,\" we're probably not a match. If you're trying to solve a real problem and want to understand what you're building, let's talk.</p>",
                                    },
                                ]
                            },
                        }
                    ],
                },
            },
        ]

        home_page.save()

        # Update or create the site to use this homepage
        site = Site.objects.filter(is_default_site=True).first()
        if site:
            site.root_page = home_page
            site.save()
        else:
            Site.objects.create(
                hostname="localhost",
                root_page=home_page,
                is_default_site=True,
                site_name="Resolve.",
            )
        self.stdout.write(self.style.SUCCESS("Updated site to use HomePage as root"))
        self.stdout.write(self.style.SUCCESS("Successfully seeded homepage content!"))

    def seed_articles(self):
        """Seed article index and example article."""
        home_page = HomePage.objects.filter(slug="home").first()
        if not home_page:
            self.stdout.write(
                self.style.ERROR("HomePage not found. Please seed homepage first.")
            )
            return

        # Check if ArticleIndexPage already exists
        if ArticleIndexPage.objects.filter(slug="articles").exists():
            self.stdout.write(
                self.style.WARNING("ArticleIndexPage already exists, skipping")
            )
            return

        # Create article index page
        article_index = ArticleIndexPage(
            title="Articles",
            slug="articles",
            intro="<p>Thoughts on AI, automation, and building practical systems.</p>",
        )
        home_page.add_child(instance=article_index)
        self.stdout.write(self.style.SUCCESS("Created ArticleIndexPage"))

    def seed_footer(self):
        # Get the default site
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            self.stdout.write(
                self.style.ERROR("No default site found. Please create a site first.")
            )
            return

        # Check if footer settings already exist
        if FooterSettings.objects.filter(site=site).exists():
            self.stdout.write(
                self.style.WARNING("Footer settings already exist, skipping")
            )
            return

        # Create footer settings
        footer_settings = FooterSettings(site=site)

        # Tagline
        footer_settings.tagline = (
            "<p>Makes machines empower humans</p><p>Made by 👨 and 🤖 in Europe</p>"
        )

        footer_settings.registration_note = "Estonian e-residency program"

        footer_settings.save()
        self.stdout.write(self.style.SUCCESS("Successfully seeded footer settings!"))

    def seed_business_settings(self):
        # Get the default site
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            self.stdout.write(
                self.style.ERROR("No default site found. Please create a site first.")
            )
            return

        # Check if business settings already exist
        if BusinessSettings.objects.filter(site=site).exists():
            self.stdout.write(
                self.style.WARNING("Business settings already exist, skipping")
            )
            return

        # Create business settings
        business_settings = BusinessSettings(site=site)
        business_settings.name = "Resolve."
        business_settings.description = (
            "Expert AI consulting services for ethical SMBs. "
            "We implement large language models (LLMs) to automate workflows, "
            "reduce costs, and amplify human capabilities."
        )
        business_settings.phone = "+31651952461"
        business_settings.email = "johan@resolve.works"
        business_settings.address_country = "Estonia"
        business_settings.price_range = "€€€"
        business_settings.opening_hours = "Mo-Fr 09:00-18:00"

        # Social links
        business_settings.linkedin_url = "https://www.linkedin.com/in/johanschuijt/"
        business_settings.github_url = "https://github.com/monneyboi/"

        # Business registration
        business_settings.address = (
            "Harju maakond, Tallinn, Lasnamäe linnaosa, Sepapaja tn 6, 15551"
        )
        business_settings.vat_number = "EE102834268"
        business_settings.register_url = (
            "https://ariregister.rik.ee/eng/company/17154517/RESOLVE-SERVICES-OÜ"
        )

        # Set founder
        try:
            founder = User.objects.get(username="johan")
            business_settings.founder = founder
        except User.DoesNotExist:
            self.stdout.write(
                self.style.WARNING("User 'johan' not found. Founder not set.")
            )

        business_settings.save()
        self.stdout.write(self.style.SUCCESS("Successfully seeded business settings!"))

    def seed_contact_settings(self):
        # Get the default site
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            self.stdout.write(
                self.style.ERROR("No default site found. Please create a site first.")
            )
            return

        # Check if contact settings already exist
        if ContactSettings.objects.filter(site=site).exists():
            self.stdout.write(
                self.style.WARNING("Contact settings already exist, skipping")
            )
            return

        # Create contact settings
        contact_settings = ContactSettings(site=site)
        contact_settings.email_subject = "Free consultation request"
        contact_settings.email_body = (
            "Hi,\n\n"
            "We're curious about how you could help us with our current challenge.\n\n"
            "...\n\n"
            "Best regards,\n"
            "..."
        )

        contact_settings.save()
        self.stdout.write(self.style.SUCCESS("Successfully seeded contact settings!"))
