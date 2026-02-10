from blog.models import Post,Category
from django.core.management.base import BaseCommand
import random

class Command(BaseCommand):
    help = 'This Commands inserts post data'

    def handle(self, *args, **options):
        
        Post.objects.all().delete()

        titles = [
            'The Future of AI',
            'Climate Change Solutions',
            'Remote Work Trends',
            'Quantum Computing Explained',
            'Renewable Energy Innovations',
            'Deep Learning Demystified',
            'Post-Pandemic Economic Outlook',
            'Blockchain in Finance',
            'Storytelling in Marketing',
            'Medical Technology Advances',
            'Space Exploration Challenges',
            'Psychology of Decision Making',
            'Evolution of Social Media',
            'The Art of Cooking',
            'Cultural Diversity in Society',
            'Sustainable Development Investments',
            'Globalization Impact',
            'Power of Mindfulness',
            'Online Learning Revolution',
            'Art and Technology Fusion',
        ]

        contents = [
            'The Future of AI: Showcases how intelligent systems are reshaping business strategy and operational velocity.',
            'Climate Change Solutions: Outlines scalable interventions driving climate resilience and carbon-neutral growth.',
            'Remote Work Trends: Highlights emerging workflows redefining distributed productivity and talent engagement.', 
            'Quantum Computing Explained: Breaks down how quantum acceleration will unlock next-gen problem-solving capabilities.',
            'Renewable Energy Innovations: Captures breakthrough technologies accelerating the clean-energy transition.',
            'Deep Learning Demystified: Simplifies advanced neural models powering data-driven competitive advantage.',
            'Post-Pandemic Economic Outlook: Examines shifting market dynamics and recovery pathways shaping global GDP.',
            'Blockchain in Finance: Explores decentralised frameworks elevating trust, security, and transaction efficiency.',
            'Storytelling in Marketing: Focuses on narrative-driven campaigns that elevate customer affinity and brand equity.',
            'Medical Technology Advances: Showcases cutting-edge med-tech solutions transforming patient outcomes end-to-end.', 
            'Space Exploration Challenges: Summarises mission-critical hurdles influencing next-gen interplanetary operations.',
            'Psychology of Decision Making: Breaks down cognitive triggers driving consumer and organisational behaviour.',
            'Evolution of Social Media: Tracks platform shifts redefining engagement, influence, and digital community building.',
            'The Art of Cooking: Highlights culinary craftsmanship that merges tradition with modern gastronomic innovation.',
            'Cultural Diversity in Society: Underscores inclusive practices strengthening collaboration and shared value creation.',
            'Sustainable Development Investments: Maps capital flows steering long-term, eco-centric economic growth.',
            'Globalization Impact: Analyses cross-border trends reshaping trade, workforce mobility, and global synergies.',
            'Power of Mindfulness: Emphasises mental frameworks that uplift productivity, clarity, and leadership agility.',
            'Online Learning Revolution: Captures digital-first learning ecosystems democratising skills at enterprise scale.',
            'Art and Technology Fusion: Celebrates the convergence of creativity and innovation driving immersive experiences.'
        ]

        img_urls = [
            'https://picsum.dev/static/1/800/400',
            'https://picsum.dev/static/2/800/400',
            'https://picsum.dev/static/3/800/400',
            'https://picsum.dev/static/4/800/400',
            'https://picsum.dev/static/5/800/400',
            'https://picsum.dev/static/6/800/400',
            'https://picsum.dev/static/117/800/400',
            'https://picsum.dev/static/8/800/400',
            'https://picsum.dev/static/9/800/400',
            'https://picsum.dev/static/10/800/400',
            'https://picsum.dev/static/11/800/400',
            'https://picsum.dev/static/12/800/400',
            'https://picsum.dev/static/13/800/400',
            'https://picsum.dev/static/14/800/400',
            'https://picsum.dev/static/15/800/400',
            'https://picsum.dev/static/16/800/400',
            'https://picsum.dev/static/17/800/400',
            'https://picsum.dev/static/18/800/400',
            'https://picsum.dev/static/19/800/400',
            'https://picsum.dev/static/20/800/400',
        ]

        categories = Category.objects.all()
        for title, content, img_url in zip(titles,contents,img_urls):
            category = random.choice(categories)
            Post.objects.create(title=title, content=content, img_url=img_url, category=category)

        self.stdout.write(self.style.SUCCESS('Completed inserting post data'))
        