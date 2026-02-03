# Duty Roster Manager - Complete Guide

## Overview

The Duty Roster Manager is an advanced scheduling system that allows administrators to create templates with configurable parameters and automatically generate duty assignments for members based on those parameters. Members can then view their assignments and confirm their availability.

## Features

### 1. Roster Templates
Administrators can create reusable roster templates with the following parameters:
- **Template Name & Description**: Descriptive names for different rosters (e.g., "Sunday Morning Worship", "Mid-Week Practice")
- **Days of Week**: Select which days the roster should repeat (Mon-Sun)
- **Time Slots**: Configure start and end times for each duty
- **Roles**: Specify different roles to be assigned (e.g., Lead Singer, Drummer, Sound Tech)
- **Subunits**: Choose which subunits members can be assigned from
- **Members Per Slot**: How many members should be assigned to each role per time slot
- **Active Period**: Set a date range for when the template is active

### 2. Automatic Roster Generation
Once a template is created, administrators can:
- Generate rosters for a specific date range
- The system automatically assigns eligible members using a round-robin algorithm
- Members are selected from the specified subunits
- Assignments are distributed fairly across eligible members
- Generate multiple rosters at once in bulk

### 3. Roster Management
Administrators can:
- View all generated rosters
- Filter rosters by date and subunit
- Update individual assignments
- Track duty status (assigned → confirmed → completed/cancelled)
- Delete or reassign duties
- Export rosters to CSV format

### 4. Member Confirmation
Members can:
- View their assigned duties
- Confirm their availability for assigned duties
- See roster details (date, time, role, subunit)
- Track their duty history

## User Interface

### Admin Dashboard
The admin dashboard includes:
- **Duty Rosters Card**: Quick access to roster management
- Links to create templates, generate rosters, and view all assignments
- Overview of assigned vs. confirmed duties

### Roster Management Pages

#### 1. Dashboard (`/roster/`)
Main control center with:
- Quick statistics (active templates, assigned duties, confirmed duties)
- Recent duty assignments
- Quick access buttons
- Active templates overview

#### 2. Templates Page (`/roster/templates`)
- List all roster templates
- Show template details (days, times, roles, schedule)
- Edit existing templates
- Delete templates
- Generate new rosters from templates

#### 3. Create/Edit Template (`/roster/template/create`, `/roster/template/<id>/edit`)
Form to configure:
- Template name and description
- Days of week selection (checkboxes)
- Date range (start date, optional end date)
- Time slot (start time, end time)
- Roles (comma-separated list)
- Members per slot (number input)
- Subunits selection (checkboxes)

#### 4. Generate Roster (`/roster/generate/<template_id>`)
Form to:
- Select date range for generation
- Options to clear existing rosters
- Notify members (when email enabled)
- Progress indicator during generation
- Success confirmation with count

#### 5. View Rosters (`/roster/view`)
- List all rosters with filtering
- Filter by date range and subunit
- Show statistics (assigned, confirmed, completed, cancelled)
- Action buttons (confirm, delete)
- Pagination for large result sets

## API Routes

### Admin Routes

**Dashboard & Templates**
- `GET /roster/` - View roster dashboard
- `GET /roster/templates` - List all templates
- `GET /roster/template/create` - Create template form
- `POST /roster/template/create` - Save new template
- `GET /roster/template/<id>/edit` - Edit template form
- `POST /roster/template/<id>/edit` - Update template
- `POST /roster/template/<id>/delete` - Delete template

**Roster Generation & Management**
- `GET /roster/generate/<template_id>` - Generate roster form
- `POST /roster/generate/<template_id>` - Execute roster generation
- `POST /roster/<id>/update` - Update roster entry (admin)
- `POST /roster/<id>/delete` - Delete roster entry (admin)
- `GET /roster/export/<template_id>` - Export roster to CSV

### Public Routes

**Member Access**
- `GET /roster/view` - View assigned rosters
- `POST /roster/<id>/confirm` - Confirm duty assignment

## How to Use

### Creating a Roster Template

1. Navigate to Admin Dashboard → Duty Rosters
2. Click "Create Template"
3. Fill in the form:
   - Enter a descriptive name (e.g., "Sunday Choir")
   - Add optional description
   - Select days of week (e.g., Sunday)
   - Set time range (e.g., 09:00-11:00)
   - Add roles needed (e.g., "Lead Singer, Bass, Alto, Soprano")
   - Set members per slot (usually 1 for soloists, higher for groups)
   - Select subunits to draw members from
   - Set active date range
4. Click "Create Template"

### Generating Rosters

