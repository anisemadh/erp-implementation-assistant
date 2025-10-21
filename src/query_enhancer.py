"""
Query enhancement for better retrieval
Expands queries with M3-specific terminology and synonyms
"""

# M3 Module and Program mappings
M3_MODULES = {
    'customer': ['OIS', 'CRS', 'customer order', 'sales order'],
    'purchase': ['PPS', 'purchasing', 'procurement', 'supplier', 'vendor'],
    'inventory': ['MMS', 'warehouse', 'stock', 'item master'],
    'finance': ['ARS', 'APS', 'GLS', 'accounts receivable', 'accounts payable'],
    'planning': ['MRP', 'MPS', 'demand', 'forecast', 'planning'],
}

# Common M3 programs by function
M3_PROGRAMS = {
    # Customer Order Management
    'customer order': ['OIS100', 'OIS300', 'OIS350'],
    'order type': ['OIS010', 'order type configuration'],
    'customer master': ['CRS610', 'customer setup'],
    'pricing': ['OIS017', 'OIS002', 'price list'],
    
    # Purchase Order Management
    'purchase order': ['PPS200', 'PPS300', 'PO'],
    'po type': ['PPS095', 'purchase order type'],
    'supplier': ['PPS001', 'PPS200', 'vendor'],
    'receiving': ['PPS300', 'receipt', 'goods receipt'],
    
    # Inventory
    'item': ['MMS001', 'item master', 'product'],
    'warehouse': ['MMS002', 'MMS005', 'warehouse setup'],
    'allocation': ['OIS100', 'MMS055', 'inventory allocation'],
    'stock': ['MMS060', 'on hand', 'inventory balance'],
    
    # Common processes
    'invoice': ['OIS350', 'ARS100', 'invoicing', 'billing'],
    'delivery': ['MWS410', 'shipment', 'picking'],
    'approval': ['CRS610', 'authority', 'workflow'],
}

# Common terminology expansions
TERMINOLOGY_MAP = {
    'po': 'purchase order PO',
    'so': 'sales order customer order SO',
    'sku': 'item number SKU product',
    'wh': 'warehouse WH',
    'cust': 'customer CUNO',
    'supp': 'supplier vendor SUNO',
    'qty': 'quantity QTY amount',
    'alloc': 'allocation allocate inventory reservation',
    'recv': 'receive receiving receipt goods receipt',
    'ship': 'shipping shipment delivery dispatch',
    'inv': 'invoice invoicing billing',
}

# Action words that indicate query type
ACTION_KEYWORDS = {
    'setup': 'configure configuration create set up establish',
    'create': 'add new generate build make',
    'configure': 'setup configuration settings parameters',
    'troubleshoot': 'issue problem error fix debug why',
    'process': 'workflow procedure steps how to',
}

class QueryEnhancer:
    """Enhances user queries with M3-specific terminology"""
    
    def __init__(self):
        self.modules = M3_MODULES
        self.programs = M3_PROGRAMS
        self.terminology = TERMINOLOGY_MAP
        self.actions = ACTION_KEYWORDS
    
    def enhance_query(self, query: str) -> str:
        """
        Enhance query with M3 terminology and related concepts
        Returns expanded query for better retrieval
        """
        query_lower = query.lower()
        enhancements = []
        
        # Start with original query
        enhanced = query
        
        # 1. Expand abbreviations and terminology
        for abbrev, expansion in self.terminology.items():
            if abbrev in query_lower.split():  # Match whole words
                enhancements.append(expansion)
        
        # 2. Add related M3 programs
        for concept, programs in self.programs.items():
            if concept in query_lower:
                enhancements.extend(programs[:2])  # Add top 2 programs
        
        # 3. Add module context
        for module_name, keywords in self.modules.items():
            if any(keyword in query_lower for keyword in keywords):
                enhancements.append(module_name)
        
        # 4. Expand action words
        for action, expansions in self.actions.items():
            if action in query_lower:
                # Don't add all expansions, just most relevant
                enhancements.append(expansions.split()[0])
        
        # 5. Add specific enhancements based on query patterns
        if 'order type' in query_lower:
            if 'customer' in query_lower or 'sales' in query_lower:
                enhancements.extend(['OIS010', 'customer order type'])
            elif 'purchase' in query_lower or 'po' in query_lower:
                enhancements.extend(['PPS095', 'purchase order type'])
        
        if 'allocat' in query_lower:
            enhancements.extend(['OIS100', 'allocation', 'inventory reservation'])
        
        if 'pric' in query_lower:
            enhancements.extend(['OIS017', 'OIS002', 'price list'])
        
        if 'receiv' in query_lower or 'receipt' in query_lower:
            enhancements.extend(['PPS300', 'goods receipt', 'receiving'])
        
        if 'invoice' in query_lower or 'invoic' in query_lower:
            enhancements.extend(['OIS350', 'invoicing', 'billing'])
        
        # 6. Combine original query with enhancements
        if enhancements:
            # Remove duplicates and join
            unique_enhancements = list(dict.fromkeys(enhancements))
            enhanced = f"{query} {' '.join(unique_enhancements)}"
        
        return enhanced
    
    def get_module_hints(self, query: str) -> list:
        """
        Identify which M3 modules are relevant to the query
        Useful for metadata filtering
        """
        query_lower = query.lower()
        relevant_modules = []
        
        for module_name, keywords in self.modules.items():
            if any(keyword in query_lower for keyword in keywords):
                relevant_modules.append(module_name)
        
        return relevant_modules


def enhance_query(query: str) -> str:
    """Convenience function to enhance a query"""
    enhancer = QueryEnhancer()
    return enhancer.enhance_query(query)


if __name__ == "__main__":
    # Test the enhancer
    test_queries = [
        "How do I create a PO?",
        "Set up customer order type",
        "Why can't I allocate inventory?",
        "Customer pricing not working",
        "Receive purchase order",
    ]
    
    enhancer = QueryEnhancer()
    
    print("Query Enhancement Examples:\n")
    for query in test_queries:
        enhanced = enhancer.enhance_query(query)
        print(f"Original:  {query}")
        print(f"Enhanced:  {enhanced}")
        print(f"Modules:   {enhancer.get_module_hints(query)}")
        print("-" * 80)