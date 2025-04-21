from datetime import datetime

import json


def check_capacity(max_capacity: int, guests: list) -> bool:
    events = []

    for guest in guests:
        check_in = guest["check-in"]
        check_out = guest["check-out"]

        events.append((check_in, 1))
        events.append((check_out, -1))

    events.sort()
    current_guests = 0
    for event in events:
        data, change = event
        current_guests += change

        if current_guests > max_capacity:
            return False

    return True

if __name__ == "__main__":
    max_capacity = int(input())
    n = int(input())


    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)


    result = check_capacity(max_capacity, guests)
    print(result)