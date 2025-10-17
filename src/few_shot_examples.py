"""
Few-shot examples for ERP Assistant
Real examples of high-quality responses to guide the LLM
"""

CONFIGURATION_EXAMPLES = [
    {
        'question': 'How do I configure a customer order type?',
        'answer': '''**Program:** OIS010 - Customer Order Type. Open

**Navigation:** Main Menu > Order Entry > Settings > Order Type

**Configuration Steps:**

1. **Access OIS010:**
   - Navigate to Main Menu > Customer Orders > Settings
   - Select "Order Type" or enter OIS010 directly

2. **Create New Order Type (F3=New):**
   - Press F3 to create new record
   - Enter **ORTP (Order Type):** 3-character code (e.g., "STD", "RSH", "EXP")

3. **Configure Required Fields:**
   - **Description:** Full name for the order type
   - **ORCA (Order Category):**
     - 1 = Normal order
     - 2 = Quotation
     - 3 = Blanket order
   - **ORSL (Order Status):** Start status (typically "15" for entry)
   - **WHLO (Warehouse):** Default warehouse or leave blank for customer default

4. **Allocation Settings:**
   - **ALMT (Allocation Method):**
     - 1 = Manual allocation only
     - 2 = Automatic allocation (recommended for standard orders)
     - 3 = Soft allocation
   - **ALPA (Show Allocation Panel):** Y/N

5. **Delivery & Invoice Settings:**
   - **MODL (Delivery Method):** Default delivery method
   - **Consolidate Deliveries:** Y/N
   - **Invoice Method:** Per line, per delivery, or consolidated

6. **Save (Enter):**
   - Press Enter to save the order type
   - System validates and confirms creation

**Testing:**
1. Go to OIS100 - Customer Order. Open
2. Create new order with F3
3. Enter your new order type in ORTP field
4. Verify all defaults populate correctly (warehouse, allocation method, etc.)
5. Test allocation behavior matches your ALMT setting

**Common Mistakes:**
- Forgetting to set ALMT causes orders to require manual allocation
- Using wrong ORCA value (category 2 for quotations doesn't create deliveries)
- Not testing with actual customer order before going live
- Missing delivery method setup causes issues at shipping

**Related Programs:**
- OIS015: Order type charges and discounts
- OIS020: Order type text templates
- MMS002: Warehouse validation'''
    },
    
    {
        'question': 'How do I configure a purchase order type?',
        'answer': '''**Program:** PPS095 - PO Order Type. Open

**Navigation:** Main Menu > Purchasing > Settings > PO Type

**Configuration Steps:**

1. **Access PPS095:**
   - Navigate to Main Menu > Purchasing > Settings
   - Select "PO Order Type" or enter PPS095 directly

2. **Create New Type (Option 1=Create):**
   - Enter blank sorting order, press Enter
   - Select Option 1=Create for new record
   - Enter **ORTP (Order Type):** 3-character code (e.g., "STD", "BLK", "SRV")

3. **Configure Basic Settings:**
   - **Name:** Full description of order type
   - **SUNO (Supplier Category):** Leave blank for all or specify category
   - **Start Status:** Typically "05" (Entry) or "10" (Released)
   
4. **Approval Configuration:**
   - **Approval Required:** Y/N
   - If Y, set **Authority Level Required**
   - Configure approval routing in PPS200 (PO settings per supplier)
   - Set dollar thresholds in CRS610 (User Authority)

5. **Document Settings:**
   - **Print PO:** Y/N automatic printing
   - **Document Code:** For PO print format
   - **Email Setup:** Configure for automatic PO transmission

6. **Advanced Settings:**
   - **Order Type Category:** Standard, Blanket, Schedule, etc.
   - **GL String Control:** How GL accounts default
   - **Receipt Required:** Y/N for automatic receipts

7. **Save (Enter):**
   - Press Enter to save
   - System confirms creation

**Testing:**
1. Go to PPS200 - Supplier. Purchase Order. Open
2. Create new PO with F3
3. Enter your new order type
4. If approval required, verify workflow triggers correctly
5. Test receipt process in PPS300 if receipts enabled
6. Verify printing/email works if configured

**Common Order Types:**
- **STD (Standard):** Regular purchases, approval required, full receipts
- **BLK (Blanket):** Long-term agreements, release POs reference blanket
- **SRV (Service):** Services/consulting, different GL handling
- **EXP (Expedite):** Rush orders, higher approval authority, priority processing

**Common Mistakes:**
- Setting approval but not configuring authority levels in CRS610
- Wrong start status (05 vs 10) affects when PO transmits to supplier
- Not testing approval workflow timeout/escalation
- Missing backup approvers causes stuck POs

**Related Programs:**
- CRS610: User authority levels (dollar thresholds)
- PPS200: Supplier PO settings
- PPS001: Supplier master (approval workflow per supplier)
- PPS300: PO Receipt (test receiving)'''
    },
    {
        'question': 'How do I set up a new customer?',
        'answer': '''**Primary Program:** CRS610 - Customer. Open

**Prerequisites:**
- Company division structure defined
- Payment terms configured (CRS010)
- Currency codes active
- Credit management policies established

---

**Step-by-Step Customer Setup:**

**1. Create Basic Customer Record (CRS610)**

**Navigation:** Main Menu > Customer Relations > Customer > Open

**Panel A: Basic Information**
- **CUNO (Customer Number):** Enter unique ID or leave blank for auto-number
- **CUNM (Customer Name):** Full legal name
- **CUA1-CUA4 (Address):** Complete address lines
- **TOWN (City)**, **ECAR (State)**, **PONO (Postal Code)**
- **CSCD (Country Code):** 2-character ISO code

**Panel B: Communication**
- **PHNO (Phone Number)**
- **TFNO (Fax)**, **MAIL (Email)**
- **YREF (Your Reference):** Primary contact name

**2. Financial Settings (CRS610, Panel E)**

**Credit Management:**
- **CRLM (Credit Limit):** Maximum exposure allowed
- **BLCD (Credit Block):** 
  - 0 = No block
  - 1 = Warning only
  - 2 = Hard block
- **PYCD (Payment Terms):** From CRS010 (e.g., NET30, NET60)
- **CUCD (Currency):** Customer's billing currency

**Payment Information:**
- **VRNO (VAT Number):** Tax registration number
- **TEPY (Payment Method):** Check, Wire, ACH, etc.
- **BKID (Bank Account):** If ACH/wire payments

**3. Order Entry Defaults (CRS610, Panel F)**

**Shipping & Delivery:**
- **WHLO (Warehouse):** Default fulfillment warehouse
- **MODL (Delivery Method):** Shipping method
- **TEDL (Delivery Terms):** FOB, CIF, etc.
- **FWHL (Forward Agent):** Freight forwarder if applicable

**Pricing:**
- **PRRF (Price List):** Link to customer's price list (from OIS002)
- **CUCD (Currency):** Must match price list currency
- **DISY (Discount %):** Customer-level discount if applicable

**Order Processing:**
- **ORTY (Order Type):** Default order type from OIS010
- **SMCD (Salesperson):** Assign sales rep
- **CUOR (Customer Order Required):** Y/N for PO requirement

**4. Invoice & Statement Settings (CRS610, Panel G)**

**Invoicing:**
- **IVRF (Invoice Reference):** Customer's AP contact
- **DUDT (Due Date Basis):** Invoice date, delivery date, etc.
- **INVM (Invoice Method):** Per line, per delivery, consolidated

**Statements:**
- **STMT (Statement):** Y/N for monthly statements
- **Language Code:** For documents

**5. Create Ship-To Addresses (CRS624)**

**If customer has multiple delivery locations:**
- Go to CRS624 - Customer Address. Open
- Create ADRT=1 (Ship-To) addresses
- Link to main customer
- Each can have unique warehouse, delivery method

**6. Connect to Price List (OIS002)**

**Program:** OIS002 - Price List. Connect Customer

**Steps:**
- Enter CUNO (Customer Number)
- Enter PRRF (Price List)
- Set Start Date and End Date
- Priority if multiple lists (1=highest)

**Without this, customer orders won't get pricing!**

---

**Testing the Setup:**

**Test 1: Credit Check**
1. Go to CRS677 - Customer Credit Information
2. Enter customer number
3. Verify credit limit, current balance appear correctly

**Test 2: Create Order**
1. Go to OIS100 - Customer Order. Open
2. F3 to create new order
3. Enter new customer number
4. Verify all defaults populate:
   - Warehouse (WHLO)
   - Order type (ORTY)
   - Delivery method (MODL)
   - Payment terms (PYCD)
5. Add an order line
6. Verify pricing populates from price list

**Test 3: Invoice Generation**
1. Complete the test order through shipping
2. Generate invoice in OIS350
3. Verify invoice format correct
4. Check GL postings in GLS120

---

**Common Mistakes:**

❌ **Not connecting to price list (OIS002)**
   → Orders have no pricing, manual entry required

❌ **Mismatched currencies**
   → Customer currency ≠ price list currency = no pricing

❌ **No payment terms set**
   → Invoices have no due date, causes AR issues

❌ **Missing warehouse default**
   → Every order requires manual warehouse selection

❌ **Credit limit = 0**
   → Customer blocked from ordering

❌ **Wrong delivery terms**
   → Freight costs calculated incorrectly

❌ **Not testing order creation**
   → Discover problems when real order placed

---

**Related Programs:**
- CRS610: Customer master (main setup)
- CRS624: Ship-to addresses
- OIS002: Price list connection
- CRS010: Payment terms configuration
- CRS677: Credit information display
- OIS100: Test order creation
- GLS120: GL review for testing'''
    },
]

