import re


def digits_from_str(string: str) -> str:
    return "".join(re.findall(r"\d+", string))


def correction_phone_country_code(
        phone: str, correct_code: str = "+7", start_number: str = "9"
) -> str:
    if phone[0:len(correct_code)-1] != correct_code:
        phone = correct_code + phone if phone[0] == start_number else correct_code + phone[phone.find(start_number):]
    return phone


corr_phone_code = correction_phone_country_code
