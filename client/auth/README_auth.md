# Auth Pages — README (Book Club)

## Overview

The **Auth section** contains the entry point for account access.
From the main Auth page (Auth Hub), guests choose whether to Sign Up or Sign In.

**Sign Up:** Opens a page with personal details to create a new account.

**Sign In:** Opens a page to log in with email and password.

After successful authentication, the Header changes from “Sign in / Register” to “Hello, {Name}!” with a small dropdown that includes Logout.
Additional navigation for authenticated users appears: My Profile and All Groups.

## Core User Flows

**Choose Auth Path (Auth Hub):**
Guests select Sign Up or Sign In.

**Sign Up:**
User fills Full Name, Email, Password, Confirm Password → on success, navigates to Profile Page.
Header updates to “Hello, {Name}!” with a mini-menu (Logout), and new links appear:
My Profile and All Groups.

**Sign In:**
User enters Email + Password → on success, navigates to the Landing Page.
Header updates to “Hello, {Name}!” with mini-menu (Logout), and My Profile / All Groups become available.

## Global Layout

Header and Footer are global across the site and also appear on all Auth pages.
Header shows two visual states:
Guest: “Sign in / Register”
Authenticated: “Hello, {Name}!” + dropdown (Logout), plus links to My Profile and All Groups.

## Future Enhancements (JavaScript & Backend)

Auth state management: Persist login (e.g., localStorage/cookies), and toggle Header state across all pages.

Form validation & errors: Validate email/password, match confirm password, show inline error messages.

## Navigation Summary

**Auth Hub:** Choose Sign In or Sign Up.

**Sign Up:** On success → Profile Page; Header → “Hello, {Name}!” + Logout; links: My Profile, All Groups.

**Sign In:** On success → Landing Page; Header → “Hello, {Name}!” + Logout; links: My Profile, All Groups.