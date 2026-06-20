from dataclasses import dataclass


@dataclass
class AuditCancelledInvoiceRequest:
    book_path: str
    portal_path: str
