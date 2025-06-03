
# Provider Account Registration

## Description
As a cleaning service provider, I want to create a professional account on MyClean so I can offer my availability and start accepting customer bookings.

## Priority
**Range**: 9 (Very high significance)  
**Iteration**: 1

**Notes:**
- Critical for onboarding service providers
- Enables the supply side of the platform
- Must be completed before bookings can happen
- Foundational feature for provider-facing flows

## Estimation
**Assumptions:**
- Standard registration fields (business name, email, password, phone)
- Email and phone validation required
- Secure password storage
- Backend API endpoints for provider registration
- Account type tagged as 'provider' in the database

**Planning Poker Results:**
- DANG CHEN: 1.5 days  
- Denzel Suhermin: 1.5 days  
- Rui Yan: 2 days  
- Jin Wang: 1 day  
**Average:** 1.5 days

## Tasks

**Backend (Rui Yan & DANG CHEN):**
1. Design provider registration API and data model – 0.5 days  
2. Implement registration endpoint with field validation – 1 day  
3. Add provider-specific validation (e.g. phone number format) – 0.5 days  
4. Store provider role and contact info in database – 0.5 days  
5. Write tests – 0.5 days

**Frontend (Denzel Suhermin & Jin Wang):**
1. Design provider registration form UI – 0.5 days  
2. Implement form with validation – 1 day  
3. Connect to backend API – 0.5 days  
4. Handle API response, error display, and navigation – 0.5 days  
5. Write tests – 0.5 days

## UI Design (Pics)

**Registration Form Elements:**
- MyClean logo  
- “Join as a Provider” heading  
- Input fields: Business Name, Email, Password, Confirm Password, Phone Number  
- Register button  
- “Already have a provider account? Log In” link  
- Error message display areas

## Completion Criteria
- Providers can successfully register with valid business/contact details  
- Form validates inputs and displays errors as needed  
- Successful registration redirects to provider dashboard or login  
- Provider accounts stored with appropriate role tags  
- Passwords are securely hashed and stored
