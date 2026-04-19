# story.py — All the story nodes for the Tsubasa game
# Each node has: text, emoji, and choices (or an ending)
# Kids: try adding your own nodes and choices!
#
# HOW A NODE WORKS:
#   "my_node": {
#       "text": "What happens in the story...",
#       "emoji": "⚽",
#       "choices": [
#           {"text": "Button the player sees", "next": "another_node"},
#       ],
#   }
# For an ending node, replace "choices" with "ending": "win" or "ending": "lose"

# GUIDE_STEPS — shown on the /guide page to teach kids how to add story nodes
GUIDE_STEPS = [
    {
        "title": "Step 1: Open story.py",
        "emoji": "📂",
        "text": "All the story lives in story.py. Open it in any text editor. You will see a big dictionary called STORY.",
        "code": None,
    },
    {
        "title": "Step 2: Understand a node",
        "emoji": "🗺️",
        "text": "Every part of the story is called a NODE. A node has three things: text (the story), emoji (a picture), and choices (buttons for the player).",
        "code": (
            '"my_node": {\n'
            '    "text": "Something happens here...",\n'
            '    "emoji": "⚽",\n'
            '    "choices": [\n'
            '        {"text": "Button label", "next": "another_node"},\n'
            '    ],\n'
            '},'
        ),
    },
    {
        "title": "Step 3: Add an ending node",
        "emoji": "🏁",
        "text": 'When the story is finished, use "ending": "win" or "ending": "lose" instead of choices.',
        "code": (
            '"my_ending": {\n'
            '    "text": "You won the World Cup!",\n'
            '    "emoji": "🏆",\n'
            '    "ending": "win",\n'
            '    "choices": [],\n'
            '},'
        ),
    },
    {
        "title": "Step 4: Connect your nodes",
        "emoji": "🔗",
        "text": 'The "next" value in a choice must exactly match the name of another node. That is how the story jumps from one node to the next.',
        "code": (
            '# In node A, point to node B:\n'
            '"choices": [\n'
            '    {"text": "Go to B", "next": "node_b"},\n'
            '],\n\n'
            '# Then make node B exist in STORY:\n'
            '"node_b": {\n'
            '    "text": "You arrived at node B!",\n'
            '    ...\n'
            '},'
        ),
    },
    {
        "title": "Step 5: Pick a fun emoji",
        "emoji": "😄",
        "text": "Change the emoji to match the mood of your scene. Copy any emoji from the internet and paste it into the emoji field.",
        "code": (
            '"emoji": "🌧️",   # rainy sad scene\n'
            '"emoji": "🔥",   # exciting action scene\n'
            '"emoji": "🤔",   # thinking / mystery scene\n'
            '"emoji": "🎉",   # celebration scene'
        ),
    },
    {
        "title": "Step 6: Restart the server",
        "emoji": "🔄",
        "text": "After saving story.py, stop the server with Ctrl+C and run python app.py again. Then refresh your browser to see your new story!",
        "code": "python app.py",
    },
]

STORY = {
    # ------------------------------------------------------------------ START
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
            {"text": "Visit Genzo in goal to build team spirit", "next": "genzo_talk"},
        ],
    },

    # ------------------------------------------------------------------ PATH: PRACTICE
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
            {"text": "Look up — Santana is rushing at you!", "next": "santana_block"},
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
    "santana_block": {
        "text": (
            "The fearsome Santana from South America charges towards you! "
            "He's the best player on Shutetsu. You have a split second to decide."
        ),
        "emoji": "😰",
        "choices": [
            {"text": "Hold your ground and shoot through him", "next": "santana_shoot"},
            {"text": "Dribble left and go around him", "next": "santana_dribble"},
            {"text": "Dummy the shot and let Oliver in", "next": "oliver_shoots"},
        ],
    },
    "santana_shoot": {
        "text": (
            "You shoot with all your power straight through Santana's challenge! "
            "The ball deflects off his shin... and loops into the net! "
            "An incredible lucky goal — but a goal is a goal! "
            "Nankatsu wins 1-0!"
        ),
        "emoji": "🍀",
        "ending": "win",
        "choices": [],
    },
    "santana_dribble": {
        "text": (
            "You feint left — Santana goes the wrong way! "
            "You burst into the box, one-on-one with the keeper. "
            "Coolly you slide the ball into the bottom corner. "
            "GOOOAL! The crowd roars! Nankatsu wins!"
        ),
        "emoji": "💨",
        "ending": "win",
        "choices": [],
    },

    # ------------------------------------------------------------------ PATH: TACTICS
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
            {"text": "Signal back: ask Oliver to make the run instead", "next": "switch_roles"},
        ],
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
    "switch_roles": {
        "text": (
            "Oliver nods and makes the run instead of you. "
            "He receives the ball in space, but a defender catches up. "
            "Oliver squares it back to you in the middle — completely free! "
            "You smash a volley into the roof of the net. GOOOAL!"
        ),
        "emoji": "🔄",
        "ending": "win",
        "choices": [],
    },

    # ------------------------------------------------------------------ PATH: SCOUT
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
            {"text": "Let Benji take the penalty instead", "next": "benji_penalty"},
        ],
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
    "benji_penalty": {
        "text": (
            "You hand the ball to Benji. He looks surprised but determined. "
            "'I trust you,' you say. Benji places the ball on the spot. "
            "He runs up slowly... and curls it into the top corner! "
            "Benji leaps into the air! Nankatsu wins 2-1! A true team victory!"
        ),
        "emoji": "🤜🤛",
        "ending": "win",
        "choices": [],
    },

    # ------------------------------------------------------------------ PATH: GENZO
    "genzo_talk": {
        "text": (
            "You find Genzo Wakabayashi stretching in goal. "
            "He is Shutetsu's legendary goalkeeper — and today he's your rival! "
            "Wait... Genzo looks sad. 'I hurt my hand in training,' he admits quietly. "
            "What do you do with this information?"
        ),
        "emoji": "🧤",
        "choices": [
            {"text": "Keep it secret and use it to your advantage", "next": "genzo_exploit"},
            {"text": "Tell your team to play fair — no targeting the injury", "next": "genzo_fair"},
            {"text": "Encourage Genzo: 'A great keeper plays with heart, not hands'", "next": "genzo_inspire"},
        ],
    },
    "genzo_exploit": {
        "text": (
            "You tell your team to shoot at Genzo's hurt hand every time. "
            "You score two easy goals... but the crowd boos. "
            "Even your own teammates look uncomfortable. "
            "Nankatsu wins 2-0, but no one celebrates. "
            "Coach Roberto says quietly: 'We won the match but lost our honour.'"
        ),
        "emoji": "😔",
        "ending": "lose",
        "choices": [],
    },
    "genzo_fair": {
        "text": (
            "You tell your team to play normally — no targeting the injury. "
            "Genzo plays brilliantly despite the pain, saving shot after shot. "
            "In the last minute you score a wonder goal from 40 metres. "
            "Genzo applauds from his goal. 'Well played, Tsubasa.' "
            "Nankatsu wins 1-0. A victory to be proud of!"
        ),
        "emoji": "🤺",
        "ending": "win",
        "choices": [],
    },
    "genzo_inspire": {
        "text": (
            "Genzo stares at you, then smiles. 'You're right.' "
            "Inspired by your words, Genzo plays the match of his life — "
            "but so do you! The game ends 1-1 after a thrilling battle. "
            "In the penalty shootout you score the winning kick. "
            "Genzo walks over and shakes your hand: 'Rivals and friends.'"
        ),
        "emoji": "🌅",
        "ending": "win",
        "choices": [],
    },
}
