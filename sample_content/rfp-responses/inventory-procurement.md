# RFP Response: Inventory & Procurement

## Overview

This document contains standard RFP responses for Fourth's MacromatiX inventory and procurement capabilities. Each response is formatted with the original question, a detailed answer, and a confidence level. All responses reflect current platform capabilities and may be used directly in RFP submissions with appropriate customization for the specific prospect's requirements.

---

## Q: Describe your inventory management capabilities.

**Confidence: GROUNDED** -- Based on verified MacromatiX platform capabilities.

Fourth's MacromatiX inventory management module provides end-to-end food and beverage cost control for multi-unit restaurant operators. Core capabilities include:

### Actual vs. Theoretical Food Cost

MacromatiX calculates theoretical food cost based on POS sales data and standardized recipes, then compares it against actual inventory usage determined through physical counts and purchase records. This actual-vs-theoretical (AvT) variance analysis identifies cost leakage at the item, category, location, and enterprise level.

| Metric | Description |
|--------|-------------|
| Theoretical cost | What food cost *should be* based on what was sold (POS mix x recipe cost) |
| Actual cost | What food cost *actually was* based on purchases, transfers, and count changes |
| Variance | Difference expressed in dollars and percentage, drillable to item level |

Typical operators identify 2-5% food cost variance through AvT analysis, with actionable insights to close the gap through portion control, waste reduction, and theft prevention.

### Recipe Management

MacromatiX supports multi-level recipe management including:

- **Ingredient-level recipes** with unit-of-measure conversions, preparation yields, and cooking loss factors
- **Sub-recipes** (components that feed into finished menu items)
- **Batch recipes** for prep items produced in volume
- **Menu item costing** that rolls up all recipe layers to produce accurate plate cost
- **Allergen and nutritional tracking** at the ingredient and recipe level
- **Seasonal and regional recipe variations** managed through recipe versioning

Recipe changes automatically cascade through all dependent menu items, updating theoretical costs in real time.

### Vendor Ordering

MacromatiX streamlines the ordering process through:

- **Par-level ordering**: System calculates suggested order quantities based on current inventory, par levels, and forecasted demand
- **Order guides**: Vendor-specific order templates with approved items, pack sizes, and pricing
- **Multi-vendor comparison**: Side-by-side pricing for equivalent items across approved vendors
- **Order scheduling**: Automated order creation based on delivery schedules and lead times
- **Mobile ordering**: Managers can count inventory and place orders from a tablet or mobile device

### Waste Tracking

The waste management module captures and categorizes waste events:

- **Prep waste**: Over-production, trimming loss, preparation errors
- **Line waste**: Expired product, quality issues, dropped items
- **Customer returns**: Tracked by reason code (wrong order, quality complaint)
- **Donation tracking**: Items donated to food banks with documentation for tax deduction purposes

Waste data feeds directly into AvT analysis, helping operators distinguish between controllable waste (training issues, over-prep) and inherent waste (yield factors, spoilage).

---

## Q: How do you handle procurement and purchase-to-pay?

**Confidence: GROUNDED** -- Based on verified MacromatiX procurement workflow capabilities.

Fourth's MacromatiX module provides a complete purchase-to-pay workflow from requisition through invoice reconciliation.

### Purchase Order Automation

| Capability | Detail |
|-----------|--------|
| **Auto-generated POs** | System creates purchase orders based on par levels, forecasted demand, and current on-hand inventory |
| **Approval workflows** | Configurable approval chains based on PO value, category, or location; supports multi-level approval for large orders |
| **Vendor management** | Centralized vendor database with contract pricing, delivery schedules, minimum order quantities, and performance ratings |
| **Contract price enforcement** | System flags orders that deviate from contracted pricing; tracks price changes over time |
| **Blanket POs** | Support for standing orders with periodic delivery against a master agreement |

### Invoice Reconciliation

MacromatiX supports three-way matching between purchase orders, receiving records, and vendor invoices:

