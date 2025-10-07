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

## Customer Order Types
Customer order (CO) types allow customer orders to be processed and checked in the customer order flow
according to the requirements of the customer's company.
A CO type is a setting that determines the automation level of a customer order and the checks to be made
during order entry. This includes how items are allocated in inventory, how picking lists are printed and how
invoicing is initiated.
M3 Sales Management User Guide | 278
Customer Order Processing
A customer order must be entered with a CO type. The type can either be entered manually or retrieved
automatically from the customer. After a customer order is entered, its CO type cannot be changed. However,
it is possible to change the CO type's default values after the order is entered. See section Field Control later
on in this document.
Before you start
To use this supporting function, the following prerequisites must be met:
If multiple unit coordination (MUC) is used, the invoice number series should be defined for each division in
program 'Internal Invoice Series. Open' (MFS165).
No checks can be made to see whether an invoice number series exists during CO type entry in a MUC
environment. Therefore, the ID of a specific series (for example, series A) must be entered for all divisions that
will use a CO type referring to series A.
The number range can vary, so that a range for series A can be 100000-199999 for division XXX and
700000-799999 for division YYY.
• Order number series and invoice number series are specified in program 'Number Series. Open' (CRS165).
• Standard documents to be used are specified in program 'Standard Document. Open' (CRS027).
Follow these steps
1 Customer order type entry
When entering a CO type, the customer order category and next manual function must be defined. The
selected combination regulates how the parameter values are proposed on the E-K panels, and which
fields and options may be changed for the order type.
• Customer order category
The customer order category indicates the type of order - for example, normal order, credit order,
or adjustment order - for which the CO type is used.
• Next manual function
The next manual function regulates the activities performed automatically after an order is entered.
2 Parameters entry
The panels in 'CO Type. Open' (OIS010) contain parameters regulating how a customer order is processed
during entry in 'Customer Order. Open' (OIS100) and later in the customer order flow.
A series of checks for the customer order type can be activated and then implemented when a customer
order is entered. When M3 is installed, each check should be taken into account. Checks that should not
be used for a CO type should be deactivated. This is done to make order processing as easy as possible
and to increase M3 performance.
General parameters for the CO type are set on the E panel. These regulate the overall settings for customer
orders entered with the CO type. The parameters indicate whether the customer order may be preliminary,
whether order messages are used.
• Parameters - Customer order header
Parameters for the customer order header are set on the F panel. These regulate the checks made
in the customer order header. The parameters indicate on which levels the credit check is made.
This CO type can then be proposed as the default CO type for the orders entered.
M3 Sales Management User Guide | 279
Customer Order Processing
• Parameters - Materials management
Parameters regarding materials management are set on the J panel. The panel contains settings for
allocation and a dispatch policy. The dispatch policy defined in 'Dispatch Policy. Open' (MWS010)
defines how to manage the dispatch.
• Parameters - Invoicing and Statistics
Parameters for invoicing and statistics are set on the K panel. The parameters indicate whether
advance invoicing is allowed, the auto level for invoicing, the acceptable deviation between ordered
quantity and delivered quantity.
• Parameters - Customer order lines I, II, and III
Parameters for customer order lines are set on the G, H, and I panels. These regulate the checks
made during entry of customer order lines. There are, for example, parameters that indicate the
search order for the item ID, whether a reasonability check is made, whether negative quantities are
allowed, whether bonus or commission is generated, the information affecting pricing.
3 Connect documents
One or more documents per document group are connected to each CO type in program 'CO Connect Documents' (OIS011). The program is accessed by related option 11='Documents' in 'CO Type.
Type.
Open' (OIS010).
Document groups regulate the documents used for a customer order entered with the CO type. To connect
documents to a customer order, the ordering customer must be connected to the same document group
as the CO type.
4 Enter order charges
Order charges can be entered for each CO type in program 'CO Type. Connect Order Charges' (OIS013).
The program is accessed by related option 13='Charges' in 'CO Type. Open' (OIS010).
Charges can also be retrieved from program 'CO Charge. Open' (OIS030) and then changed for the CO
type. If the same order charge is entered both for the customer and the CO type, then the CO type charge
has priority.
The charges entered for the CO type are proposed by default during customer order entry. They can then
be changed or deleted.
Charges can be external or internal. An external charge is invoiced to the customer. An internal one is
not invoiced, but is considered a cost when calculating contribution margins for a customer order.
Charges can be entered as fixed amounts or as factors. If a factor is used, the charge is calculated as a
percent of another amount, such as a net price.
5 Define field control
The fields to be displayed during customer order entry can be determined in 'CO Type. Update Field
Selection' (OIS014). The program can be accessed by related option 14='Field control' in program 'CO
Type. Open' (OIS010).
'CO Type. Update Field Selection' (OIS014) displays the field headings for all fields used during
customer order entry. For each field, it is possible to specify whether the contents are to be displayed
and whether the contents may be changed. For many of the fields it is also possible to specify how the
default values are to be retrieved for the CO header/lines during entry.
6 Enter customer order type per customer
A CO type can be connected to a customer on 'Customer. Open' (CRS610/F)Parameters for the customer
order header are set in the F panel. These regulate the checks made in the customer order header. The
M3 Sales Management User Guide | 280
Customer Order Processing
parameters indicate: whether the customer order may be preliminary, whether bonus/commission is
generated, on which levels the credit check is made. This CO type can then be proposed as the default
CO type for the orders entered.
On the P panel in 'Customer Order. Open' (OIS100) you can specify whether the CO type is to be retrieved
from the customer file or if the CO type entered in this program is to be used.
7 Enter country specific information
Country specific CO type data are for certain countries managed and displayed through the country
specific panel X in 'CO Type. Open' (OIS010). See the country specific instruction in this document on
how to enter country specific CO type data.
Brazil-specific CO type data
This functionality must be set up for divisions that have been configured with country version BR on 'Company.
Connect Division' (MNS100/L).
Follow these steps:
1 Select F13='Settings' in (OIS010) and include panel X in the panel sequence.
Note: Panel X is automatically removed when running in a configuration not supporting country specific
CO type data.
2 Search for the specific CO type and use option 2='Change'.
3 Navigate to panel X to open 'CO Type BR. Open' (OIBR06). Specify values in the required fields and click
Next.
Note: If a CO type is copied or deleted through (OIS010), its corresponding country specific data will also be
copied or deleted.
These fields are defined in 'CO types).
type BR. Open' (OIBR06) and stored in the table XOTYPE (Customer order
Program ID/Panel
Field
The field indicates...
(OIBR06)
Invoice type
(OIBR06)
Document type
... the type of fiscal note. These
are the alternatives:
• 0 = Exit (issued) fiscal note
• 1 = Entry (received) fiscal note
... different types of documents,
such as specifications, instruc-
tions, or manuals.
Argentina-specific CO type data
This functionality must be set up for divisions that have been configured with country version AR on 'Company.
Connect Division' (MNS100/L).
Follow these steps:
1 Select F13='Settings' in (OIS010) and include panel X in the panel sequence.
Note: Panel X is automatically removed when running in a configuration not supporting country specific
CO type data.
M3 Sales Management User Guide | 281
Customer Order Processing
2 Search for the specific CO type and use option 2='Change'.
3 Navigate to panel X to open 'CO Type AR. Open' (OIAR01). Specify values in the required fields and click
Next.
Note: If a CO type is copied or deleted in (OIS010), its corresponding country specific data will also be copied
or deleted.
These fields are defined in (OIAR01) and stored in the table XARTYP (Customer order - order types AR).
Program ID/Panel
Field
The field indicates...
(OIAR01)
Invoice type
... which prefix will be used for in-
voices according to the setup of
the invoice number series on
(MFS165/E) connected to the or-
der type on (OIS010/K).
In case the system does not find
a matching prefix on (MFS165/E),
the default invoice prefix setup on
(MFS165/E) will be used.
Customer Order Type
A customer order type is the collective identity for a number of settings that regulate the processing of
customer orders throughout the customer order flow.
The customer order type is specified for the customer order during entry. The customer order is then connected
to a line of values which regulate whether a credit check or reasonability check are activated, whether the
order is bonus or commission generating, and whether the order can be over-shipped.
A customer order type is specified for every customer registered in the customer file. It is then entered by
default during customer order entry, but can be changed.
Customer order types are entered in 'CO Types. Open' (OIS010).

