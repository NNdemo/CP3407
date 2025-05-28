# Customer Account Login

## Description
As a registered user of MyClean, I want to log in to my account so that I can access my bookings and manage my cleaning services.

## Priority
**Range**: 10 (Highest significance)  
**Iteration**: 1

**Notes:**
- Important for all users who have used the system before
- Supports both safe and dependable logins
- It is required for receiving services that are customized for you.

## Estimation
**Assumptions:**
- Login onto the website using your email and password.
- Uses session and token-based authentication.
- Your passwords are already carefully protected.
- The backend will examine the credentials and then return a token or session.

**Planning Poker Results:**
- DANG CHEN: 2 days  
- Denzel Suhermin: 1.5 days  
- Rui Yan: 1 days
- Jin Wang: 1 day  
**Average:** 1.4 days

## Tasks
**Backend (DANG CHEN & Rui Yan):**
1. Design login API endpoint - 0.5 days  
2. Implement credential validation - 0.5 days  
3. Implement session/token generation - 0.5 days  
4. Handle login error states - 0.5 days  
5. Write backend tests - 1 day  

**Frontend (Denzel Suhermin & Jin Wang):**
1. Design login form UI - 0.5 days  
2. Implement form with validation - 1 days  
3. Connect form to login API - 0.5 days  
4. Display login error messages - 0.5 days  
5. Redirect on success and write tests - 0.5 days  

## UI Design (Pics)
**Login Form Elements:**
- MyClean logo  
- "Welcome Back" or "Login to Your Account" heading  
- Input fields: Email, Password  
- Login button  
- "Don't have an account? Register" link  
- Error message display for invalid credentials  

## Completion Criteria
- Users are able to use their log-in name and secret password to connect.  
- Incorrect credentials cause the system to show the right error messages.  
- Users are directed to their main home page when they log in correctly.  
- Your token or session is stored in a safe environment.