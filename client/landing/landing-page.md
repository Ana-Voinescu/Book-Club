# Landing Page — README (Book Club)

## Overview

The **Landing Page** is the primary entry point of the Book Club website. Clicking the site name next to the logo always returns the user to this Landing Page.

## Core User Flows

* **Search (Books / Groups):** Users can search by book or group name. Pressing **Enter** navigates to the matching page (Book page or Group page). In a future iteration, the search input will show **type‑ahead/autocomplete** suggestions as the user types.
* **Authentication:** Visitors can **Sign up** or **Sign in** from the Landing Page. Once authenticated, users can quickly access **My Profile** and the **All Groups** list directly from the Landing Page.
* **Library Access:** A visible entry point to the **Library** is available from the Landing Page for quick browsing.

## Global Layout

* **Header** and **Footer** are global components reused across the entire site. They appear on every page, including the Landing Page.

## Components & Content

* **Header:** Logo + site name (clicking returns to Landing), primary navigation (Library, Groups, Sign in/Sign up or Profile when logged in).
* **Main Content:** Hero/intro text, search bar for Books/Groups, and shortcuts to common destinations (e.g., Library, All Groups).
* **Footer:** Basic links, copyright, and any legal or contact references.

## Behavior by Auth State

* **Guest (not signed in):** Sees Sign in / Sign up. Certain buttons/links intended only for authenticated users are **hidden**.
* **Authenticated user:** Sees quick links to **My Profile** and **All Groups** from the Landing Page.

## Current Frontend State (Pre‑JavaScript)

* Before wiring up JavaScript, the project uses a **CSS utility class** to **hide elements** that should not be visible to guests. This ensures the Landing Page mock‑up reflects the intended experience even without dynamic logic.

  * Example (conceptual):

    * `.hidden-for-guest` — applied to buttons/links that only logged‑in users should see. When the auth logic is implemented, this class will be toggled/removed accordingly.

## Future Enhancements

* Wire the search input to backend data and implement **autocomplete** (books & groups) with keyboard navigation and selection.
* Replace guest‑hiding via CSS with **real auth state** checks (JS + backend), rendering only permitted controls.
* Persist search query in URL (e.g., `?q=`) and show graceful empty states if no results are found.
* Add analytics for search usage and click‑through to measure engagement.

## Navigation Summary

* **Logo / Site name:** Returns to Landing Page.
* **Search:** Enter → navigates to the appropriate Book/Group page.
* **Auth:** Sign in / Sign up; when signed in → My Profile, All Groups.
* **Library:** Direct link from the Landing Page.

## Notes

* Keep Header/Footer DRY and shared across routes.
* Maintain accessible labels for the search input and buttons.
* Ensure tab order is logical; hitting **Enter** in the search field should submit search.
