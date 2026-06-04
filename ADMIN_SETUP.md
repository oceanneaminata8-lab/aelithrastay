# AelithraStay Admin Portal - Complete Implementation Guide

## Overview
A comprehensive admin interface has been implemented with dedicated authentication, user management, property moderation, dispute resolution, and revenue tracking capabilities.

## Backend Implementation

### 1. New Models
- **AdminLog**: Tracks all admin actions with detailed audit trail
  - Stores action type, object type, object ID, and additional details
  - Helps maintain accountability and provides audit history

### 2. New API Endpoints

#### User Management (`/api/admin/users/`)
- `GET /api/admin/users/` - List all users
- `POST /api/admin/users/{id}/suspend/` - Suspend a user account
- `POST /api/admin/users/{id}/activate/` - Reactivate a suspended user
- `POST /api/admin/users/{id}/change_role/` - Change user role (guest/host/admin)

#### Dispute Management (`/api/admin/disputes/`)
- `GET /api/admin/disputes/` - List booking disputes
- `POST /api/admin/disputes/{id}/mark_reviewing/` - Mark dispute as under review
- `POST /api/admin/disputes/{id}/resolve/` - Resolve a dispute with resolution notes
- `GET /api/admin/disputes/statistics/` - Get dispute statistics

#### Review Moderation (`/api/admin/reviews/`)
- `GET /api/admin/reviews/` - List reviews for moderation
- `POST /api/admin/reviews/{id}/hide/` - Hide a review from public view
- `POST /api/admin/reviews/{id}/mark_reported/` - Mark review as reported
- `POST /api/admin/reviews/{id}/resolve/` - Resolve a reported review
- `GET /api/admin/reviews/statistics/` - Get moderation statistics

#### Property Approval (`/api/admin/properties/`)
- `GET /api/admin/properties/` - List properties for approval (filter by status)
- `POST /api/admin/properties/{id}/approve/` - Approve a property listing
- `POST /api/admin/properties/{id}/reject/` - Reject a property listing
- `POST /api/admin/properties/{id}/mark_reported/` - Report a property
- `POST /api/admin/properties/{id}/resolve_report/` - Resolve a property report
- `GET /api/admin/properties/statistics/` - Get property moderation stats

#### Payment Management (`/api/admin/payments/`)
- `GET /api/admin/payments/` - List all payments (filter by status)
- `POST /api/admin/payments/{id}/refund/` - Process payment refund
- `GET /api/admin/payments/statistics/` - Get payment and revenue statistics

#### Admin Notifications (`/api/admin/notifications/`)
- `POST /api/admin/notifications/broadcast/` - Send notification to all users
- `POST /api/admin/notifications/send_to_role/` - Send to specific user role
- `POST /api/admin/notifications/send_to_user/` - Send to specific user
- `GET /api/admin/notifications/admin_notifications/` - Get system notifications

#### Admin Activity Logs (`/api/admin/logs/`)
- `GET /api/admin/logs/` - List all admin actions (filter by action/object type)

### 3. Database Setup

Before starting the application, run migrations to create the AdminLog table:

```bash
# Navigate to backend directory
cd backend

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 4. Create Admin User

Run the following command to create an admin user:

```bash
python manage.py createsuperuser
```

Or if you have a script:

```bash
python manage.py shell
```

Then:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.create_user(
    username='admin@aelithrastay.com',
    email='admin@aelithrastay.com',
    password='your_secure_password',
    role='admin',
    is_staff=True,
    is_superuser=True
)
```

## Frontend Implementation

### 1. Admin Login Page
- **URL**: `/admin-login`
- **Features**:
  - Email and password authentication
  - "Remember this device" option
  - Role verification (must have admin role)
  - Separate from regular user login

### 2. Admin Dashboard (`/admin`)
Protected by `adminGuard` - only accessible to users with admin role.

#### Main Panels

**Dashboard**
- Quick overview of key metrics
- Recent reservations
- Quick action buttons

**User Management**
- View all users with their roles and status
- Suspend/activate user accounts
- Change user roles (guest ↔ host ↔ admin)
- Delete users
- Search and filter users

**Property Listings**
- View and search all properties
- Delete properties
- Filter by location, type, price

**Property Approval**
- Queue of properties awaiting approval
- Approve properties (with optional notes)
- Reject properties (with reason)
- View approval status

**Reservations**
- View all bookings
- Cancel bookings
- Filter by status, dates, price

**Booking Disputes**
- View all open and reviewing disputes
- Mark disputes as under review
- Resolve disputes with resolution details
- View dispute history and statistics

**Review Moderation**
- List reviews flagged for moderation
- Hide inappropriate reviews (with reason)
- Approve reviews
- View moderation statistics

**Admin Notifications**
- Send broadcasts to all users
- Send targeted messages to specific roles
- View notification history

