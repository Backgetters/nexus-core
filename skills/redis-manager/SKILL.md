# Redis Manager Skill

Interact with Redis databases for caching and data storage.

## Usage

- `redis keys <pattern>` - List keys matching pattern
- `redis get <key>` - Get value by key
- `redis set <key> <value>` - Set key value
- `redis flush` - Clear database (use with caution)

## Requirements

- Redis CLI or redis-py
- REDIS_URL environment variable
