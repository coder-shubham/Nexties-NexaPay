from decimal import Decimal

def format_fixed(value, decimals=0):
    # Ensure value and decimals are Decimal for precision arithmetic
    value = Decimal(value)
    decimals = Decimal(decimals)
    
    # Get the multiplier as 10^decimals
    multiplier = Decimal(10) ** decimals
    
    # Check for negative value
    negative = value < 0
    if negative:
        value = -value

    # Calculate whole and fraction part
    whole = value // multiplier  # Integer division
    fraction = value % multiplier  # Remainder for fractional part

    # Convert fraction to string and pad with zeros if necessary
    fraction_str = str(fraction).rstrip('0')  # Remove trailing zeros
    fraction_str = fraction_str.zfill(int(decimals))

    # Combine whole and fraction
    if decimals == 0:
        result = str(whole)
    else:
        result = f"{whole}.{fraction_str}"

    # Add negative sign back if necessary
    if negative:
        result = f"-{result}"

    return result

def parse_fixed(value: str, decimals: int = 0):
    # Ensure value is a valid decimal string
    if not isinstance(value, str) or not value.replace(',', '').replace('.', '', 1).isdigit():
        raise ValueError(f"Invalid decimal value: {value}")

    # Is the value negative?
    negative = value.startswith("-")
    if negative:
        value = value[1:]  # Remove the negative sign for processing

    # Handle case where value is just "."
    if value == ".":
        raise ValueError("Missing value")

    # Split into whole and fractional parts
    comps = value.split(".")
    if len(comps) > 2:
        raise ValueError(f"Too many decimal points in value: {value}")

    whole, fraction = comps[0], comps[1] if len(comps) > 1 else "0"

    # Remove trailing zeros from the fractional part
    fraction = fraction.rstrip("0")

    # Ensure fraction doesn't exceed the allowed decimals
    if len(fraction) > decimals:
        raise ValueError(f"Fractional component exceeds decimals: {fraction}")

    # Pad the fraction to the appropriate length for the given decimals
    fraction = fraction.ljust(decimals, "0")

    # Convert to integers for the whole and fractional parts
    whole_value = Decimal(whole) if whole else Decimal(0)
    fraction_value = Decimal(fraction) if fraction else Decimal(0)

    # Calculate the result in Wei (or equivalent smallest unit)
    multiplier = Decimal(10) ** decimals
    wei_value = (whole_value * multiplier) + fraction_value

    # Apply negative sign if needed
    if negative:
        wei_value = -wei_value

    # Return the result as a string for precise handling
    return str(int(wei_value))