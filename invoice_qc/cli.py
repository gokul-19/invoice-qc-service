import argparse
import json
from .extractor import InvoiceExtractor
from .validator import InvoiceValidator


def main():
    parser = argparse.ArgumentParser(description="Invoice QC CLI")
    sub = parser.add_subparsers(dest="command")

    # Extract
    e = sub.add_parser("extract")
    e.add_argument("--pdf-dir")
    e.add_argument("--output")

    # Validate
    v = sub.add_parser("validate")
    v.add_argument("--input")
    v.add_argument("--report")

    # Full run
    f = sub.add_parser("full-run")
    f.add_argument("--pdf-dir")
    f.add_argument("--report")

    args = parser.parse_args()

    if args.command == "extract":
        extractor = InvoiceExtractor()
        invoices = extractor.extract_invoices(args.pdf_dir)
        with open(args.output, "w") as f:
            f.write(json.dumps([inv.dict() for inv in invoices], indent=2))
        print(f"Extracted {len(invoices)} invoices")

    elif args.command == "validate":
        data = json.load(open(args.input))
        validator = InvoiceValidator()
        results = validator.validate([InvoiceExtractor().extract_single for _ in []])
        with open(args.report, "w") as f:
            f.write(json.dumps(results, indent=2))
        print(results["summary"])

    elif args.command == "full-run":
        extractor = InvoiceExtractor()
        invoices = extractor.extract_invoices(args.pdf_dir)
        validator = InvoiceValidator()
        results = validator.validate(invoices)
        with open(args.report, "w") as f:
            f.write(json.dumps(results, indent=2))
        print(results["summary"])


if __name__ == "__main__":
    main()
