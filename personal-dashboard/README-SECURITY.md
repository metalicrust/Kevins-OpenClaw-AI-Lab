# ⚠️ PERSONAL DASHBOARD - LOCAL USE ONLY

**DO NOT COMMIT THIS DIRECTORY TO GITHUB**

This directory contains sensitive personal information including:
- Health data and medical conditions
- Personal schedules and location information
- Financial/cryptocurrency portfolio details

## Security Notice

All files in this directory should remain **local only**. They have been removed from git tracking for your privacy and security.

## Template Files

Use the `-TEMPLATE.md` files as starting points:
- Copy template to create your personal version
- Remove "-TEMPLATE" from the filename
- Fill in your personal data
- **Keep locally - never commit**

## Files That Should Stay Local

- `health/tracker.md` - Medical information
- `general/reminders.md` - Personal schedules, locations
- `crypto/portfolio.md` - Financial data
- `content/calendar.md` - Personal content planning

## If These Files Are Currently in Git

Run these commands to remove them from git (keeping local copies):

```bash
git rm --cached personal-dashboard/**/*.md
echo "personal-dashboard/" >> .gitignore
git commit -m "Remove personal data from repository"
```

---

**Remember:** Your personal health, location, and financial data should never be in a public or shared repository.
