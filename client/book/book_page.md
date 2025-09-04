# Book Page — README (Book Club)
## Overview

The **Book Page** is a dedicated page for each book in the system.
It displays a book card with the cover, title, author, release year, a short summary, and the price in “bookmarks.”
Below the card, users can see the Reviews section, where readers share and reply to reviews.

## Core User Flows

**View Book Details:** Each Book Page contains the book cover, title, author, year of release, and a short description.

## Purchase Flow:

**Guest:** Can only see the book’s price in bookmarks.

**Authenticated (no purchase):** Sees a Buy Now button if they have enough bookmarks.

**Authenticated (purchased):** Sees a Read PDF button that links directly to the book’s PDF.

## Reviews:

Guests can read existing reviews but cannot write new reviews.
Authenticated users can write a new review (title + content).
Authenticated users can reply to existing reviews.
Users can delete only their own replies (not yet implemented in JS).

## Global Layout

Header and Footer are global components reused across the entire site.
Both appear on every page, including the Book Page.

## Components & Content
📖 **Book Card**
Cover image — book’s front cover.
Book details — title, author, release year, summary.
Price section — shows the book’s cost in bookmarks.
**Action buttons:**
Guests → only see the price.
Authenticated users without purchase → “Buy Now” button.
Authenticated users with purchase → “Read PDF” button.

⭐ **Ratings (To-Do)**
A star rating system will display the average score of the book.
Not implemented yet — will be handled in JavaScript.

📝 **Reviews**
Each review contains a title and content.
Replies are shown indented under each review.
Reply and delete actions are visually available, but Delete is disabled until JS logic is added.
Guests can only read reviews; the “new post” editor and reply form will be hidden for them once JS logic is connected.

## Behavior by Auth State

**Guest (not signed in):**
Can see the book details and price.
Can read reviews and replies.
Cannot purchase, read, or write reviews.

**Authenticated User (not purchased):**
Can see the book details and price.
Sees a Buy Now button (if they have enough bookmarks).
Can write reviews and replies.
Can only delete their own replies (to be enforced in JS).

**Authenticated User (purchased):**
Can see book details and price.
Sees a Read PDF button linking directly to the book’s PDF.
Full review/reply permissions as above.

## Current Frontend State (Pre-JavaScript)

Buy / Read flow: Buttons are present but behavior is simulated only by CSS (hidden class).
Delete buttons: Present in markup but disabled (disabled + aria-disabled="true") until JS is implemented.
Reply forms: Included in HTML, hidden by default with .hidden, will later be toggled with JS.
Guest restrictions: Not yet dynamic — forms are still visible; hiding will be implemented in JS.
Star ratings: Placeholder — not yet implemented.

## Future Enhancements

Implement auth-based logic in JS: hide/show Buy/Read buttons, review forms, and enforce guest restrictions.
Connect the Buy Now button to the user’s bookmarks balance.
Wire the Read PDF button to actual user entitlements.
Add star rating system with average calculation and display.
Enable reply toggle logic with JavaScript (click → open reply editor).
Enforce delete ownership in backend (only allow deleting your own replies).
Add empty state messages when no reviews exist.

## Navigation Summary

**Header / Footer:** Shared site-wide components.
**Book Card:** Displays book details + price + appropriate action button.
**Reviews Section:** Shows all reviews and replies; editor appears for authenticated users.
