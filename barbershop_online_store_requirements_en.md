# Software Requirements Specification (SRS): Online Barbershop Products Store
**Version 1.0**

## 1. Purpose and Scope

The purpose of this project is to provide an online store for barbershop products as part of the website. The barbershop manager manages the products, while customers can sign in to their accounts, select the products they want, place orders, pay online, and collect their purchases in person at the barbershop.

This document defines only the business requirements and information flow; it does not cover implementation details.

## 2. Category and Product Management

The barbershop manager must be able to create, view, edit, and delete product categories.

The manager must also be able to create, view, edit, and delete products. Each product must include the following information:

- Product title
- Description and specifications
- Price
- Product images
- Associated category
- Publication status
- Order availability status

The manager must be able to specify whether each product is available for customers to order.

In the first release, the system does not need to track exact inventory quantities. Therefore, whether a product can be ordered is determined by the status set by the manager.

## 3. Browsing and Selecting Products

Customers can visit the store section to view active categories and the products belonging to each category.

Each product has its own detail page displaying its title, images, description, price, and order availability status.

Customers can select products that are available to order. Customers must be signed in to add products to their shopping carts.

## 4. Shopping Cart

After signing in, each customer has their own shopping cart.

Customers must be able to add products to the cart, change product quantities, and remove products from the cart. The shopping cart must be retained even after the customer signs out.

The shopping cart includes the selected products, the quantity of each product, the unit price, and the total amount.

Before an order is placed, the price and order availability of every product must be checked again. If a product's price or order availability has changed, the customer must be informed of the change before proceeding.

## 5. Order Placement and Payment

After reviewing the shopping cart, the customer can confirm the order and proceed to online payment.

Each order includes the customer's information, selected products, quantities, the price of each product at the time of ordering, the total amount, the order date, and the order status.

Once the payment process begins, the order is assigned the **Pending Payment** status.

A payment is considered successful only after its result has been validly verified. The customer's return from the payment gateway to the website does not, by itself, mean that the payment succeeded.

After successful payment, the order moves to the **Placed** status. If payment fails, the order remains unpaid, and the customer can retry payment for the same order.

Repeated order-submission requests or repeated payment-transaction callbacks must not create duplicate orders or record the same payment more than once.

## 6. Order Statuses

Orders have the following statuses:

| Status | Description |
|---|---|
| Pending Payment | The order has been created, but its payment has not yet been successfully verified. |
| Placed | Payment has been verified, and the order is ready for the manager to review. |
| Viewed | The manager has reviewed the order. |
| Ready for Pickup | The manager has obtained the ordered products, and the order is ready for in-person collection. |
| Delivered | The customer has received the products, and the manager has recorded the handover. |
| Cancelled | The manager has cancelled the order. |

After an order is placed, the manager first changes its status to **Viewed**. Once the products have been obtained, the manager changes the status to **Ready for Pickup**. After the products have actually been handed over to the customer, the manager changes the status to **Delivered**.

In the first release, only the manager can cancel an order. Payment status must be tracked separately from order status so that cancelling a paid order is not incorrectly treated as a refund.

## 7. Customer Account

Customers must be able to view their order history and the details of each order in their account area.

Each order's information includes the order number, order date, products, quantities, total amount, payment status, and current order status.

Customers may view only orders associated with their own accounts.

When an order changes to **Ready for Pickup**, the customer must be informed that they need to visit the barbershop to collect the products.

## 8. Product Collection

In the first release, products can only be collected in person at the barbershop. Postal delivery is outside the scope of this release.

Once the products are ready, the manager changes the order status to **Ready for Pickup**. The customer visits the barbershop to collect the products. After the handover has actually taken place, the manager records the order as **Delivered**.

## 9. Overall Business Flow

1. The manager creates and publishes categories and products.
2. The customer visits the store and browses the products and categories.
3. The customer signs in and adds the desired products to the shopping cart.
4. The customer reviews the shopping cart and confirms the order.
5. The order is assigned the **Pending Payment** status, and the customer is redirected to the payment gateway.
6. After successful payment is verified, the order changes to **Placed** and becomes visible in the management panel.
7. The manager reviews the order and changes its status to **Viewed**.
8. The manager obtains the ordered products and changes the status to **Ready for Pickup**.
9. The customer visits the barbershop to collect the products.
10. After handing over the products, the manager changes the order status to **Delivered**, and the customer can view the final status in their account.

If payment fails, the order remains unpaid, and the customer can retry payment.

## 10. Out of Scope

The following features are not included in the first release:

- Postal or courier delivery
- Exact inventory quantity tracking
- Discount codes and sales campaigns
- Marketplace functionality with multiple sellers
- Cash on delivery
- Customer-initiated order cancellation
- Automatic refunds

**Open item:** The refund policy for paid orders cancelled by the manager must be defined before the financial requirements are finalized.
