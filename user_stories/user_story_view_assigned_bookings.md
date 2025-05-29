# View Assigned Bookings


## Description
As a user, I need an interface to view the cleaning services that I have booked, including address, date, time, and service type， just like viewing orders.


## Priority

**Range**: 30<br>
**Iteration**: 1

**Notes:** <br>
- As a sub-function of the application
- Users can view their orders here and perform operations on them.
- Not as foundational as login, but crucial for task planning.
- Slightly more complex as it involves fetching and rendering data.


## Estimation

**Assumptions:**
- Booking assignment logic is already handled by the backend.
- API is ready to provide a list of assigned bookings.


**Planning Poker:**
- DANG CHEN: 2 days
- Denzel Suhermin: 1 days
- Rui Yan: 3 days
- Jin Wang: 1.5 days<br>
- **Average:** `1.875` days 


## Tasks
**Backend (DANG CHEN & Rui Yan):**
1. Order statu API - 1 day
2. Database - 1 day
3. Test - 0.5 days


**Frontend (Denzel Suhermin & Jin Wang):**
1. Low-fidelity login interface design (such as Figma) - 1 day
2. Implement the front-end design - 1 day
3. Connect to backend APIs - 0.5 days
4. Test - 0.5 day


## UI Design 

1. **Overview of all orders**
   - List all orders including order status, time, location and other information

1. **Order modification interface**
   - Can modify the order here, such as changing the order time, location, or canceling the order


## Completed:
* Users can use this interface to view the order status
* Users can perform operations on orders, such as canceling orders and modifying times through this interface
* Screenshots of the functions or other introductions will be attached after completion