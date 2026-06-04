# AelithraStay Admin Portal - Quick Start Guide

## Login

1. Navigate to **http://localhost:4200/admin-login** (or your production URL)
2. Enter your admin email
3. Enter your admin password  
4. Click "Enter Admin Panel"
5. You'll be redirected to the dashboard

## Dashboard Overview

The admin dashboard contains these main sections:

### Left Sidebar
Quick navigation to all admin functions:
- **Dashboard** - Overview and key metrics
- **Property Listings** - All properties on platform
- **Property Approval** - Queue of pending properties
- **Reservations** - All bookings
- **Disputes** - Booking disputes  
- **Review Moderation** - Flag reviews
- **User Management** - Manage user accounts
- **Notifications** - Send messages
- **Analytics** - Revenue & performance

### Top Header
- **Search Bar** - Search across current panel
- **Export** - Export data as CSV
- **Add Listing** - Create new property

### Key Metrics (Dashboard)
Shows at-a-glance stats:
- Total Users
- Active Listings
- Current Reservations  
- Platform Revenue

## Key Tasks

### 📋 Approve a New Property

1. Click **Property Approval** in sidebar
2. Review pending properties in table
3. For each property:
   - Read title, type, price
   - Click **Approve** (with optional notes) → property goes live
   - Click **Reject** → property deleted (host notified)

### 👥 Manage User Accounts

1. Click **User Management** in sidebar
2. View all users in table
3. For each user:
   - **Promote** - Click person icon to promote guest→host
   - **Make Admin** - Click verified icon  
   - **Suspend** - Click block icon (blocks account)
   - **Activate** - Click check icon (reactivates suspended account)
   - **Delete** - Click trash icon

### 🔴 Resolve Booking Disputes

1. Click **Disputes** in sidebar
2. View open disputes in table
3. For each dispute:
   - Click **Under Review** when starting to handle
   - Click **Resolve** and enter settlement notes
4. Both parties notified automatically

### ⭐ Moderate Reviews

1. Click **Review Moderation** in sidebar
2. View flagged reviews in table
3. For each review:
   - Click **Approve** (stays public)
   - Click **Hide** (removed from public, add reason)
4. Moderation tracked automatically

### 💰 Track Revenue & Refunds

1. Click **Analytics** in sidebar
2. View total revenue earned
3. See refund statistics
4. Check monthly goal progress
5. Export report as CSV for records

### 📢 Send Notifications

1. Click **Notifications** in sidebar
2. Click **Send Broadcast** button
3. Enter notification title
4. Enter message content
5. Click Send - goes to all/selected users

### 🔍 Search & Filter

In any panel:
- Use search bar to find items
- Type property name, user name, email, etc.
- Results update in real-time
- Click **Clear Filters** to reset

### 📊 Export Data

1. Click **Export** button in top right
2. Data downloads as CSV file
3. Open in Excel/Sheets for further analysis

## Common Workflows

### Approving Multiple Properties

```
1. Property Approval → Pending queue shown
2. Read each property details
3. Approve/Reject in order
4. Hosts notified of decision
5. Approved properties go live
```

### Resolving a Dispute

```
1. Disputes → See open disputes
2. Click "Under Review" 
3. Read both sides of dispute
4. Click "Resolve"
5. Type settlement/outcome
6. Both parties receive notification
7. Dispute marked complete
```

### Handling Inappropriate Review

```
1. Review Moderation → See flagged reviews
2. Read review content
3. If inappropriate: Click Hide + Add reason
4. Review removed from public
5. Guest notified of removal
6. Stats updated
```

### Suspending Misbehaving User

```
1. User Management → Find user
2. Click block icon to suspend
3. User immediately cannot access platform
4. User notified of suspension
5. Later: Click check icon to reactivate
```

## Tips & Tricks

✨ **Pro Tips:**
- Use search to quickly find items
- Check suspension status of problematic users
- Review admin logs to see history
- Export reports regularly for records
- Use moderation notes for documentation
- Create detailed dispute resolutions for records
- Approve properties promptly to help hosts go live

⚠️ **Be Careful:**
- Deleting users cannot be undone
- Rejecting properties notifies hosts
- Suspending users is permanent until reactivated
- Export reports before they get too old
- Double-check before major actions

## Keyboard Shortcuts

- `S` - Search (focus search box)
- `E` - Export
- `/` - Go to home

## Troubleshooting

**"Access Denied"**
- Check you're logged in as admin
- Verify admin role in user database
- Clear browser cache and try again

**Data Not Loading**
- Refresh the page
- Check internet connection  
- Try different browser
- Check browser console for errors

**Can't Suspend User**
- Make sure user exists
- Try refreshing first
- Check user isn't already suspended

**Notifications Not Sending**
- Verify user emails are correct
- Check title/message aren't empty
- Try sending to smaller group first

## Contact Information

Need help?
- Check the full [ADMIN_SETUP.md](ADMIN_SETUP.md) guide
- Review [ADMIN_IMPLEMENTATION_CHECKLIST.md](ADMIN_IMPLEMENTATION_CHECKLIST.md)
- Check Django admin panel: http://localhost:8000/admin
- Enable debug mode to see error details

## Safety Checklist

Before going live:
- [ ] Test all moderation features
- [ ] Verify suspension works  
- [ ] Test notifications send
- [ ] Check property approval flow
- [ ] Verify dispute resolution
- [ ] Export test report
- [ ] Change default admin password
- [ ] Review admin logs regularly

## Key Statistics to Monitor

Daily checks:
- New properties awaiting approval
- Pending disputes
- Flagged reviews
- Reported properties
- Revenue trends
- User activity

Monthly checks:
- Total revenue vs goals
- Refund rates
- User growth
- Dispute resolution time
- Moderation stats

---

**Version:** 1.0  
**Last Updated:** June 2024  
**Contact:** admin@aelithrastay.com
