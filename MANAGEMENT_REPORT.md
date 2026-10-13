# Barber Hub — Management Report

**Date:** October 13, 2026
**Scope:** Implemented features and user-facing workflows currently available on the website. This report intentionally excludes implementation and technical details.

---

## 1. Executive Summary

Barber Hub is the online presence of the barbershop: a Persian-language, right-to-left website through which **customers book hair appointments** and **shop for salon products**, while **barbers** and **salon managers** manage the operation from their own dedicated panels.

Today the platform supports the complete end-to-end journey for both sides of the business:

- **Appointments:** customers log in with just a mobile number, pick a barber, pick one or more services, choose a free time slot, and confirm — with the system automatically preventing double-bookings.
- **Product store:** a full storefront with catalogue, search, cart, checkout, and online payment, plus order tracking for customers and an order-processing pipeline for staff.
- **Staff panels:** barbers see and manage their own day, services, and weekly schedule; managers oversee salon-wide appointments, the service catalogue, and the entire store operation.

---

## 2. User Roles and Access

The website serves three user roles. Each signs in through a separate login page suited to that role:

| Role | How they sign in | Where they land |
| --- | --- | --- |
| **Customer** | Mobile number + one-time SMS code (no password needed) | Booking wizard / Store |
| **Barber** | Username and password, restricted to active barber accounts | Barber panel |
| **Manager** | Username and password, restricted to salon management accounts | Manager panel |

Customers are created automatically the first time they verify their mobile number — there is no separate registration step.

---

## 3. Public Pages (No Login Required)

- **Landing page** — the website's front door, introducing the salon and leading visitors directly into the appointment booking flow.
- **Storefront** — the product store home page, showing all published product categories and products. Visitors can browse, filter by category, and search products without an account.
- **Product detail pages** — each product has its own page with photos (image gallery), description, and price. A dedicated "product not found" page handles invalid links gracefully.
- A standard **administration console** is also available to technical staff at a separate address (not part of the customer experience).

Signing in is only required when adding items to the cart, checking out, or submitting a booking.

---

## 4. Customer Journey 1 — Appointment Booking

The booking experience is a guided 4-step wizard. The customer's progress is kept on their own device, so they can move between steps without losing their selections.

### Step 1: Sign in with mobile number (SMS code)
1. The customer enters their mobile number.
2. A 6-digit verification code is sent to that number by SMS.
3. The customer enters the code to sign in.
   - Codes expire after **2 minutes**, and each code can be used only once.
   - First-time customers get an account automatically; returning customers simply sign back in.

### Step 2: Choose a barber and services
1. The website shows the salon's barbers together with the services each one offers.
2. The customer selects one barber and one or more services.
3. The running total price and total duration of the visit are shown as services are added.

### Step 3: Choose a date and time
1. The customer picks a date.
2. The system calculates which time slots are genuinely free — it takes into account the barber's weekly working schedule, the total duration of the selected services, and existing bookings, so two customers can never book the same barber at the same time.
3. Only available slots are offered; booked or outside-working-hours times are not selectable.

### Step 4: Review and confirm
1. The customer sees a full summary — barber, selected services, date, time, and total price — before anything is final.
2. On confirmation, the appointment is registered and a **booking confirmation page** is displayed with all the details of the visit.

### What happens after booking
The appointment moves through a lifecycle managed by the barber (see Section 5): it starts as *Pending*, and is then *Confirmed*, *Completed*, or *Cancelled* by the barber. Only pending and confirmed appointments count toward a barber's availability, so a cancelled visit frees the slot for another customer.

---

## 5. Customer Journey 2 — Product Store Purchase

### Browsing
Customers browse the storefront, filter by category, or search by name (no login needed). Each product page shows the photo gallery, description, and price.

### Shopping cart
1. While signed in, the customer adds products to the cart in the desired quantity.
2. The cart page shows all items, their unit prices, the item count, and the total.
3. The customer can change quantities or remove items at any time before checkout.

### Checkout and payment
1. The **checkout page** shows a final review of the cart contents and total price.
2. The customer can attach a note to the order (e.g., special requests).
3. When the order is submitted:
   - If any product price has changed since the customer saw it, the system **asks the customer to confirm the new prices** before the order goes through — protecting against surprises.
   - Duplicate submissions are prevented, so refreshing or re-clicking cannot create a second identical order.
