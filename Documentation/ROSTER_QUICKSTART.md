# Duty Roster Feature - Quick Start

## Installation

The duty roster feature has been automatically installed and integrated into your Media Unit Management application.

### What Was Added

1. **Database Models**
   - `RosterTemplate` - Stores admin-configured parameters
   - `DutyRoster` - Individual duty assignments

2. **Routes**
   - Admin routes for template and roster management
   - Public routes for member roster viewing
   - CSV export functionality

3. **Templates**
   - Roster dashboard
   - Template management interface
   - Generation wizard
   - Roster viewing and confirmation

4. **Integration**
   - Added "Duty Rosters" link to admin dashboard
   - Integrated with existing member and subunit data

## Getting Started (5 Minutes)

### Step 1: Access Roster Management
1. Log in as admin
2. Go to Admin Dashboard
3. Click "Duty Rosters" card

### Step 2: Create Your First Template
1. Click "Create Template"
2. Fill in:
   - **Name**: "Sunday Worship Service"
   - **Days**: Check "Sunday"
   - **Start Date**: Today's date
   - **Start Time**: 09:00
   - **End Time**: 11:00
   - **Roles**: "Lead Singer, Bass Guitar, Drummer, Sound Tech"
   - **Members Per Slot**: 1
   - **Subunits**: Select your available subunits
3. Click "Create Template"

### Step 3: Generate Rosters
1. Go to Templates
2. Click "Generate" on your template
3. Set date range (e.g., next 3 months)
4. Click "Generate Rosters"
5. System creates assignments automatically

### Step 4: View & Manage
1. Click "View All Rosters"
2. See all generated assignments
3. Confirm duties or make adjustments as needed
4. Click "Manage Templates" to modify anytime

## Key Concepts

### Templates
Think of templates like **recurring appointment templates**. They contain:
- Who should work (subunits)
- What they should do (roles)
- When (days, times, date range)
- How many (members per slot)

### Generation
**Automatic assignment** using a round-robin algorithm:
- Takes eligible members from selected subunits
- Assigns them to roles fairly
- Creates entries for all selected days
- Can regenerate anytime (old entries replaced)

### Status Tracking
Each roster entry progresses:
- **Assigned** (new) → Member needs to confirm
- **Confirmed** (ready) → Member acknowledged
- **Completed** (done) → Duty finished
- **Cancelled** (not happening)

## Common Tasks

### Edit a Template
1. Go to Templates
2. Click "Edit" on the template
3. Modify parameters
4. Click "Update"

### Add More Roles to a Template
1. Edit template
2. Modify "Roles" field (add comma-separated roles)
3. Save and regenerate rosters

### Remove Someone from a Duty
1. Go to View Rosters
2. Find the roster entry
3. Click "Delete" button

### Export Rosters to Excel
1. Go to Templates
2. Click "Export" on the template
3. Save CSV file
4. Open in Excel/Google Sheets

### Check Member Availability
1. Go to View Rosters
2. Search by member name
3. See all their assigned duties

## Customization Tips

### For Different Event Types
Create separate templates for:
- Worship services
- Prayer meetings
- Training sessions
- Administrative duties
- Special events

### Seasonal Planning
- Create templates with end dates for seasons
- Disable templates in off-season
- Create new templates as seasons change

### Fair Distribution
- Set appropriate member pool (subunits)
- Adjust "members per slot" based on role
- Use export data to manually audit

## Integration with Existing System

The roster system integrates with:
- **Members**: Uses approved/completed members from applications
- **Subunits**: Filters members by subunit assignment
- **Admin Dashboard**: Quick access from dashboard
- **File System**: Exports to CSV files

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| No rosters generate | Check if template has selected subunits with eligible members |
| Same member in multiple slots | Check template's "members per slot" - should be 1 for soloists |
| Members can't see rosters | Direct them to `/roster/view` or check if logged in |
| Old rosters still showing | Enable "Clear existing rosters" option before regenerating |

## Next Steps

1. **Create your first template** (5 minutes)
2. **Generate a test roster** (2 minutes)
3. **Share with team** - Members can view at `/roster/view`
4. **Review and adjust** - Modify template based on results
5. **Go live** - Set up regular schedule

## File Structure

```
app/
  models.py              # RosterTemplate, DutyRoster models
  routes.py              # roster_bp with all routes
  templates/roster/
    dashboard.html       # Main roster dashboard
    templates.html       # Template list & management
    template_form.html   # Create/edit form
    generate.html        # Generate rosters form
    view.html           # View rosters & confirmation
```

## API Endpoints Quick Reference

### Admin Only
- `POST /roster/template/create` - Create new template
- `POST /roster/template/<id>/edit` - Edit template
- `POST /roster/template/<id>/delete` - Delete template
- `POST /roster/generate/<id>` - Generate rosters
- `POST /roster/<id>/update` - Update roster
- `POST /roster/<id>/delete` - Delete roster
- `GET /roster/export/<id>` - Export to CSV

### Public/Members
- `GET /roster/view` - View assigned rosters
- `POST /roster/<id>/confirm` - Confirm availability

## Support Resources

- **ROSTER_GUIDE.md** - Complete feature documentation
- **DATABASE.md** - Database schema details
- **API.md** - API documentation
- **Admin Dashboard** - Help links and documentation

---

**Ready to start?** Log in as admin and click "Duty Rosters" to begin!