1. **Purchase order** documents what was ordered and at what price.
2. **Receiving record** captures what was actually delivered (quantity, condition, substitutions).
3. **Vendor invoice** is matched against the PO and receiving record.
4. **Discrepancies** (price variances, quantity differences, unauthorized substitutions) are flagged for resolution before payment approval.

### Approval Workflows

Approval workflows are configurable by:
- Dollar threshold (e.g., orders over $5,000 require regional manager approval)
- Product category (e.g., alcohol orders require specific approver)
- Vendor (e.g., new vendors require procurement team approval for first 3 orders)
- Exception-based (e.g., only orders exceeding budget by more than 10% require approval)

---

## Q: What food cost analytics do you provide?

**Confidence: GROUNDED** -- Based on verified MacromatiX analytics and reporting capabilities.

MacromatiX provides comprehensive food cost analytics at the item, location, region, and enterprise levels.

### Variance Analysis

The primary analytical framework is actual-versus-theoretical variance, available in multiple views:

| View | Granularity | Use Case |
|------|------------|----------|
| Item-level variance | Individual ingredient or menu item | Identify specific items with high waste or theft |
| Category variance | Food groups (proteins, produce, dairy, etc.) | Spot systematic issues by category |
| Location comparison | Side-by-side location performance | Benchmark locations against each other |
| Trend analysis | Week-over-week, period-over-period | Track improvement or deterioration over time |
| Daypart analysis | Variance by meal period | Identify prep or service issues by shift |

### Menu Engineering

MacromatiX provides menu engineering analytics that combine sales mix data with food cost data:

- **Stars**: High profitability, high popularity -- protect and promote
- **Plowhorses**: Low profitability, high popularity -- re-engineer for margin
- **Puzzles**: High profitability, low popularity -- increase marketing/visibility
- **Dogs**: Low profitability, low popularity -- consider removing from menu

Menu engineering reports update automatically as sales mix and food costs change.

### Cost Trending

- **Commodity price tracking**: Monitor ingredient cost changes over time
- **Vendor price comparison**: Track pricing across suppliers for the same items
- **Menu price impact modeling**: Simulate the effect of ingredient cost changes on menu item margins
- **Budget vs. actual**: Track food cost against budgeted targets by location and period

---

## Q: How does your system integrate with POS for menu mix data?

**Confidence: GROUNDED** -- Based on verified POS integration capabilities.

MacromatiX integrates with all major restaurant POS systems to receive real-time sales mix data, which drives theoretical food cost calculations and demand-driven ordering.

### Supported POS Integrations

| POS System | Integration Method | Data Received |
|-----------|-------------------|---------------|
| Toast | API (real-time) | Sales mix, modifiers, voids, comps |
| Aloha (NCR) | API / file-based | Sales mix, modifiers, labor data |
| MICROS (Oracle) | API / file-based | Sales mix, modifiers, revenue centers |
| Revel | API (real-time) | Sales mix, modifiers, discounts |
| Square | API (real-time) | Sales mix, item-level detail |
| Brink (PAR) | API | Sales mix, modifiers |
| Qu | API (real-time) | Sales mix, modifiers |
| Custom/Other | Flat file import, API | Configurable data mapping |

### Data Flow

1. POS transmits sales transactions (typically at 15-minute intervals or end-of-day batch).
2. MacromatiX maps POS menu items to recipes in the recipe database.
3. Theoretical usage is calculated: sales quantity x recipe ingredients = what should have been used.
4. Theoretical usage is compared against actual usage (purchases - ending inventory + beginning inventory).
5. Variance is reported at item, category, and location level.

### Demand-Driven Ordering

POS sales data also feeds Fourth's demand forecasting engine (Fourth iQ), which projects future sales at the menu-item level. MacromatiX uses these forecasts to generate suggested order quantities that account for:
- Projected sales by menu item for the order period
- Current on-hand inventory
- Safety stock requirements
- Vendor lead times and delivery schedules
- Shelf life and perishability constraints

This demand-driven approach reduces both over-ordering (waste) and under-ordering (stockouts that affect guest experience and revenue).
