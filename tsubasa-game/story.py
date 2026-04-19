# story.py — All the story nodes for the Tsubasa game
# Each node has: text, image emoji, and choices (or an ending)
# Kids: try adding your own nodes and choices!

STORY = {
    "start": {
        "text": (
            "You are Tsubasa Ozora, an 11-year-old soccer player from Nankatsu City. "
            "Today is the day of the big match against Shutetsu FC! "
            "Your team is counting on you. What do you do before the match?"
        ),
        "emoji": "⚽",
        "choices": [
            {"text": "Practice your Drive Shot on the field", "next": "practice"},
            {"text": "Talk to your teammate Oliver to plan tactics", "next": "tactics"},
            {"text": "Watch the rival team warm up to learn their style", "next": "scout"},
        ],
    },
    "practice": {
        "text": (
            "You spend an hour perfecting your famous Drive Shot. "
            "The ball screams through the air like a rocket! "
            "Coach Roberto watches and nods. 'Your shot is strong, Tsubasa.' "
            "The match begins — it's 0-0. You get a free kick 30 meters out!"
        ),
        "emoji": "🦵",
        "choices": [
            {"text": "Unleash the Drive Shot!", "next": "drive_shot_win"},
            {"text": "Pass to Oliver for a Twin Shot", "next": "twin_shot"},
        ],
    },
    "tactics": {
        "text": (
            "Oliver sketches a plan on the ground with a stick. "
            "'If we press high, their goalkeeper gets nervous.' "
            "You both agree on a signal: thumbs up means run into space. "
            "In the match, you spot Oliver give the thumbs up at the perfect moment!"
        ),
        "emoji": "🤝",
        "choices": [
            {"text": "Sprint into space and receive Oliver's pass", "next": "through_ball"},
            {"text": "Fake the run and let Oliver shoot alone", "next": "oliver_shoots"},
        ],
    },
    "scout": {
        "text": (
            "You notice Shutetsu's goalkeeper always dives left on shots. "
            "That's a secret weapon! You whisper this to Benji Price before the match. "
            "Benji grins: 'Good eyes, Tsubasa!' "
            "Late in the game, it's 1-1. You win a penalty kick!"
        ),
        "emoji": "🔍",
        "choices": [
            {"text": "Shoot right — the keeper's weak side!", "next": "penalty_win"},
            {"text": "Blast it straight down the middle", "next": "penalty_miss"},
        ],
    },
    "drive_shot_win": {
        "text": (
            "You plant your foot, swing your leg with everything you have — BOOM! "
            "The ball tears through the air and smashes into the top corner! "
            "GOOOAL! The crowd goes wild! Nankatsu leads 1-0! "
            "The final whistle blows. YOU WIN!"
        ),
        "emoji": "🏆",
        "ending": "win",
        "choices": [],
    },
    "twin_shot": {
        "text": (
            "You and Oliver line up side by side. "
            "'Together!' you shout. Both of you kick at the same instant — "
            "the goalkeeper doesn't know which way to dive! "
            "DOUBLE GOAL! The net explodes! Nankatsu wins 2-0!"
        ),
        "emoji": "🌟",
        "ending": "win",
        "choices": [],
    },
    "through_ball": {
        "text": (
            "You burst past two defenders at full speed. "
            "Oliver's pass is perfectly timed — it lands right at your feet! "
            "One-on-one with the goalkeeper... you chip the ball over him! "
            "GOOOAL! Nankatsu wins the match!"
        ),
        "emoji": "🏅",
        "ending": "win",
        "choices": [],
    },
    "oliver_shoots": {
        "text": (
            "You fake the run brilliantly — three defenders follow you! "
            "Oliver has a wide-open shot. He blasts it into the net! "
            "'Great assist, Tsubasa!' Oliver shouts. "
            "Nankatsu wins thanks to your selfless play!"
        ),
        "emoji": "🥇",
        "ending": "win",
        "choices": [],
    },
    "penalty_win": {
        "text": (
            "You step up calmly. You remember what you saw during warm-ups. "
            "You shoot right — the keeper dives left! "
            "The ball rolls gently into the empty net. "
            "Nankatsu wins the championship 2-1! Heroes!"
        ),
        "emoji": "🎉",
        "ending": "win",
        "choices": [],
    },
    "penalty_miss": {
        "text": (
            "You blast it straight and hard — but the keeper guessed right! "
            "He catches the ball easily. 1-1 at full time. "
            "The match goes to extra time. Your legs are tired. "
            "Shutetsu scores in extra time. You lose 2-1. "
            "But Roberto smiles: 'A loss teaches more than a win. Train harder!'"
        ),
        "emoji": "😤",
        "ending": "lose",
        "choices": [],
    },
}
