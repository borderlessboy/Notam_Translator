"""
notam_translator module

This module provides functions for parsing and translating NOTAM messages.

Functions:
    parse_notam(notam): Parse a NOTAM message and extract relevant information.
    
    create_readable_message(parsed_info): Create a human-readable 
    message from parsed NOTAM information.
    
    format_time(utc_time): Convert a UTC time string to a readable date format.
"""
import re
from datetime import datetime

def parse_notam(notam):
    """
    Parse a NOTAM message and extract relevant information.

    Args:
        notam (str): The NOTAM message to parse.

    Returns:
        dict: A dictionary containing the extracted information, including Location, Activity
        , Operational Area, Start Time, End Time, Surface, Altitude, Created Time, and Source.

    Raises:
        AttributeError: If the NOTAM message is invalid or missing required information.
    """
    parsed_info = {
        'Location': 'N/A',
        'Activity': 'N/A',
        'Operational Area': 'N/A',
        'Start Time': 'N/A',
        'End Time': 'N/A',
        'Surface': 'SFC',
        'Altitude': 'N/A',
        'Created Time': 'N/A',
        'Source': 'N/A'
    }
    # Extract information from the NOTAM message
    try:
        parsed_info['Location'] = re.search(r'Q\) (\w+)', notam).group(1)
    except AttributeError:
        pass

    try:
        parsed_info['Activity'] = re.search(r'E\) (.*?)(?=F\)|$)'
            , notam, re.DOTALL).group(1).strip()
    except AttributeError:
        pass

    try:
        parsed_info['Operational Area'] = re.search(r'Q\) \w+/(\w+)', notam).group(1)
    except AttributeError:
        pass

    try:
        start_time = re.search(r'B\) (\d{10})', notam).group(1)
        parsed_info['Start Time'] = format_time(start_time)
    except AttributeError:
        pass

    try:
        end_time = re.search(r'C\) (\d{10})', notam).group(1)
        parsed_info['End Time'] = format_time(end_time)
    except AttributeError:
        pass

    try:
        parsed_info['Altitude'] = re.search(r'G\) (\d+)FT', notam).group(1)
    except AttributeError:
        pass

    try:
        parsed_info['Created Time'] = re.search(r'CREATED: (.*?) SOURCE:', notam).group(1)
    except AttributeError:
        pass

    try:
        parsed_info['Source'] = re.search(r'SOURCE: (\w+)', notam).group(1)
    except AttributeError:
        pass

    return parsed_info

def format_time(utc_time):
    """
    Convert a UTC time string to a readable date format.

    Args:
        utc_time (str): The UTC time string to convert.

    Returns:
        str: The converted time string in a readable date format.
    """
    # Convert the YYMMDDHHMM format to a readable date format
    return datetime.strptime(utc_time, '%y%m%d%H%M').strftime('%Y-%m-%d %H:%M UTC')


def create_readable_message(parsed_info):
    """
    Create a human-readable message from parsed NOTAM information.

    Args:
        parsed_info (dict): The dictionary containing the extracted NOTAM information.

    Returns:
        str: A human-readable message summarizing the NOTAM information.
    """
    message = "NOTAM Translation:\n"
    for key, value in parsed_info.items():
        # Convert key to title case and replace underscores with spaces
        formatted_key = key.replace('_', ' ').title()
        message += f"{formatted_key}: {value}\n"
    return message

def main():
    """
    Main entry point for the NOTAM translator program.

    Prompts the user to enter a NOTAM message, parses the message
    , and prints a human-readable translation.

    Returns:
        None
    """
    print("Enter the NOTAM message:")
    notam_input = input()
    parsed_info = parse_notam(notam_input)
    if parsed_info:
        readable_message = create_readable_message(parsed_info)
        print(readable_message)
    else:
        print("Invalid NOTAM format. Please check the input.")

if __name__ == "__main__":
    main()
