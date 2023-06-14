"""Skrypt przedstawiający kilka reguł PEP 8.
"""

import datetime as dt


TEMPERATURE_SCALES = ("fahrenheit", "kelvin",
                      "celsius")


class TemperatureConverter:
    pass  # W tym momencie nic się nie dzieje


def convert_to_celsius(degrees, source="fahrenheit"):
    """Ta funkcja konwertuje stopnie w skali Fahrenheita lub Kelvina
    na stopnie Celsjusza.
    """
    if source.lower() == "fahrenheit":
        return (degrees-32) * (5/9)
    elif source.lower() == "kelvin":
        return degrees - 273.15
    else:
        return f"Nie potrafię przekonwertować z {source}"


celsius = convert_to_celsius(44, source="fahrenheit")
non_celsius_scales = TEMPERATURE_SCALES[:-1]

print("Aktualny czas: " + dt.datetime.now().isoformat())
print(f"Temperatura w stopniach Celsjusza wynosi: {celsius}")
