import random

STATUS_COMMENTS = {
    'Done': [
        "🎉 Another one bites the dust!",
        "✨ Crushed it!",
        "🚀 Mission accomplished!",
        "🌟 Nailed it!"
    ],

    'Live Testing': [
        "🔍 Let's hunt those bugs!",
        "🎯 Testing in progress...",
        "🧪 Lab work ongoing",
        "🔬 Under the microscope"
    ],

    'Ready for Release': [
        "🚦 Ready for takeoff!",
        "📦 Packed and ready to go",
        "🎁 Fresh out of the oven",
        "🔥 Hot and ready!"
    ],

    'In Development': [
        "⚡ Code wizards at work",
        "🛠️ Building something awesome",
        "💻 Cooking up some code",
        "🔨 Hammering out the details"
    ],

    'Ready': [
        "🎬 Action stations!",
        "⭐ Time to shine",
        "🎯 Target acquired",
        "🔋 Charged up and ready"
    ],

    'Refinement': [
        "🎨 Making it beautiful",
        "✨ Adding some sparkle",
        "🔧 Fine-tuning in progress",
        "💎 Polishing to perfection"
    ]
}

GREETINGS = [
    "Hey team! Here's what's cooking",
    "Greetings, fellow developers!",
    "Welcome to this week's update",
    "Another exciting week in the books",
    "Time for your weekly dose of progress"
]

CLOSING_MESSAGES = [
    "Keep crushing it! 💪",
    "Another great week in the books! 🎉",
    "Until next time, happy coding! 💻",
    "Stay awesome, team! ⭐",
    "Let's keep the momentum going! 🚀"
]

EMOJIS = ["🚀", "💻", "⚡", "🎯", "✨", "🔥", "💪", "🎨", "🎉", "🌟"]

def get_random_emoji():
    return random.choice(EMOJIS)

def get_random_greeting():
    return random.choice(GREETINGS)

def get_random_status_comment(status):
    if status in STATUS_COMMENTS:
        return random.choice(STATUS_COMMENTS[status])
    return f"{get_random_emoji()} Status: {status}"

def get_random_closing_message():
    return random.choice(CLOSING_MESSAGES)