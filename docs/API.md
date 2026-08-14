# API Documentation

The Mahanaayak OS backend utilizes standard REST architecture. Swagger documentation is exposed when the application is running.

## Base URL
`/api/v1`

## Accessing Swagger UI
1. Run the server
2. Navigate to `http://localhost:5000/apidocs`

## Key Endpoints
### Authentication (`/auth`)
- `POST /login` - Get JWT access/refresh tokens
- `POST /logout` - Blacklist token
- `POST /refresh` - Refresh JWT access token

### Citizens (`/citizens`)
- `GET /` - List citizens
- `POST /` - Create citizen

### Complaints (`/complaints`)
- `GET /` - Filterable complaints list
- `POST /` - Register new complaint with optional attachments

### Analytics & GIS (`/analytics`, `/gis`)
- `GET /analytics/admin-dashboard` - Aggregated AI-ready insights
- `GET /gis/heatmap` - GeoJSON intensity data

For a complete schema reference, use the Swagger `/apidocs` endpoint.
