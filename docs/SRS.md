# Mahanaayak OS Software Requirements Specification

## 1. Introduction
Mahanaayak OS is an integrated constituency command center designed to monitor civic health, process citizen grievances, and output AI-assisted operational intelligence.

## 2. Core Modules
- **Authentication & RBAC**: Secure JWT-based access for Admins and Field Officers.
- **Citizen Management**: Identity and demographic tracking (Voter ID centric).
- **Grievance Engine**: Status tracking, severity prioritization, deduplication, and attachment handling.
- **GIS Intelligence**: Heatmaps and mapping coordinate correlation.
- **AI Synthesis**: Generation of manifestos, speeches, resource allocation matrices, and sentiment analysis via Google Gemini.

## 3. Security
- HttpOnly JWT Tokens
- Rate Limiting via Redis
- Input sanitization and automated schema validations

## 4. Scalability
- Redis-driven caching layer for analytics.
- Nginx reverse proxy load-balancing Gunicorn workers.
