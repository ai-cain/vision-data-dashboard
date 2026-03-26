# Architecture

## High-level layering

The project follows a deliberate separation of concerns:

- `models/`: persistence structure
- `schemas/`: request parsing and serialization
- `services/`: business logic
- `routes/`: thin HTTP and WebSocket controllers
- `frontend/src/pages/`: page composition
- `frontend/src/hooks/`: API-bound query hooks and realtime hooks

## REST request flow

```mermaid
sequenceDiagram
    participant UI as React UI
    participant API as Flask Route
    participant SVC as Service Layer
    participant DB as PostgreSQL

    UI->>API: GET /api/v1/stats/overview
    API->>SVC: get_dashboard_overview()
    SVC->>DB: query devices/events/inspections
    DB-->>SVC: rows
    SVC-->>API: aggregated payload
    API-->>UI: JSON response
```

## Realtime event flow

```mermaid
sequenceDiagram
    participant Writer as Event Producer
    participant API as POST /api/v1/events
    participant SVC as event_service
    participant Broker as EventStreamBroker
    participant UI as Dashboard

    Writer->>API: create vision event
    API->>SVC: create_event(payload)
    SVC->>Broker: publish(event.created)
    Broker-->>UI: ws /ws/events message
    UI->>UI: merge into React Query cache
```

## Repository map

```text
vision-data-dashboard/
|-- backend/
|   |-- app/
|   |   |-- models/
|   |   |-- routes/
|   |   |-- schemas/
|   |   |-- services/
|   |-- migrations/
|   |-- tests/
|   |-- requirements.txt
|   |-- requirements-dev.txt
|-- frontend/
|   |-- src/
|   |   |-- components/
|   |   |-- hooks/
|   |   |-- lib/
|   |   |-- pages/
|   |   |-- test/
|   |   |-- types/
|-- docs/
|-- .github/workflows/
|-- docker-compose.yml
|-- mkdocs.yml
```

## Why this structure

### Backend

Routes stay intentionally thin so that:

- request parsing remains simple
- business logic is testable outside HTTP concerns
- auth and live stream behavior stay centralized in services

### Frontend

The frontend is organized around:

- page-level route composition
- reusable chart and layout primitives
- React Query hooks for REST reads
- a dedicated live stream hook for dashboard updates
- shared domain types mirroring backend payloads

## Runtime topology

```mermaid
flowchart LR
    subgraph Browser
        UI[React + Vite]
        Cache[React Query Cache]
    end

    subgraph API
        Flask[Flask App Factory]
        REST[RESTX Namespaces]
        WS[Flask-Sock Route]
        Services[Service Layer]
        Broker[EventStreamBroker]
    end

    subgraph Data
        PG[(PostgreSQL 16)]
    end

    UI --> REST
    REST --> Services
    Services --> PG
    Services --> Broker
    Broker --> WS
    WS --> Cache
    Cache --> UI
```
