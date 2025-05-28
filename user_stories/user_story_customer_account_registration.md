# Customer Account Registration

## Description
As a potential user of MyClean, I want to create a personal account so I can access the app's features and book cleaning services.

## Priority
**Range**: 10 (Highest significance)
**Iteration**: 1

**Notes:**
- Entry point for all users into the system
- Core foundational feature
- Essential for customer acquisition

## Estimation
**Assumptions:**
- Standard registration fields (name, email, password)
- Email validation required
- Secure password storage
- Backend API endpoints for registration

**Planning Poker Results:**
- DANG CHEN: 2 days
- Denzel Suhermin: 1.5 days
- Rui Yan: 1 day
- Jin Wang: 1 day
**Average:** 1.4 days

## Tasks
**Backend (DANG CHEN & Rui Yan):**
1. Design user registration API and data model - 0.5 days
2. Implement user registration endpoint with validation - 1 day
3. Implement password security - 0.5 days
4. Create database storage - 0.5 days
5. Write tests - 1 day

**Frontend (Denzel Suhermin & Jin Wang):**
1. Design registration form UI - 0.5 days
2. Implement form with validation - 1 day
3. Connect to backend API - 0.5 days
4. Handle responses and navigation - 0.5 days
5. Write tests - 0.5 days

## UI Design (Pics)
**Registration Form Elements:**
- MyClean logo
- "Create Your Account" heading
- Input fields: Full Name, Email, Password, Confirm Password
- Register button
- "Already have an account? Log In" link
- Error message display areas

## Completion Criteria
- Users can successfully create accounts with valid information
- Form validates input and shows appropriate error messages
- Successful registration redirects to appropriate page
- Passwords are securely stored 