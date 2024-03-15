import random

blackjack_values = {
    "2" : {"value" : 2, "name": 2, "file_name" : "2h.png:2d.png:2c.png:2s.png"},
    "3" : {"value" : 3, "name": 3, "file_name" : "3h.png:3d.png:3c.png:3s.png"},
    "4" : {"value" : 4, "name": 4, "file_name" : "4h.png:4d.png:4c.png:4s.png"},
    "5" : {"value" : 5, "name": 5, "file_name" : "5h.png:5d.png:5c.png:5s.png"},
    "6" : {"value" : 6, "name": 6, "file_name" : "6h.png:6d.png:6c.png:6s.png"},
    "7" : {"value" : 7, "name": 7, "file_name" : "7h.png:7d.png:7c.png:7s.png"},
    "8" : {"value" : 8, "name": 8, "file_name" : "8h.png:8d.png:8c.png:8s.png:11h.png:11d.png:11c.png:11s.png"},
    "9" : {"value" : 9, "name": 9, "file_name" : "9h.png:9d.png:9c.png:9s.png:12h.png:12d.png:12c.png:12s.png"},
    "10" : {"value" : 10, "name": 10, "file_name" : "10h.png:10d.png:10c.png:10s.png:13h.png:13d.png:13c.png:13s.png"},
    "11": {"value": 11, "name": 11, "file_name": "1h.png:1d.png:1c.png:1s.png"},
}


card = random.choice(range(2, 11))
card_info = bakkara_values[f'{card}']['file_name'].split(':')
image = random.choice(card_info)
#print(card_info)