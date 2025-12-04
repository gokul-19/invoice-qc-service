from collections import defaultdict
from datetime import datetime

class InvoiceValidator:

    def validate(self, invoices):
        summary = defaultdict(int)
        results = []

        seen_keys = set()

        for inv in invoices:
            errors = []

            # Completeness
            if not inv.invoice_number:
                errors.append("missing_field: invoice_number")
            if not inv.invoice_date:
                errors.append("missing_field: invoice_date")
            if not inv.seller_name or not inv.buyer_name:
                errors.append("missing_field: party_name")

            # Format
            errors += self.check_date(inv.invoice_date)
            errors += self.check_date(inv.due_date)

            if inv.currency not in ["INR", "EUR", "USD"]:
                errors.append("invalid_currency")

            # Business Rules
            errors += self.check_totals(inv)
            errors += self.check_due_date(inv)

            # Duplicate
            key = (inv.invoice_number, inv.seller_name, inv.invoice_date)
            if key in seen_keys:
                errors.append("duplicate_invoice")
            else:
                seen_keys.add(key)

            is_valid = len(errors) == 0

            for e in errors:
                summary[e] += 1

            results.append({
                "invoice_id": inv.invoice_number,
                "is_valid": is_valid,
                "errors": errors
            })

        summary_final = {
            "total_invoices": len(invoices),
            "valid_invoices": sum(r["is_valid"] for r in results),
            "invalid_invoices": sum(not r["is_valid"] for r in results),
            "error_counts": summary
        }
        return {"summary": summary_final, "results": results}

    # ----------- HELPER RULES ------------

    def check_date(self, date_str):
        if not date_str:
            return []
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            if dt.year < 2000 or dt.year > 2035:
                return ["invalid_date_range"]
            return []
        except:
            return ["invalid_date_format"]

    def check_totals(self, inv):
        errors = []
        if inv.line_items:
            computed = sum(i.line_total for i in inv.line_items)
            if inv.net_total and abs(inv.net_total - computed) > 0.01:
                errors.append("business_rule_failed: net_total_mismatch")

        if inv.net_total and inv.tax_amount and inv.gross_total:
            if abs(inv.net_total + inv.tax_amount - inv.gross_total) > 0.01:
                errors.append("business_rule_failed: totals_mismatch")

        return errors

    def check_due_date(self, inv):
        if not inv.due_date or not inv.invoice_date:
            return []

        try:
            inv_date = datetime.strptime(inv.invoice_date, "%Y-%m-%d")
            due_date = datetime.strptime(inv.due_date, "%Y-%m-%d")
            if due_date < inv_date:
                return ["business_rule_failed: due_before_invoice"]
        except:
            return []
        return []
