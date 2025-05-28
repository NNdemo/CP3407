# Browse Cleaning Services

## Description
As a potential customer, I want to browse a list of available cleaning services and view cleaner details so I can decide which service best suits my needs before booking.

## Priority
**Range**: 10 (Highest importance)  
**Iteration**: 1

**Notes:**
- Users can discover the different services provided before they decide.
- It helps people decide but does not request confirmation from the token’s owner.
- User engagement depends on it, yet it is less important than booking or login.

## Estimation
**Assumptions:**
- User can browse freely without logging in
- The system already benefits from services and better data.
- Filters and sorting tools are basic features included.
- Profile cards list name, the type of service offered, how much it costs and the user’s rating.

**Planning Poker Results:**
- DANG CHEN: 2.5 days  
- Denzel Suhermin: 2 days  
- Rui Yan: 1.5 days  
- Jin Wang: 1.5 days  
**Average:** 1.9 days

## Tasks
**Backend (DANG CHEN & Rui Yan):**
1. Create a design service data model and structure - 0.5 days  
2. Develop and add an API to return a list of all active services - 0.5 days  
3. Add a few simple filters (for rating, location, price) - 1 day  
4. Be sure to list the profile’s photo, name and description - 0.5 days  
5. Create both unit and integration tests - 1 day

**Frontend (Denzel Suhermin & Jin Wang):**
1. Make the UI for the design booking flow - 1 day
2. Add a service selection feature - 1 day
3. Set up a picker for both date and time to show available functions - 1 day
4. Make confirmation page for booking - 0.5 days
5. Get data from the backend APIs - 0.5 days
6. Navigate and address customer responses - 0.5 days
7. Write a test for your feature - 1 day

## UI Design
**Browse Page Layout:**
1. **Search/Filter Bar**  
   - Text search  
   - Dropdowns for rating, price, service type  

2. **Cleaner Service Cards**  
   - Profile picture  
   - Name and service type  
   - Rating (e.g. ★★★★☆)  
   - Price per hour/session  
   - "View More" button (leads to detail view or booking page)

3. **Responsive Layout**  
   - Grid on desktop  
   - Stack layout for mobile devices

## Completion Criteria
- Anyone can check the available cleaning services without making an account.  
- The profiles list key information: name, service, customer rating and price.  
- Filtering and sorting on application works as it should.  
- When you click a profile, you are taken to a full view or a page where you can book the service.  
- The website is designed to look right on all devices.
