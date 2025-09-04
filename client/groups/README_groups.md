# Groups Page — README (Book Club)

## Overview

The **Groups Page** is available only to authenticated users.
It provides an overview of all existing Book Clubs, displayed as a grid of group cards.
Each card represents a single reading group and links to that group’s dedicated page.

## Core User Flows

**Access:** Only logged-in users can access the Groups Page (via the Header navigation).

**Browse Groups:** Users scroll through a grid of group cards.

**View Group Details:** Each card shows:
Group cover image
Group name
Group purpose/goal (short description)

**Navigate to Group Page:** Clicking a card takes the user to the Group Page with more details about that specific group.

**Authenticated user:**
Can open the Groups Page from the Header.
Can browse all group cards and click into a specific group.

# Current Frontend State (Pre-JavaScript)
Static placeholder cards are implemented for layout and styling.
Cards visually simulate navigation to a Group Page (e.g., via static links).
No real backend or database connection yet.

# Future Enhancements
**Dynamic loading:** Fetch groups from a backend/database instead of static placeholders.
**Search / Filter:** Add options to filter groups by name, purpose, or current book.
**Join / Leave group actions:** Buttons for authenticated users to join or leave a group.