4. The customer is redirected to the **Zarinpal online payment gateway** to pay securely.
5. After paying, the customer returns to a **payment result page** showing the order, its items, and the payment status.

### Order tracking
- **Order history** — every customer can see all their past orders with their current status.
- **Order detail page** — full contents, prices, total, payment status, and any note the customer attached.
- **Retry payment** — if a payment failed or was interrupted, the customer can retry it directly from the order page, as long as the order is still awaiting payment.

### Order statuses
Each order moves through a clear pipeline that staff manage (see Section 7):

Awaiting Payment → Placed → Reviewed → Ready for Pickup → Delivered (or Cancelled)

---

## 6. Barber Panel

Available to salon barbers after signing in with their own accounts:

- **Today's dashboard** — the barber's appointments for the day, with the total count at a glance and each appointment's current status clearly labelled.
- **Appointment management** — with one click, the barber can mark an appointment as **Completed** (the visit is done) or **Cancel** it (freeing the time slot).
- **My services** — the barber sees the salon's full service catalogue and chooses which services to offer. For each service they can keep the salon's default price and duration, or set their own custom price and custom duration.
- **Weekly working hours** — a weekly schedule editor where the barber defines their working hours per day of the week. These hours directly control which time slots customers are offered.

---

## 7. Manager Panel

Available to salon managers after signing in with their own accounts:

### Appointments
- **Today's appointments** — a salon-wide dashboard showing all of today's appointments across every barber and customer.

### Salon services
- **Service catalogue management** — managers maintain the salon's master list of services: create new services, edit existing ones (name, base price, default duration, description), and enable/disable services. Barbers then offer these services (with optional personal pricing).

### Store — catalogue
- **Product categories** — create, edit, and delete the categories customers filter by.
- **Products** — create and edit products with title, description, price, category, and **multiple uploaded photos**; publish or unpublish a product; control whether a product can be ordered; delete products (removed from the storefront without destroying their order history).

### Store — orders
- **Order list** — all store orders, filterable by status.
- **Order detail** — full order contents, the customer's contact details and note, and payment information.
- **Order processing** — the manager advances each order through its lifecycle: marking it as Reviewed, Ready for Pickup, or Delivered, or cancelling it.

---

## 8. Status Reference

**Appointment statuses**

| Status | Meaning |
| --- | --- |
| Pending | Booked by the customer, awaiting the barber's confirmation; occupies the time slot |
| Confirmed | Confirmed by the barber; occupies the time slot |
| Completed | The visit took place and is finished |
| Cancelled | Called off by the barber; the time slot becomes available again |

**Store order statuses**

| Status | Meaning |
| --- | --- |
| Awaiting Payment | Order created; the customer has not completed payment yet |
| Placed | Payment completed; the salon should start processing it |
| Reviewed | Staff have seen and started processing the order |
| Ready for Pickup | Prepared and waiting for the customer |
| Delivered | Handed over to the customer; order closed |
| Cancelled | Cancelled by staff |

---

## 9. Implemented but Not Yet Visible to Users

The following capabilities exist internally but currently have no page on the website, and are listed here for planning purposes:

- **Customer profile information** (name/details) and the **personal hairstyle gallery** (customers saving haircut styles) — the underlying capability is built, but no customer-facing pages expose it yet.
- A **customers list page** has been prepared but is not linked anywhere.
- There is no **sign-out link** in the site navigation yet; sessions end by other means.

These are natural candidates for the next release and require no rework of existing features — only new pages.

---

## 10. Summary of What the Website Delivers Today

| Area | Status |
| --- | --- |
| SMS-based customer login | ✅ Live |
| Appointment booking wizard (barber, services, date/time, review, confirm) | ✅ Live |
| Double-booking prevention based on barber schedules | ✅ Live |
| Barber panel (today's appointments, statuses, services, working hours) | ✅ Live |
| Manager panel (salon appointments, service catalogue) | ✅ Live |
| Store storefront, search, product pages | ✅ Live |
| Cart, checkout, online payment (Zarinpal) | ✅ Live |
| Customer order history and payment retry | ✅ Live |
| Manager store management (catalogue, products, orders) | ✅ Live |
| Customer profile & hairstyle gallery pages | ⏳ Built, not yet exposed |
