# Prd Issues Breakdown

## Epic: User Registration & Profile Management

### User Story: Allow users to register and create profiles with verified information.
**Request:** Enable users to download the app, register with a verified phone number, and complete their profile with necessary identification and payment methods.

**Acceptance Criteria:** Users can register using a verified phone number. Users can upload identification documents. Users can link payment methods to their profile.

**Priority:** High

**Labels:** onboarding, authentication, security

#### Tasks:
- **Task:** Implement user registration with phone number verification
  - **Description:** Develop a system to register users with phone number verification and ensure account security.
  - **Priority:** High
  - **Labels:** authentication, security, backend, API

- **Task:** Design Profile Creation UI
  - **Description:** Create the frontend page for users to upload identification and link payment methods.
  - **Priority:** Medium
  - **Labels:** frontend, UI, onboarding

- **Task:** Develop API for storing user profiles
  - **Description:** Build backend services to securely store and manage user profile information.
  - **Priority:** High
  - **Labels:** backend, API, database

### User Story: Allow users to set their ride preferences and route details.
**Request:** Provide users the ability to set their home and work locations, preferred times, vehicle preferences, and detour tolerance.

**Acceptance Criteria:** Users can set home and work locations. Users can specify travel times and vehicle preferences. Users can define maximum detour time they are willing to accept.

**Priority:** Medium

**Labels:** frontend, UX, database

#### Tasks:
- **Task:** Create UI for route and preference setup
  - **Description:** Design and implement the user interface for setting ride preferences and specific routes.
  - **Priority:** Medium
  - **Labels:** frontend, UI, UX

- **Task:** Develop backend logic for storing ride preferences
  - **Description:** Build services to handle the storage and retrieval of user ride preferences.
  - **Priority:** Medium
  - **Labels:** backend, database

---

## Epic: Ride Sharing Coordination

### User Story: Enable users to request rides and receive potential matching options.
**Request:** Users should be able to enter destinations and receive shared ride options with cost and time savings estimates.

**Acceptance Criteria:** Users can see potential ride matches. Users receive estimated ride costs and time savings. Users can choose to accept or decline matches.

**Priority:** High

**Labels:** ride-sharing, frontend, backend, UX

#### Tasks:
- **Task:** Implement destination input and matching suggestion
  - **Description:** Develop a system for users to input destination and see shared ride options and savings.
  - **Priority:** High
  - **Labels:** backend, algorithm, frontend

- **Task:** Create algorithm for ride matching
  - **Description:** Develop a reliable and efficient algorithm for matching users based on destinations and preferences.
  - **Priority:** High
  - **Labels:** backend, algorithm, data

- **Task:** Design UI for ride request flow
  - **Description:** Create the user interface that displays ride-sharing options and allows users to accept or decline matches.
  - **Priority:** Medium
  - **Labels:** frontend, UI, UX

### User Story: Ensure seamless ride confirmation and finalization of matches.
**Request:** Once users are matched, finalize ride details, confirm payment splits, and complete safety verifications.

**Acceptance Criteria:** Ride details are confirmed after user acceptance. Payment is securely split among confirmed rides. Safety checks are completed before ride initiation.

**Priority:** High

**Labels:** backend, security, payment, UX

#### Tasks:
- **Task:** Develop ride confirmation process
  - **Description:** Implement a process to confirm ride details, including payment and safety verification, after user match acceptance.
  - **Priority:** High
  - **Labels:** backend, API, payment

- **Task:** Integrate payment system for automatic splits
  - **Description:** Build a payment system that automatically calculates and splits costs among riders.
  - **Priority:** High
  - **Labels:** payment, backend, API

- **Task:** Ensure safety verification during confirmation
  - **Description:** Implement safety protocols and checks to verify user identities and ensure compliance before ride confirmation.
  - **Priority:** High
  - **Labels:** security, backend

---

## Epic: In-Ride Experience & Safety

### User Story: Enhance user safety and experience during rides with real-time tracking and communication.
**Request:** Provide users with features such as real-time GPS tracking, a communication channel with riders, and emergency support.

**Acceptance Criteria:** Real-time tracking is available during rides. Users can communicate with co-riders through the app. An emergency button provides immediate support access.

**Priority:** High

**Labels:** safety, UX, GPS, frontend

#### Tasks:
- **Task:** Implement real-time GPS ride tracking
  - **Description:** Develop a feature that allows users and drivers to share real-time location status during rides.
  - **Priority:** High
  - **Labels:** backend, API, GPS

- **Task:** Create rider communication channel
  - **Description:** Build an in-app chat or communication interface for riders to interact with each other during the ride.
  - **Priority:** Medium
  - **Labels:** frontend, communication, UX

- **Task:** Develop emergency support feature
  - **Description:** Create a quick-access emergency support button and protocol for users to report issues during rides.
  - **Priority:** High
  - **Labels:** safety, UX, frontend, backend

---

## Epic: Payment System & Financial Management

### User Story: Provide a secure and transparent payment system for ride cost handling.
**Request:** Build a system for processing payments after rides, ensuring transparency in cost-sharing, and offering various payment options.

**Acceptance Criteria:** Payments can be processed securely after a ride. Cost-sharing is transparent and clearly communicated. Multiple payment methods (credit card, digital wallets) are available.

**Priority:** High

**Labels:** payment, security, finance

#### Tasks:
- **Task:** Integrate secure payment gateway
  - **Description:** Implement a payment gateway that securely processes transactions for ride payments.
  - **Priority:** High
  - **Labels:** backend, payment, security

- **Task:** Create transparent cost-sharing mechanism
  - **Description:** Develop a system to clearly articulate how costs are split among riders and ensure transparency.
  - **Priority:** Medium
  - **Labels:** backend, finance, UX

- **Task:** Enable multiple payment method options
  - **Description:** Provide users with the flexibility to use different payment methods (e.g., credit/debit card, mobile wallets) during transactions.
  - **Priority:** Medium
  - **Labels:** frontend, payment, user choice

---

