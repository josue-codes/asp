# Entities

## List

- User
- Album
- Photo
- Tag
- Contract

### User

- First Name
- Last Name
- Email
- Role
  - Admin
  - Client
  - Prospect

### Album

- Name
- Access Token

### Photo

- Name
- Content
- URL
- Portfolio?

### Tag

- Name

### Contract

- User
- Rate
- Date Services to be Rendered
- Services to be Rendered
- Duration of Services
- Location of Services

## Entity Relationships

- Album
  - User

- Photo
  - Album
  - Tag: list[Tag]
  