1. From Templates page, click "Generate" on a template
2. Adjust date range if needed
3. Choose options (clear existing, notify members)
4. Click "Generate Rosters"
5. System will create roster entries for all selected days

**Example**: Template set for "Every Sunday" with start date "2024-01-01" and end date "2024-03-31" will generate rosters for all Sundays in that period.

### Managing Rosters

1. Go to "View All Rosters"
2. Use filters to find specific rosters (by date, subunit)
3. See statistics showing assignment status
4. Click action buttons to:
   - **Confirm**: Mark duty as confirmed by member
   - **Delete**: Remove duty entry
5. Click "Edit" to reassign or change details

### Exporting Data

1. From Templates page, click "Export" button
2. System generates CSV file with all roster entries for that template
3. Download and open in Excel/Google Sheets for reporting

## Status Workflow

Rosters have the following status progression:

```
assigned (default)
    ↓
confirmed (member confirms availability)
    ↓
completed (duty is done)
    ├→ cancelled (cancelled before completion)
    └→ no-show (member didn't show up)
```

## Database Schema

### RosterTemplate Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | Template name |
| description | String | Optional description |
| days_of_week | JSON | Array of day numbers (0-6) |
| start_date | Date | Template start date |
| end_date | Date | Optional template end date |
| start_time | String | Time in HH:MM format |
| end_time | String | Time in HH:MM format |
| subunits | JSON | Array of subunit IDs |
| roles | JSON | Array of role names |
| members_per_slot | Integer | Members per role |
| is_active | Boolean | Template active status |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### DutyRoster Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| template_id | Integer | FK to RosterTemplate |
| duty_date | Date | Date of duty |
| start_time | String | Time in HH:MM format |
| end_time | String | Time in HH:MM format |
| assigned_to | String | Member name |
| subunit | String | Member's subunit |
| role | String | Assigned role |
| status | String | Current status (assigned/confirmed/completed/cancelled) |
| confirmed_by | String | Who confirmed (member name or admin) |
| confirmed_at | DateTime | When confirmed |
| created_at | DateTime | Creation timestamp |

## Best Practices

### Template Creation
- **Be specific with names**: Use names that clearly indicate when/what (e.g., "Sunday Choir 2024 Q1")
- **Group similar duties**: Create templates for repeating patterns
- **Realistic member counts**: Set members per slot based on available pool

### Roster Generation
- **Plan ahead**: Generate rosters a month in advance when possible
- **Date ranges**: Use appropriate end dates to prevent infinite generation
- **Clear old rosters**: Consider clearing old rosters before generating new ones to avoid duplicates

### Member Management
- **Notify early**: Enable notifications so members know duties in advance
- **Confirmation tracking**: Monitor confirmation rates to ensure coverage
- **Fallback planning**: Have backup members in case of cancellations

## Troubleshooting

**No eligible members found when generating**
- Check that subunits are selected in template
- Verify members are approved/completed in the application process
- Check member's assigned_subunit_id matches template subunits

**Rosters not generating for all dates**
- Verify end_date is set correctly (rosters don't generate beyond end_date)
- Check that days_of_week are selected correctly (0=Monday, 6=Sunday)
- Ensure sufficient date range is specified

**Members not able to confirm**
- Check member's browser permissions
- Verify member is logged in/has proper access
- Check roster status is "assigned" before confirmation

**Export showing incorrect data**
- Ensure you're exporting the correct template
- Check date filters if partial export is needed

## Advanced Features (Future Enhancements)

Potential additions:
- Email notifications to assigned members
- Automatic conflict detection
- Member preferences and availability calendar
- Recurring roster templates (weekly/monthly)
- Performance metrics and analytics
- Substitution/swap functionality
- REST API for mobile app access

## Frequently Asked Questions

**Q: Can I create multiple rosters for the same date?**
A: Yes. Different templates can generate rosters for the same date. This is useful for having multiple groups performing simultaneously.

**Q: What happens if I delete a template?**
A: All associated rosters are also deleted (cascading delete). This is permanent, so download/export data first if needed.

**Q: Can members view rosters without logging in?**
A: Rosters are visible to logged-in members and also available through `/roster/view` which is accessible to all. Status filtering may depend on authentication level.

**Q: How are members assigned if more than one slot exists?**
A: The system uses a round-robin algorithm. If there are 5 eligible members and 3 slots per role, the algorithm distributes assignments to ensure fair coverage and avoid duplicates in the same date/role.

**Q: Can I manually add/remove individual rosters?**
A: Yes. You can delete rosters individually from the View Rosters page. To manually reassign, delete the roster and use the form to create a new one.

---

## Support & Contact

For questions or issues with the Roster Manager feature, contact the system administrator or refer to the main project documentation.