**Analytics**
- Revenue tracking and performance metrics
- Monthly goal progress
- Revenue breakdown by payment method
- Refund statistics

**Locations**
- Global platform presence
- Active listings by country
- Quick filter to properties by location

### 3. Admin Service (`admin.service.ts`)

Provides TypeScript methods for all admin operations:

```typescript
// User Management
adminService.getAdminUsers()
adminService.suspendUser(userId)
adminService.activateUser(userId)
adminService.changeUserRole(userId, role)

// Disputes
adminService.getDisputes(status)
adminService.markDisputeReviewing(disputeId)
adminService.resolveDispute(disputeId, resolution)

// Reviews
adminService.getReviewsForModeration(status)
adminService.hideReview(reviewId, note)
adminService.resolveReviewReport(reviewId, resolution)

// Properties
adminService.getPropertiesForApproval(status)
adminService.approveProperty(propertyId, note)
adminService.rejectProperty(propertyId, reason)
adminService.markPropertyReported(propertyId, reason)

// Payments
adminService.getPaymentStats()
adminService.processRefund(paymentId, reason)

// Notifications
adminService.sendNotificationToAll(title, message)
adminService.sendNotificationToRole(title, message, role)
adminService.sendNotificationToUser(userId, title, message)

// Logs
adminService.getAdminLogs(actionType, objectType)
```

## Security Features

1. **Role-Based Access Control**
   - Only users with `role='admin'` can access admin panel
   - Admin routes protected by `adminGuard`
   - Separate authentication endpoint for admin login

2. **Audit Trail**
   - All admin actions logged in `AdminLog` model
   - Tracks who performed what action and when
   - Includes action details for accountability

3. **Permission Checks**
   - `IsAdmin` permission class on all admin endpoints
   - Checks both `is_staff` and `role == 'admin'`
   - Prevents unauthorized access

4. **User Suspension**
   - Suspended users cannot log in
   - Checked during authentication
   - Admin can suspend/activate accounts

## Key Features Implemented

### ✅ User Management with Suspend/Activate
- View all users with detailed information
- Suspend accounts to block access
- Reactivate suspended accounts
- Change user roles and permissions
- Delete user accounts

### ✅ Property Approval Before Publishing
- Queue system for pending properties
- Admin approval/rejection workflow
- Approval notes for documentation
- Status tracking and filtering

### ✅ Reported Reviews/Properties Moderation
- Flag inappropriate reviews
- Hide reviews from public view
- Track moderation notes
- Mark properties as reported
- Resolve reports with notes

### ✅ Platform Revenue Dashboard
- Total revenue tracking
- Revenue breakdown by payment method
- Refund tracking and statistics
- Monthly goal progress visualization
- Payment status filtering

### ✅ Booking Dispute Management
- View all disputes with details
- Mark disputes as under review
- Resolve disputes with settlement details
- Dispute statistics and tracking
- Status filtering

### ✅ Admin Notifications Center
- Send broadcasts to all users
- Send targeted notifications by user role
- Send notifications to specific users
- Notification history tracking

## Usage Workflow

### For Property Approval

1. Go to Admin → Property Approval
2. Review pending properties in queue
3. Click approve/reject button
4. Add approval notes (optional) or rejection reason
5. Property status updated and host notified

### For Dispute Resolution

1. Go to Admin → Booking Disputes
2. Click on dispute to view details
3. Mark as "Under Review" to indicate handling
4. Click resolve and enter settlement details
5. Both parties notified of resolution

### For Review Moderation

1. Go to Admin → Review Moderation
2. Review flagged reviews
3. Approve (remains public) or Hide (removed from view)
4. Add moderation notes if hiding
5. Update statistics tracked

### For User Management

1. Go to Admin → User Management
2. Search/filter users as needed
3. Click action buttons to:
   - Change role
   - Suspend/activate account
   - Delete account
4. All changes logged automatically

## Troubleshooting

### Admin Login Not Working
- Ensure user has `role = 'admin'` in database
- Check that `is_staff = True`
- Verify credentials are correct

### Property Approval Not Loading
- Run migrations: `python manage.py migrate`
- Check that properties exist with `approval_status = 'pending'`

### Statistics Not Showing
- Endpoints require admin role
- Check browser console for API errors
- Verify all bookings have `total_price` set

### Notifications Not Sending
- Check that users exist in database
- Verify notification endpoint is accessible
- Check network tab in browser dev tools

## Future Enhancements

Potential additions:
- Bulk actions for multiple items
- Advanced search and filtering
- Email notification templates
- Admin role levels (super-admin, moderator, etc.)
- Two-factor authentication for admin login
- Content flagging and automated moderation
- Appeal system for users
- Advanced analytics with charts
- CSV export for all data types
- Admin activity email alerts
