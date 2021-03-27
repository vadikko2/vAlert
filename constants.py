CRITICAL_TYPES = ('critical', 'normal', 'low', 'important')
DEPARTURES = ('it', 'finance')

# Указываем с какой вероятностью буду выпадать заявки определенной критичностью.
# Cумма вероятностей должна ровняться 1
FREQUENCY_LIST = [
    ('critical', 0.5),
    ('important', 0.25),
    ('normal', 0.175),
    ('low', 0.075)
]