TROUBLESHOOTING_EXAMPLES = [
    {
        'question': 'Why can\'t I allocate an order line?',
        'answer': '''**Diagnostic Steps:**

**1. Check Order Line Status (OIS100):**
- Open OIS100 - Customer Order. Open
- Find your order number
- Check **ORST (Order Status)** field:
  - Must be status **20 (Released)** or higher to allocate
  - If status 15 or lower, release the order first
  - If on credit hold, resolve hold before allocation

**2. Verify Inventory Availability (MMS060):**
- Go to MMS060 - Item. Display On Hand Balance
- Enter **ITNO (Item Number)** from order line
- Enter **WHLO (Warehouse)** 
- Check **Available Balance:**
  - Must have positive available quantity
  - Available = On Hand - Allocated - Reserved
  - If zero/negative, no stock to allocate

**3. Check Item Setup (MMS001):**
- Go to MMS001 - Item. Open
- Select Panel E14 (Item/Warehouse)
- Verify **STQT (Stocked):** Must be "1" (Stocked item)
- Check **WHLO (Warehouse):** Item must be set up for this warehouse
- If not stocked or warehouse missing, add warehouse setup

**4. Check Allocation Settings (OIS010):**
- Verify order type allows allocation
- Go to OIS010 - Customer Order Type. Open
- Check **ALMT (Allocation Method):**
  - 0 or 1 = Manual only (OK for manual allocation)
  - 2 = Automatic (should allocate on release)
- If method wrong, may need to change order type

**5. Verify Demand Time Fence (MMS001):**
- Back in MMS001, Panel E14
- Check **DTFH (Demand Time Fence Hours)**
- Order delivery date must be WITHIN DTF to allocate against on-hand
- If outside DTF, order competes with forecasted demand
- Either bring order date in OR override DTF with authority

**6. Check for Soft Allocations:**
- In OIS100, check if line shows soft allocation
- Soft allocations don't reserve inventory
- Convert to hard allocation: Option 41=Allocate > change type

**7. Customer Credit Status (OCI100):**
- Verify customer isn't on credit hold
- Credit hold prevents allocation in some configurations
- Check order header for credit hold indicators

**Most Common Causes:**
1. ❌ Order status too low (not released) - **FIX:** Release order to status 20
2. ❌ No inventory available - **FIX:** Purchase more or reallocate from other orders
3. ❌ Item not set up for warehouse - **FIX:** Add warehouse in MMS001, Panel E14
4. ❌ Outside demand time fence - **FIX:** Move delivery date or get override authority
5. ❌ Wrong order type (no allocation allowed) - **FIX:** Change order type or settings

**Resolution Steps:**
1. Identify which condition above is failing
2. Fix the root cause (add inventory, release order, update item setup, etc.)
3. Retry allocation: In OIS100, Option 41=Allocate or F14
4. If still fails, check MNS205 for system messages/errors

**Prevention:**
- Set up items completely before taking orders
- Configure automatic allocation on order types (ALMT=2)
- Monitor inventory levels vs. demand
- Regular DTF reviews to ensure settings make sense'''
    },
    
    {
        'question': 'Why doesn\'t customer pricing populate when I add an order line?',
        'answer': '''**Diagnostic Steps:**

**1. Check Price List Assignment (OIS002/CRS610):**
- Go to OIS002 - Price List. Connect Customer
- Enter **CUNO (Customer Number)**
- Verify customer is connected to a price list
- Check **PRRF (Price List)** and **Start Date/End Date**
- If not connected, link customer to appropriate price list

**2. Verify Price List Has Item Pricing (OIS017):**
- Go to OIS017 - Price List. Open Line
- Enter the **PRRF (Price List)** from step 1
- Enter **ITNO (Item Number)** you're ordering
- Check if price exists and dates are valid
- If no price, add pricing in OIS017

**3. Check Customer Order Type Pricing (OIS010):**
- Some order types override pricing rules
- Go to OIS010 - Customer Order Type
- Verify pricing method for the order type
- Check if order type forces zero pricing or special rules

**4. Verify Currency Match (CRS610):**
- Go to CRS610 - Customer. Open
- Check **CUCD (Currency Code)** on customer
- Price list currency must match customer currency
- If mismatch, either update customer or use correct price list

**5. Check Agreement Pricing (OIS035):**
- Customer may have agreement pricing that overrides lists
- Go to OIS035 - Customer Agreement Price
- Search for customer + item combination
- Agreement pricing takes precedence over price lists
- Verify dates are valid if agreement exists

**6. Item Sales Price Setup (MMS002):**
- Go to MMS002 - Item. Open Warehouse
- Panel E3 (Sales Price)
- Check **SAPR (Sales Price):** Base price if no list pricing
- This is fallback if price list lookup fails

**7. Price Break Quantities (OIS017):**
- In OIS017, check if quantity breaks configured
- Order quantity may be below minimum for list pricing
- Increase order quantity or adjust price breaks

**Price Lookup Hierarchy (M3 checks in this order):**
1. **Customer Agreement Price** (OIS035) - Highest priority
2. **Customer/Item Price List** (OIS017 via OIS002)
3. **Customer Group Price List** (if customer in group)
4. **Base Sales Price** (MMS002) - Lowest priority
5. **Zero/Manual** - If none found

**Most Common Causes:**
1. ❌ Customer not linked to price list - **FIX:** Connect in OIS002
2. ❌ Item not in price list - **FIX:** Add pricing in OIS017
3. ❌ Price list dates expired - **FIX:** Update date range in OIS017
4. ❌ Currency mismatch - **FIX:** Ensure customer currency = price list currency
5. ❌ Order quantity below minimum - **FIX:** Increase quantity or adjust breaks

**Resolution Steps:**
1. Follow diagnostic steps above to find gap
2. Add missing pricing or fix configuration
3. Return to OIS100 and re-enter order line
4. Or use Option 2=Change on existing line to trigger price recalculation
5. Verify price populates correctly

**Manual Override (If Needed):**
- In OIS100, you can manually enter **SAPR (Sales Price)**
- Use this if pricing setup cannot be done immediately
- Document manual overrides for audit purposes

**Prevention:**
- Maintain price lists proactively before launching items
- Set up new customers with correct price list links
- Regular price list audits to catch expired dates
- Use customer groups for easier price list management'''
    },
    
    {
        'question': 'Pick ticket is splitting into many documents, what is wrong?',
        'answer': '''**Root Cause Analysis:**

Pick tickets split when delivery consolidation rules are not met. M3 creates separate deliveries (and pick tickets) when it detects differences in key fields.

**Common Split Triggers:**

**1. Different Delivery Dates:**
- **Program:** OIS100 - Customer Order. Open
- Check **DWDZ (Requested Delivery Date)** on each line
- Lines with different dates create separate deliveries
- **FIX:** Standardize delivery dates OR accept multiple deliveries

**2. Different Ship-To Addresses:**
- Check **ADID (Address ID)** or **CUNM (Consignee)** 
- Different ship-to = separate deliveries
- **FIX:** Ensure all lines have same ship-to address

**3. Different Warehouses:**
- Check **WHLO (Warehouse)** on order lines
- M3 creates one delivery per warehouse
- **FIX:** Consolidate to single warehouse OR accept split by design

**4. Different Delivery Terms:**
- Check **TEDL (Delivery Terms)** in OIS100
- Different terms (FOB, CIF, etc.) trigger splits
- **FIX:** Use consistent delivery terms per order

**5. Order Type Consolidation Settings:**
- **Program:** OIS010 - Customer Order Type. Open
- Check consolidation settings for the order type
- Some order types configured to NOT consolidate
- **FIX:** Update order type settings or use different type

**6. Routing/Carrier Differences:**
- Check **MODL (Delivery Method)** and **ROUT (Route)**
- Different routes/methods = separate deliveries
- **FIX:** Use same routing for all lines

**7. Manual Delivery Split by User:**
- Check if someone manually split deliveries in MWS410
- Review **DLIX (Delivery Number)** on lines
- **FIX:** Recombine deliveries if possible (before picking)

**Diagnostic Steps:**

**Step 1: Review Delivery Numbers (MWS410)**
- Go to MWS410 - Delivery. Display
- Enter order number
- Count how many DLIX (Delivery Numbers) exist
- This shows actual delivery split

**Step 2: Compare Order Lines (OIS100)**
- In OIS100, display all lines
- Use Option 5=Display to see detailed line info
- Create table comparing key fields across lines:

| Line | DWDZ | WHLO | ADID | TEDL | MODL |
|------|------|------|------|------|------|
| 1    | ?    | ?    | ?    | ?    | ?    |
| 2    | ?    | ?    | ?    | ?    | ?    |

- Identify which field(s) differ

**Step 3: Check Consolidation Rules (OIS010)**
- Verify order type allows consolidation
- Check customer-specific consolidation settings

**Resolution Options:**

**Option A: Fix Before Allocation (Preferred)**
1. In OIS100, update order lines to have matching:
   - Delivery dates (DWDZ)
   - Warehouse (WHLO)  
   - Ship-to (ADID)
   - Delivery terms (TEDL)
2. Delete existing deliveries if already created
3. Re-allocate/release order
4. New consolidated delivery will be created

**Option B: Combine Existing Deliveries (Before Picking)**
1. Go to MWS410 - Delivery. Combine
2. Select deliveries to merge
3. Can only combine if:
   - Not yet picked
   - Same warehouse
   - Same ship-to address
   - No shipment created

**Option C: Accept Multiple Deliveries (If Necessary)**
- Sometimes splits are required by business rules
- Example: Different ship dates legitimately need separate shipments
- Accept multiple pick tickets as correct behavior

**Prevention:**

1. **Standardize Order Entry:**
   - Train CSRs on consolidation rules
   - Default delivery date to single date per order
   - Use templates for consistent warehouse/routing

2. **Order Type Configuration:**
   - Set up order types with consolidation enabled
   - Configure smart defaults (warehouse, routing, terms)

3. **Customer Master Defaults:**
   - Set up customers with consistent ship-to, routing, terms
   - Reduces likelihood of differences at order entry

4. **System Validation:**
   - Consider custom validation to warn when creating splits
   - Alert CSR if adding line with different key fields

**Related Programs:**
- MWS410: Delivery management and combination
- OIS100: Order line details
- OIS010: Order type consolidation settings
- CRS610: Customer master defaults'''
    },
    {
        'question': 'Why can\'t I release a customer order?',
        'answer': '''**Diagnostic Process:**

Customer orders must pass multiple validations before releasing from status 15 (Entry) to 20 (Released). Follow these checks in order:

---

**1. Check Order Status (OIS100)**

**Program:** OIS100 - Customer Order. Open

**Current Status Check:**
- Look at **ORST (Order Status)** field
- If already 20+ → Order IS released (check if looking at wrong order)
- If 15 or below → Continue diagnostics
- If 88/99 → Order cancelled, cannot release

**Status meanings:**
- 05 = Preliminary  
- 15 = Order entry
- 20 = Released (target)
- 33 = Allocated
- 66 = Delivered

---

**2. Credit Hold Check (Most Common Issue)**

**Check A: Order Header (OIS100)**
- Look for **CUCD (Credit Hold)** indicator
- If "1" or "2" → Order on credit hold

**Check B: Customer Credit Status (CRS677)**
- Go to CRS677 - Customer Credit Information
- Enter customer number
- Review:
  - **Credit Limit vs Current Balance**
  - **Overdue Invoices**
  - **Credit Block Code** (from CRS610)
  
**Credit Hold Types:**
- **Soft Hold (Warning):** Can be overridden with authority
- **Hard Hold (Block):** Must resolve credit issue first

**Resolution for Credit Hold:**
1. If customer legitimately over limit:
   - Customer must pay down balance
   - OR get approval to increase limit in CRS610
2. If old invoices causing issue:
   - Process payments in ARS100
   - Update credit status
3. If hold is error:
   - Override in OIS100 with proper authority
   - Document reason for override

---

**3. Incomplete Order Line Data**

**Check in OIS100 - Order Lines:**

**Required Fields per Line:**
- **ITNO (Item Number):** Must be valid, active item
- **ORQT (Order Quantity):** Must be > 0
- **WHLO (Warehouse):** Must be specified
- **DWDZ (Delivery Date):** Must be valid date
- **SAPR (Sales Price):** Must have price (unless $0 items allowed)

**Common Line Issues:**
- ❌ Item not set up for warehouse → Add in MMS001 Panel E14
- ❌ Negative quantity → Correct to positive
- ❌ No price and pricing required → Fix pricing setup
- ❌ Past delivery date → Update to future date

**How to Check:**
- Use Option 5=Display on each line
- Look for error messages in message line
- Check MNS205 for detailed error logs

---

**4. Missing Required Order Header Data**

**Check Order Header Fields:**
- **CUNO (Customer Number):** Must be valid
- **ORTP (Order Type):** Must be configured in OIS010
- **CUOR (Customer PO):** May be required by order type/customer
- **PYNO (Payment Terms):** Required for invoicing
- **MODL (Delivery Method):** Required for shipping

**Validation:**
- Each field should have value (not blank if required)
- Values must exist in master files
- Check order type requirements in OIS010

---

**5. Authorization/Authority Issues**

**User Authority Check:**
- Some order types require release approval
- Check CRS610 - User Authority
- User may not have authority level to release this order
  
**Order Type Restrictions:**
- Check OIS010 - Order Type settings
- Some types require approval workflow
- May need higher authority for dollar amount

**Resolution:**
- Have authorized user release order
- OR request temporary authority increase
- OR change order type if appropriate

---

**6. Inventory/Allocation Blocks**

**While not preventing release, may want to check:**
- Item availability (MMS060)
- Allocation settings (OIS010)
- Demand time fence issues

**These typically don't block release, but block allocation after release.**

---

**7. Configuration/System Issues**

**Order Type Configuration:**
- Go to OIS010 - Customer Order Type
- Verify order type is active
- Check if special workflow configured
- Review start status settings

**Customer Configuration:**
- Verify customer active (not blocked)
- Check customer order block codes
- Review customer status in CRS610

---

**Step-by-Step Resolution Process:**

**Step 1: Identify the Block**
1. Open order in OIS100
2. Try to change status to 20 (Option 2=Change, ORST=20)
3. Note specific error message
4. Check MNS205 for detailed error

**Step 2: Address Root Cause**
- Credit hold → Resolve credit
- Missing data → Complete required fields  
- Authority → Get proper approval
- Item issue → Fix item/warehouse setup

**Step 3: Retry Release**
1. After fixing issue, return to OIS100
2. Option 2=Change
3. Change ORST to 20
4. Press Enter
5. Verify status changes to 20

**Step 4: Verify Order Flows**
- Check if allocation triggered (ORST=33)
- Verify downstream processes work
- Monitor for additional issues

---

**Common Causes by Frequency:**

1. **Credit hold (40%)** → Check CRS677, resolve credit
2. **Missing price (25%)** → Fix OIS002/OIS017 pricing
3. **Incomplete line data (15%)** → Add missing warehouse/dates
4. **User authority (10%)** → Get approval or higher auth
5. **Item setup issue (5%)** → Fix MMS001 configuration
6. **Other config (5%)** → Review order type, customer setup

---

**Prevention Strategies:**

**At Order Entry:**
- Use order templates with defaults
- Configure automatic validations
- Set up customer masters completely
- Maintain price lists proactively

**System Configuration:**
- Set sensible credit limits
- Configure warning messages for issues
- Use order types appropriately
- Train users on requirements

**Monitoring:**
- Regular credit review meetings
- Dashboard for stuck orders
- Alert for orders >24hrs in status 15

---

**Related Programs:**
- OIS100: Order management
- CRS677: Credit information
- CRS610: Customer master and authority
- OIS010: Order type configuration
- MNS205: Error message log
- MMS001: Item master (if item issues)
- ARS100: Payment processing (if credit hold)'''
    },
]

