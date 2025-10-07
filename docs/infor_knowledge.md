# Customer Order Management Module

## Common questions
- How do I create different order types? 
- How do I make the system populate the order with customer preferences like ship method, allow or not backorder and ship from different warehouses
- How do I set up soft or hard allocation?
- How do I combine the allocate/pick/ship process in one step? 
- How do I create multiple deliveries per order? 
- How do I put order on-hold if the customer is on credit hold? 
- How does the pricing and discounts work?
- How does allocation and demand time fence work? 

## Key Configurations
 - Order types that will trigger different processes for allocation, pick and ship.
 - Customer set up with defaults for ship method, pricing discounts, accepting backorders and shipping from multiple locations. 
 - Checking customer credit status before releasing orders for allocation


## Common Mistakes
 - Users want to allocate orders that are outside the demand time fence.
 - Users want to allocate, pick and ship orders that are on-hold due to credit stop.
 - Creating multiple delivery tickets due to allocations issues.

# Purchasing and Inventory Management Module

## Common questions
- How do I print a PO? 
- How do I know what is left on a PO?
- How do I know what has been received and what has been paid by AP? 
- How do I create a PO for special items that don’t exist in the item master? 
- How do I quarantine defective items? 
- How do I return defective items?
- How do I move items between locations within a warehouse? 

## Key Configurations
 - Authority levels for PO approvals
 - Tolerance level for PO quantity and receiving quantities for a PO line to be closed
 - Vendor rebate setup
 - PO email to vendors
 - Tracking by lot
 - Blanket PO

## Common Mistakes
 - Over-receiving and under-receiving on a PO line
 - Closing a line that is partially received
 - Receiving in the wrong location
 - Receiving against the wrong PO
