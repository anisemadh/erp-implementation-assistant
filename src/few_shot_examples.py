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
    }
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
    }
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
    }
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