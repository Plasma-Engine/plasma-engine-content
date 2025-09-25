# Plasma Engine Content

## Overview

**Plasma Engine Content** is the AI-powered content generation and publishing service. It enables:

- ✍️ **Multi-Format Generation**: Articles, social posts, newsletters, scripts
- 🎨 **Brand Voice Consistency**: Style guide enforcement and tone matching
- 🖼️ **Media Creation**: Image generation, video scripts, infographics
- 📅 **Content Calendar**: Scheduling and campaign management
- 🔄 **Cross-Platform Publishing**: Direct posting to multiple channels
- 📊 **Performance Tracking**: Engagement metrics and A/B testing

## Tech Stack

- **Language**: Python 3.11
- **Framework**: FastAPI
- **AI Models**: OpenAI, Anthropic, Stability AI
- **Queue**: Celery + Redis
- **Database**: PostgreSQL
- **Storage**: S3 for media assets
- **CMS**: Headless CMS integration
- **Analytics**: Segment, Mixpanel

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload

# Run tests
pytest

# Start Celery worker
celery -A app.tasks worker --loglevel=info
```

## Architecture

```
Request → Template Selection → AI Generation → Review/Edit → Publishing
             ↓                      ↓              ↓            ↓
         Brand Rules            Prompts       Human Loop    Platforms
```

## Key Features

- **Template Library**: Pre-built content frameworks
- **SEO Optimization**: Keyword integration, meta generation
- **Plagiarism Check**: Originality verification
- **Version Control**: Content revision history
- **Workflow Automation**: Approval chains and staging
- **Localization**: Multi-language content generation

## Content Types

- **Long-form**: Blog posts, whitepapers, case studies
- **Social Media**: X/Twitter threads, LinkedIn posts, Instagram captions
- **Email**: Newsletters, drip campaigns, transactional
- **Video**: Scripts, subtitles, descriptions
- **Technical**: Documentation, API guides, tutorials

## Publishing Channels

- **Social**: X/Twitter, LinkedIn, Facebook, Instagram
- **Blog**: WordPress, Medium, Ghost, Webflow
- **Email**: SendGrid, Mailchimp, ConvertKit
- **CMS**: Contentful, Strapi, Sanity

## Development

See [Development Handbook](../plasma-engine-shared/docs/development-handbook.md) for guidelines.

## CI/CD

This repository uses GitHub Actions for CI/CD. All PRs are automatically:
- Linted and tested
- Security scanned
- Reviewed by CodeRabbit

See `.github/workflows/ci.yml` for details.