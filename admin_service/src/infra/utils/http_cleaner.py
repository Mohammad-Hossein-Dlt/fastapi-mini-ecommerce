def clean_outbound_request(data: dict) -> dict:
    """Remove None values before sending HTTP requests."""
    return {k: v for k, v in data.items() if v is not None}
