# Library Page — README (Book Club)
## Overview

The **Library Page** displays all available books in a responsive grid of book cards.
Each card shows the cover, title, author, price, and a bookmark icon.
The Library is publicly accessible to all visitors (including guests). However, only authenticated users can purchase or read books.

## Core User Flows

*** Browse Books:** Users can scroll through a grid of book cards that represent available titles.

***Book Details:** Clicking a book card navigates to that book’s Book Page.

***Guest Restrictions:** Guests can view the Book Page but cannot purchase or read the book.

## Global Layout

***Header** and **Footer** are global components reused across the entire site. They appear on every page, including the Library Page.

## Components & Content

***Books Grid:**

Built with CSS Grid to create a responsive layout.
Automatically adjusts the number of columns based on screen size.
Each grid cell contains a Book Card.

**Book Card:**

Displays the cover image of the book.
Shows the title and author.
Contains a meta section with the price and a bookmark SVG icon.
On hover, the card slightly lifts (translateY) and gains a shadow, creating an interactive effect.

**Navigation:**

Clicking a book card leads to its dedicated Book Page.
Behavior by Auth State
**Guest (not signed in):**
Can view the Library and open Book Pages.
Cannot purchase or read a book.

## Authenticated User:

Can view all details and has access to purchase/read options on Book Pages.
Current Frontend State (Pre-JavaScript)
The Library is currently implemented as a static grid with dummy book cards.
Hover effects (transform, box-shadow) are already in place for interactivity.
Clicking a card routes to a placeholder Book Page until backend logic is implemented.

## Future Enhancements

Connect the Library grid to a backend/database for dynamic book loading.
Add filtering and sorting (by author, genre, price, etc.).
Implement real purchase/read functionality tied to authentication.
Introduce lazy loading or pagination for large book collections.

## Navigation Summary

**Header / Footer:** Shared components across the site.

**Library Grid:** Displays all available books.

**Book Card:** Click → navigates to Book Page.

**Guest restriction:** Guests cannot purchase/read books.