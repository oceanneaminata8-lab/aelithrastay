# AelithraStay Admin System - Architecture & Feature Map

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AELITHRASTAY ADMIN PORTAL                     │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────┐
│   ADMIN LOGIN    │         │   USER TYPES     │
│                  │         │                  │
│ /admin-login     │────────▶│ • Guest          │
│                  │         │ • Host           │
│ Email/Password   │         │ • Admin ✓        │
│ Remember Device  │         │                  │
└──────────────────┘         └──────────────────┘
         │
         │
         ▼
┌──────────────────────────────────────────────────────────────────┐
│              ADMIN DASHBOARD (/admin)                             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  SIDEBAR NAVIGATION                                     │   │
│  │  • Dashboard            • Notifications                 │   │
│  │  • Properties           • Analytics                     │   │
│  │  • Property Approval    • Locations                     │   │
│  │  • Reservations                                         │   │
│  │  • Disputes             (Add New Listing)              │   │
│  │  • Review Moderation                                    │   │
│  │  • User Management                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  MAIN CONTENT AREA - Different Panels                   │   │
│  │                                                         │   │
│  │  • Dashboard: Key metrics & quick stats                │   │
│  │  • Users: Manage roles, suspend, activate              │   │
│  │  • Properties: View, delete, search                    │   │
│  │  • Property Approval: Approve/reject pending           │   │
│  │  • Reservations: View, filter, cancel bookings         │   │
│  │  • Disputes: Mark reviewing, resolve with notes        │   │
│  │  • Reviews: Hide, approve, moderate                    │   │
│  │  • Notifications: Send broadcasts                      │   │
│  │  • Analytics: Revenue, refunds, progress               │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

## Feature Flow Diagrams

### 1. User Management Flow
```
┌─────────────┐
│  All Users  │
└──────┬──────┘
       │
       ├─────────────────┬──────────────┬──────────────┐
       │                 │              │              │
       ▼                 ▼              ▼              ▼
   [Change Role]   [Suspend]      [Activate]     [Delete]
       │                │              │              │
       ├─guest         User blocked   Reactivate     │
       ├─host         from platform   account        │
       └─admin                                        │
            │                                        │
            └────────────────────────────────────────┤
                                                     ▼
                                              AdminLog Entry
```

### 2. Property Approval Flow
```
┌──────────────────┐
│  Host Creates    │
│  Property        │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│ Status: PENDING      │
│ (Not visible public) │
└────────┬─────────────┘
         │
    ┌────┴────┐
    │          │
    ▼          ▼
┌────────┐ ┌────────┐
│ Approve│ │ Reject │
└───┬────┘ └────┬───┘
    │           │
    ▼           ▼
┌───────────┐ ┌──────────┐
│ APPROVED  │ │ REJECTED │
│ (Visible) │ │ (Deleted)│
└───────────┘ └──────────┘
```

### 3. Dispute Resolution Flow
```
┌─────────────────┐
│ Guest/Host      │
│ Opens Dispute   │
└────────┬────────┘
         │
         ▼
┌──────────────────┐
│ Status: OPEN     │
│ (Under review)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│ Admin Reviews        │
│ Mark "Reviewing"     │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ Admin Resolves       │
│ + Settlement Notes   │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ Status: RESOLVED     │
│ Both parties notify  │
└──────────────────────┘
```

### 4. Review Moderation Flow
```
┌─────────────────┐
│ Guest Reviews   │
│ Property        │
└────────┬────────┘
         │
    ┌────┴─────────────┐
    │                  │
    ▼                  ▼
┌────────────┐   ┌─────────────┐
│ CLEAN      │   │ REPORTED    │
│ (Visible)  │   │ (Flagged)   │
└────────────┘   └──────┬──────┘
                        │
                   ┌────┴────┐
                   │          │
                   ▼          ▼
              ┌────────┐  ┌─────────┐
              │ HIDE   │  │ RESOLVE │
              │(Remove)│  │(Approve)│
              └────────┘  └─────────┘
```

### 5. Notification System Flow
```
┌──────────────────┐
│  Admin Panel     │
│  Notifications   │
└────────┬─────────┘
         │
    ┌────┼────────────┐
    │    │            │
    ▼    ▼            ▼
┌────┐ ┌──────┐ ┌─────────┐
│All │ │ Role │ │Specific │
│    │ │      │ │ User    │
└─┬──┘ └──┬───┘ └────┬────┘
  │       │          │
  ▼       ▼          ▼
Send to all    Send to    Send to
users          guests/    one user
               hosts/
               admins
               │
               ▼
         Notification
         Stored + Sent
```