BEST_PRACTICES_EXAMPLES = [
    {
        'question': 'Should we use soft or hard allocation for customer orders?',
        'answer': '''**Recommendation: Hard Allocation for Most Scenarios**

**Hard Allocation (Recommended Default):**

**When to Use:**
- Standard customer orders
- Made-to-order items
- High-value products
- Tight inventory situations
- When inventory accuracy is critical

**Advantages:**
✓ Reserves inventory - prevents double-booking
✓ Clear visibility of committed vs. available
✓ Protects against overselling
✓ Works well with automatic allocation
✓ Better inventory control and planning

**Configuration:**
- Order type ALMT (Allocation Method) = 2 (Automatic hard allocation)
- Set in OIS010 - Customer Order Type

**Disadvantages:**
✗ Ties up inventory even if order might change
✗ Requires de-allocation if order cancelled
✗ Less flexibility for last-minute changes

---

**Soft Allocation:**

**When to Use:**
- Quotations and estimates
- Long lead time orders (weeks/months out)
- When inventory is plentiful
- Planning/forecasting scenarios
- Internal transfers or non-critical orders

**Advantages:**
✓ More flexible - doesn't reserve inventory
✓ Good for long-term planning
✓ Easy to adjust without de-allocation
✓ Useful for "what-if" scenarios

**Configuration:**
- Order type ALMT = 3 (Soft allocation)
- Or manual soft allocation on order lines

**Disadvantages:**
✗ No inventory protection - can be oversold
✗ Requires manual conversion to hard when shipping
✗ Less accurate available inventory view
✗ Risk of allocation failure at conversion time

---

**Hybrid Approach (Best Practice):**

**Use different order types for different scenarios:**

1. **Standard orders (ORTP=STD):**
   - Hard allocation, automatic (ALMT=2)
   - 90% of orders

2. **Quotes (ORTP=QUO):**
   - Soft allocation (ALMT=3)
   - Convert to STD when confirmed

3. **Future orders (ORTP=FUT):**
   - Soft allocation for orders >30 days out
   - Auto-convert to hard 7 days before ship date

4. **Backorders:**
   - Start soft (no inventory available)
   - Convert to hard when inventory received

---

**Implementation Strategy:**

**Phase 1: Set Defaults (Week 1)**
- Configure STD order type with ALMT=2 (hard, automatic)
- Train team on hard allocation benefits
- Document allocation policies

**Phase 2: Add Exceptions (Week 2-3)**
- Create QUO type for soft allocation
- Set up business rules for when to use each
- Create conversion procedures (soft → hard)

**Phase 3: Monitor & Optimize (Ongoing)**
- Track allocation failures
- Review oversell incidents
- Adjust policies based on business needs

---

**Common Mistakes to Avoid:**

❌ Using soft allocation as default "because it's easier"
   → Leads to overselling and customer dissatisfaction

❌ Never converting soft to hard
   → Discover no inventory at shipping time

❌ Using only hard allocation for everything
   → Inflexible for long-term planning

❌ Manual allocation instead of automatic hard
   → CSR errors, forgotten allocations

---

**Decision Matrix:**

| Scenario | Allocation Type | Reason |
|----------|----------------|--------|
| Standard order, stock on hand | Hard, Auto | Protect inventory |
| Quote/estimate | Soft | Not committed yet |
| Order >30 days out | Soft → Hard | Reserve later |
| Backorder, no stock | Soft → Hard | Allocate when received |
| Drop ship | N/A | No warehouse inventory |
| Consignment | Hard | Customer owns, track consumption |

---

**Key Takeaway:**

**Default to hard allocation** for committed orders. It provides better control and prevents overselling. Use soft allocation strategically for planning and uncommitted scenarios, with clear procedures to convert to hard before shipping.

**Related Configuration:**
- OIS010: Order type allocation method (ALMT)
- MMS055: Allocation priority rules
- OIS100: Manual allocation override (Option 41)
- System parameter ALUR: Allocation rules'''
    },{
        'question': 'What\'s the best way to handle backordered items?',
        'answer': '''**Recommendation: Multi-Layered Backorder Strategy**

Backorders require different handling depending on item characteristics, customer expectations, and inventory policies. Here's a comprehensive approach:

---

## **Strategy 1: Prevention (Best Approach)**

**Objective:** Minimize backorders through proactive inventory management

**Tactics:**

**1. Safety Stock Optimization**
- Calculate safety stock based on lead time variability
- Use MMS002 - Item Warehouse, Panel E1
- Set **SSQT (Safety Stock):** Based on demand variability
- Formula: Safety Stock = (Max Daily Usage × Max Lead Time) - (Avg Daily Usage × Avg Lead Time)

**2. Reorder Point Management**
- Set **REQT (Reorder Point)** to trigger before stockout
- REQT = (Avg Daily Demand × Lead Time) + Safety Stock
- Review monthly, adjust seasonally

**3. Demand Forecasting**
- Use MMS100 for forecast maintenance
- Review forecast accuracy (MMS170)
- Update forecasts based on actual demand trends
- Consider seasonal patterns

**4. Supplier Reliability Programs**
- Track supplier on-time delivery (PPS360)
- Rate suppliers on lead time consistency
- Maintain backup suppliers for critical items
- Negotiate VMI or consignment for key items

---

## **Strategy 2: Allow Backordering (When Appropriate)**

**When to Allow Backorders:**
✓ Long-term customer relationships
✓ Custom/made-to-order items
✓ Items with predictable replenishment
✓ Customer willing to wait
✓ Competitor lead times similar

**Configuration:**

**A. Customer-Level Backorder Setting**
- **Program:** CRS610 - Customer. Open
- Panel F (Order Entry)
- **BKOD (Backorder):**
  - 1 = Allow backorders
  - 2 = No backorders (substitute or cancel)
  - 3 = Partial shipment allowed

**B. Item-Level Backorder Control**
- **Program:** MMS001 - Item. Open
- Panel E14 (Item/Warehouse)
- **BKOD (Backorder Indicator):** Override customer setting
- Use for items that should NEVER backorder (perishables, etc.)

**C. Order Type Backorder Behavior**
- **Program:** OIS010 - Customer Order Type
- Configure backorder handling per order type
- Rush orders → No backorders
- Standard orders → Allow backorders

---

## **Strategy 3: Active Backorder Management**

**Monitor Backorders Daily:**

**Program:** OIS281 - Customer Order Line. Display Backorder

**Process:**
1. Review all backorder lines daily
2. Check expected receipt dates
3. Contact customers proactively with ETAs
4. Prioritize by customer importance

**Automatic Allocation from Receipts:**

**Configuration:**
- Set up automatic backorder allocation
- When inventory received, system auto-allocates to backorders
- Priority based on:
  - Order date (FIFO)
  - Customer priority code
  - Promised delivery date

**Program Flow:**
1. PO received in PPS300
2. Inventory updated in MMS100
3. System checks backorders (OIS281)
4. Auto-allocation runs
5. Customer notified (optional workflow)

---

## **Strategy 4: Communication & Customer Service**

**Proactive Communication:**

**At Order Entry:**
- If item backordered, inform customer immediately
- Provide ETA based on next expected receipt
- Offer alternatives if available
- Document in order notes (OIS100)

**During Backorder Period:**
- Weekly updates if backorder >1 week
- Immediate notification when item received
- Expedite options if customer willing to pay

**Automation:**
- Set up email alerts when items allocated
- Dashboard for CSRs showing backorder status
- Integration with CRM for customer communication

---

## **Strategy 5: Alternative Fulfillment Options**

**Option A: Substitute Items**
- Maintain substitution rules in MMS001
- Offer higher-value substitute at same price
- Get customer approval for substitution
- System: Use item substitution in OIS100

**Option B: Partial Shipments**
- Ship available quantity immediately
- Backorder remaining quantity
- Configure in order type (OIS010)
- Customer must allow partial shipments (CRS610)

**Option C: Cross-Warehouse Fulfillment**
- Check other warehouse availability (MMS060)
- Transfer stock if economically viable
- Use MMS100 for transfers
- Update order warehouse in OIS100

**Option D: Drop Shipment**
- Purchase from supplier, ship direct to customer
- Use drop ship order type
- Customer charged full price
- Avoid carrying inventory

---

## **Strategy 6: Prioritization Rules**

**When inventory limited, prioritize allocation:**

**Priority Factors:**
1. **Customer tier** (A/B/C classification)
2. **Order date** (FIFO typically)
3. **Promised ship date**
4. **Order value**
5. **Product margin**
6. **Contract obligations** (blanket POs)

**Configuration:**
- Set up in MMS055 - Allocation Priority
- Define priority codes per customer (CRS610)
- System respects priority during allocation
- Manual override available for exceptions

---

## **Implementation Roadmap**

**Phase 1: Baseline (Week 1-2)**
- Identify current backorder rate
- Analyze root causes (supplier, forecast, safety stock)
- Set KPI targets (backorder rate <2%)

**Phase 2: Configuration (Week 3-4)**
- Configure customer backorder settings (CRS610)
- Set item backorder controls (MMS001)
- Define order type behaviors (OIS010)
- Set up automatic allocation

**Phase 3: Process (Week 5-6)**
- Train CSRs on backorder communication
- Implement daily backorder review meeting
- Create escalation procedures
- Document standard responses

**Phase 4: Optimization (Ongoing)**
- Review safety stock monthly
- Adjust reorder points seasonally
- Track backorder metrics
- Supplier performance reviews

---

## **Key Metrics to Track**

**Backorder KPIs:**
- **Backorder Rate:** (Backordered Lines / Total Lines) × 100
- **Backorder Age:** Days in backorder status
- **Fill Rate:** (Filled Lines / Total Lines) × 100
- **Perfect Order Rate:** Orders shipped complete on time

**Targets:**
- Backorder Rate: <2%
- Avg Backorder Age: <7 days
- Fill Rate: >98%
- Perfect Order Rate: >95%

---

## **Common Mistakes to Avoid**

❌ **"We'll just stock more of everything"**
   → Ties up cash, increases obsolescence risk

❌ **No communication to customer**
   → Customer discovers backorder at expected delivery time

❌ **Treating all backorders equally**
   → Rush orders get same treatment as standard

❌ **Manual backorder allocation**
   → Errors, delays, priority issues

❌ **No root cause analysis**
   → Keep getting same items backordered repeatedly

❌ **Over-promising unrealistic dates**
   → Better to under-promise, over-deliver

---

## **Decision Matrix**

| Item Type | Strategy | Backorder Policy | Priority |
|-----------|----------|------------------|----------|
| High volume, predictable | Prevention | Allow if <7 days | FIFO |
| Custom/MTO | Allow backorder | Always allow | Order date |
| Low volume, erratic | Substitution | Avoid backorder | Customer tier |
| Perishable | No backorder | Never allow | N/A |
| High margin | Stock adequately | Rare backorders | Revenue |
| Commodity | Multi-warehouse | Allow, quick fill | Standard |

---

## **Bottom Line**

**Best practice is layered:**

1. **Prevent** backorders through proper inventory management (80% solution)
2. **Allow** strategic backorders where appropriate (15% of cases)
3. **Manage** backorders actively with communication (5% exceptions)
4. **Learn** from backorders to improve forecasting and stocking

**The goal isn't zero backorders** (too expensive), but **managed backorders with customer satisfaction** maintained through communication and quick resolution.

---

**Related Programs:**
- OIS281: Backorder line display
- CRS610: Customer backorder settings
- MMS001: Item backorder control
- OIS010: Order type configuration
- MMS055: Allocation priority
- MMS002: Safety stock and reorder point
- PPS360: Supplier performance'''
    },

]

def get_examples_by_type(query_type: str):
    """Get relevant examples for the query type"""
    examples_map = {
        'configuration': CONFIGURATION_EXAMPLES,
        'troubleshooting': TROUBLESHOOTING_EXAMPLES,
        'best_practices': BEST_PRACTICES_EXAMPLES,
        'general': []  # No examples for general queries
    }
    return examples_map.get(query_type, [])

def format_examples_for_prompt(examples):
    """Format examples into string for system prompt"""
    if not examples:
        return ""
    
    formatted = "\n\nEXAMPLES OF HIGH-QUALITY RESPONSES:\n\n"
    
    for i, example in enumerate(examples, 1):
        formatted += f"Example {i}:\n"
        formatted += f"Question: {example['question']}\n\n"
        formatted += f"Answer:\n{example['answer']}\n\n"
        formatted += "---\n\n"
    
    return formatted