## Common Mistakes
 - Users want to allocate orders that are outside the demand time fence.
 - Users want to allocate, pick and ship orders that are on-hold due to credit stop.
 - Creating multiple delivery tickets due to allocations issues.

# Purchasing and Inventory Management Module
## Setting up a supplier rebate agreement model
1 Define a supplier rebate agreement model:
a Supplier rebate agreement models are maintained in 'Supplier Rebate Agreement Model. Open'
(PPS470).
b The supplier rebate agreement model in the purchase transactions (Planned Purchase order, Purchase
Order Batch, Firm Purchase Order) are inherited either from the ‘Supplier Purchase & Finance’
M3 Procurement User Guide | 486
Supplier Rebate for Purchasing
(CRS624), ‘Supplier Open/Division’ (MFS620), or manually specified or changed during order
creation.
c As a default, the supplier rebate agreement model in the header is inherited into the line but manual
override is applicable. This occurs for a Batch Purchase Order, Planned Purchase Order, and Firm
Purchase Order. The agreement model on the purchase order header is editable until a purchase
order line is added, at this stage, the agreement model of the order header is write-protected.
2 The supplier rebate agreement model contains sequences that you can define in Suppl Rebate Agr -
Model Lines. Open' (PPS471). Specify these items to define the supplier rebate agreement model lines:
• Supplier Rebate Agreement Group, defined in ‘Supplier Rebate Agreement - Group. Open’ in
(PPS482).
• Supplier Rebate Agreement Table, defined in ‘Supplier Rebate Agreement Table. Open’ in (PPS473),
holds the selection matrix that identifies the supplier rebate agreement number valid for a given
criterion. This is connected to the model line to indicate the list of agreements to evaluate.
• Accruals date type indicates the date to use when evaluating the purchase transaction against the
agreement. The Supplier Invoice date is currently the only Accruals date available.
• Accruals Management indicates how the rebate accruals are managed. The current alternative is
process by batch using (PPS477).
Specifying a Dependent sequence is optional. Specify the sequence number in the supplier rebate
agreement model to which the model line is dependent on. This means its rebate amount is computed
as a portion of the rebate amount of the base model line.
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