## Data Flow - Backend

```
┌──────────────────────────────────────────────────────────────┐
│                    DJANGO BACKEND                             │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐                                            │
│  │  Django      │                                            │
│  │  Models      │                                            │
│  ├──────────────┤                                            │
│  │ • User       │                                            │
│  │ • Property   │                                            │
│  │ • Booking    │                                            │
│  │ • Review     │                                            │
│  │ • Payment    │                                            │
│  │ • AdminLog   │                                            │
│  │ • Notif'n    │                                            │
│  └──────┬───────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────┐                           │
│  │  Admin ViewSets & Endpoints  │                           │
│  ├──────────────────────────────┤                           │
│  │ • admin_views.py (accounts)  │                           │
│  │ • admin_views.py (bookings)  │                           │
│  │ • admin_views.py (reviews)   │                           │
│  │ • admin_views.py (properties)│                           │
│  │ • admin_views.py (payments)  │                           │
│  │ • admin_views.py (notif)     │                           │
│  └──────┬───────────────────────┘                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────┐                           │
│  │  Admin Routes (/api/admin/)  │                           │
│  ├──────────────────────────────┤                           │
│  │ /users/                      │                           │
│  │ /disputes/                   │                           │
│  │ /reviews/                    │                           │
│  │ /properties/                 │                           │
│  │ /payments/                   │                           │
│  │ /notifications/              │                           │
│  │ /logs/                       │                           │
│  └──────┬───────────────────────┘                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────┐                           │
│  │  Permission Checks           │                           │
│  │  (IsAuthenticated + IsAdmin) │                           │
│  └──────┬───────────────────────┘                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────┐                           │
│  │  Response with Data          │                           │
│  │  or Action Confirmation      │                           │
│  └──────────────────────────────┘                           │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow - Frontend

```
┌──────────────────────────────────────────────────────────────┐
│                ANGULAR FRONTEND                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────┐                          │
│  │  Admin Login Page              │                          │
│  │  (/admin-login)                │                          │
│  │                                │                          │
│  │  Email: [_________]            │                          │
│  │  Password: [_______]           │                          │
│  │  [Enter Admin Panel]           │                          │
│  └────────┬───────────────────────┘                          │
│           │                                                  │
│           ▼                                                  │
│  ┌────────────────────────────────┐                          │
│  │  Authentication                │                          │
│  │  admin.service.login()         │                          │
│  └────────┬───────────────────────┘                          │
│           │                                                  │
│     ┌─────┴──────┐                                            │
│     │            │                                            │
│  Success      Failure                                         │
│     │            │                                            │
│     ▼            ▼                                            │
│  Navigate    Show Error                                       │
│  to /admin   Message                                          │
│     │                                                        │
│     ▼                                                        │
│  ┌────────────────────────────────┐                          │
│  │  Admin Dashboard               │                          │
│  │  (/admin)                      │                          │
│  │                                │                          │
│  │  [Sidebar] | [Main Content]    │                          │
│  └────────┬───────────────────────┘                          │
│           │                                                  │
│      ┌────┴──────────────┐                                    │
│      │                   │                                    │
│      ▼                   ▼                                    │
│   User Action        Load Data                                │
│   (button click)     (admin.service)                           │
│      │                   │                                    │
│      ├─────────┬─────────┤                                    │
│      │         │         │                                    │
│      ▼         ▼         ▼                                    │
│   Approve   Suspend   GetStats                                │
│   Property   User     Review Data                             │
│      │         │         │                                    │
│      └─────────┼─────────┘                                    │
│              │                                               │
│              ▼                                               │
│   ┌──────────────────────────────┐                           │
│   │  AdminService Method Call    │                           │
│   │  .approveProperty(id)        │                           │
│   │  .suspendUser(id)            │                           │
│   │  etc.                        │                           │
│   └──────────┬───────────────────┘                           │
│              │                                               │
│              ▼                                               │
│   ┌──────────────────────────────┐                           │
│   │  HTTP Request to API         │                           │
│   │  POST /api/admin/properties  │                           │
│   │  POST /api/admin/users       │                           │
│   │  GET /api/admin/reviews      │                           │
│   │  etc.                        │                           │
│   └──────────┬───────────────────┘                           │
│              │                                               │
│              ▼                                               │
│   ┌──────────────────────────────┐                           │
│   │  Handle Response             │                           │
│   │  Update Signals              │                           │
│   │  Show Toast Message          │                           │
│   │  Refresh Panel               │                           │
│   └──────────────────────────────┘                           │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Permission Matrix

