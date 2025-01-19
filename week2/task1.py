import re

def find_and_print(messages, current_station):

    def friend_station(message):
        match = re.findall(r'\b[A-Z][a-z]*\b(?:\s[A-Z][a-z]*\b)*', message)
        if match:
            return match
        return None

    def calculate_distance(current_pos, friend_pos):
        if isinstance(current_pos, list):  
            current_main, current_branch = current_pos
        else:
            current_main, current_branch = current_pos, 0

        if isinstance(friend_pos, list):  
            friend_main, friend_branch = friend_pos
        else:
            friend_main, friend_branch = friend_pos, 0

        return abs(current_main - friend_main) + abs(current_branch - friend_branch)

    glstation = {
        "Songshan": 0,
        "Nanjing Sanmin": 1,
        "Taipei Arena": 2,
        "Nanjing Fuxing": 3,
        "Songjiang Nanjing": 4,
        "Zhongshan": 5,
        "Beimen": 6,
        "Ximen": 7,
        "Xiaonanmen": 8,
        "Chiang kai-Shek Memorial Hall": 9,
        "Guting": 10,
        "Taipower Building": 11,
        "Gongguan": 12,
        "Wanlong": 13,
        "Jingmei": 14,
        "Dapinglin": 15,
        "Qizhang": 16,
        "Xiaobitan": [16, 1], 
        "Xindian City Hall": 17,
        "Xindian": 18
    }

    current_pos = glstation[current_station]

    closest_friend = None
    min_distance = float('inf')

    for friend, message in messages.items():
        station_names = friend_station(message)
        if station_names:
            for station_name in station_names:
                if station_name in glstation:
                    friend_pos = glstation[station_name]
                    distance = calculate_distance(current_pos, friend_pos)
                    if distance < min_distance:
                        min_distance = distance
                        closest_friend = friend

    if closest_friend:
        print(closest_friend)

messages = {
    "Leslie": "I'm at home near Xiaobitan station.",
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Vivian": "I'm at Xindian station waiting for you."
}

find_and_print(messages, "Wanlong")  # print Mary
find_and_print(messages, "Songshan")  # print Copper
find_and_print(messages, "Qizhang")  # print Leslie
find_and_print(messages, "Ximen")  # print Bob
find_and_print(messages, "Xindian City Hall")  # print Vivian
