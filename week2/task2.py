def book(consultants, hour, duration, criteria):

    if 'schedule' not in consultants[0]:
        for consultant in consultants:
            consultant['schedule'] = []

    def is_available(schedule, start, duration):

        end = start + duration
        for booked_start, booked_end in schedule:
            if not (end <= booked_start or start >= booked_end):
                return False
        return True

    def book_time(schedule, start, duration):

        schedule.append((start, start + duration))


    available_consultants = [
        c for c in consultants 
        if is_available(c['schedule'], hour, duration)
    ]

    if not available_consultants:
        print("No Service")
        return


    if criteria == "price":
        best_consultant = min(available_consultants, key=lambda c: c['price'])
    elif criteria == "rate":
        best_consultant = max(available_consultants, key=lambda c: c['rate'])
    

    book_time(best_consultant['schedule'], hour, duration)
    print(best_consultant['name'])


consultants = [
    {"name": "John", "rate": 4.5, "price": 1000},
    {"name": "Bob", "rate": 3, "price": 1200},
    {"name": "Jenny", "rate": 3.8, "price": 800}
]

book(consultants, 15, 1, "price")  # Jenny
book(consultants, 11, 2, "price")  # Jenny
book(consultants, 10, 2, "price")  # John
book(consultants, 20, 2, "rate")   # John
book(consultants, 11, 1, "rate")   # Bob
book(consultants, 11, 2, "rate")   # No Service
book(consultants, 14, 3, "price")  # John