```
┌─────────────────────┬─────────┬──────────┬─────────────┐
│ Action              │ Guest   │ Host     │ Admin       │
├─────────────────────┼─────────┼──────────┼─────────────┤
│ Access Admin Panel  │    ✗    │    ✗     │      ✓      │
│ Approve Properties  │    ✗    │    ✗     │      ✓      │
│ Reject Properties   │    ✗    │    ✗     │      ✓      │
│ Resolve Disputes    │    ✗    │    ✗     │      ✓      │
│ Moderate Reviews    │    ✗    │    ✗     │      ✓      │
│ Suspend Users       │    ✗    │    ✗     │      ✓      │
│ Activate Users      │    ✗    │    ✗     │      ✓      │
│ Change User Role    │    ✗    │    ✗     │      ✓      │
│ Send Notifications  │    ✗    │    ✗     │      ✓      │
│ Process Refunds     │    ✗    │    ✗     │      ✓      │
│ View Admin Logs     │    ✗    │    ✗     │      ✓      │
│ Create Property     │    ✗    │    ✓     │      ✓      │
│ View Own Reviews    │    ✓    │    ✓     │      ✓      │
│ View Bookings       │    ✓    │    ✓     │      ✓      │
└─────────────────────┴─────────┴──────────┴─────────────┘
```

## Audit Log Actions Tracked

```
┌─────────────────────────────────────────────────────────┐
│            ADMIN ACTIONS LOGGED                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  USER MANAGEMENT:                                      │
│  • user_suspended          → Timestamp, username       │
│  • user_activated          → Timestamp, username       │
│  • user_role_changed       → Old role, New role        │
│                                                         │
│  PROPERTY MANAGEMENT:                                  │
│  • property_approved       → Title, notes              │
│  • property_rejected       → Title, reason             │
│  • property_reported       → Title, report reason      │
│  • property_reported_resolved → Title, resolution      │
│                                                         │
│  DISPUTE MANAGEMENT:                                   │
│  • dispute_opened          → Booking ID                │
│  • dispute_reviewing       → Booking ID                │
│  • dispute_resolved        → Resolution notes          │
│                                                         │
│  REVIEW MANAGEMENT:                                    │
│  • review_hidden           → Reason                    │
│  • review_reported         → Timestamp                 │
│  • review_resolved         → Resolution                │
│                                                         │
│  PAYMENT MANAGEMENT:                                   │
│  • payment_refunded        → Amount, reason            │
│                                                         │
│  All entries include:                                  │
│  • Admin username who performed action                 │
│  • Exact timestamp                                     │
│  • Detailed action parameters                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Integration Points

```
┌───────────────────────────────────────────────────────────────┐
│              SYSTEM INTEGRATION MAP                            │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Django     │  │  PostgreSQL  │  │  JWT Auth   │       │
│  │   Backend    │─▶│  Database    │  │  Tokens     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────────┐                       │
│  │  REST API Endpoints              │                       │
│  │  /api/admin/*                    │                       │
│  └──────────────────────────────────┘                       │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────────┐                       │
│  │  CORS Configuration              │                       │
│  │  Allows Angular Frontend          │                       │
│  └──────────────────────────────────┘                       │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────────┐                       │
│  │  Angular Frontend                │                       │
│  │  Admin Service + Components      │                       │
│  └──────────────────────────────────┘                       │
│                                                               │
│  Real-time updates via:                                     │
│  • HTTP Signals (Angular)                                   │
│  • WebSocket (optional future)                              │
│  • Email Notifications (optional)                           │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Response Format Examples

### Success Response
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "role": "guest",
  "is_suspended": false,
  "date_joined": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
  "error": "Invalid admin email or password.",
  "status": 401
}
```

### List Response
```json
[
  {
    "id": 1,
    "guest_name": "John Doe",
    "property_title": "Beautiful Beach House",
    "dispute_status": "open",
    "dispute_reason": "Damage to property",
    "created_at": "2024-06-04T14:20:00Z"
  },
  {
    "id": 2,
    "guest_name": "Jane Smith",
    "property_title": "Mountain Cabin",
    "dispute_status": "reviewing",
    "dispute_reason": "Missing items",
    "created_at": "2024-06-03T09:15:00Z"
  }
]
```

---

**Architecture Complete** ✓  
**All systems integrated and functional**
