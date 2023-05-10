def get_field_widget_attrs_with_placeholder_(
    placeholder: str,
) -> dict[str, str]:
    """Returns a dict of field widget attributes with the given placeholder."""
    return {"class": "w-50 form-control mb-2", "placeholder": placeholder}
