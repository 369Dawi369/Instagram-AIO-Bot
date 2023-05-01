import random

hashtags = [
        "#memes #dankmemes #funnymemes #memesdaily #edgymemes #offensivememes #dailymemes #fortnitememes #memestagram",
        "#spicymemes #btsmemes #animememes #tiktokmemes #memesespañol #memesespañol #nichememes #dankmemesdaily",
        "#kpopmemes #bestmemes #spongebobmemes #darkmemes #wholesomememes #memestar #relatablememes #stolenmemes",
        "#instamemes #memesrlife #pubgmemes #memesbrasil #memesquad #indianmemes #deepfriedmemes #minecraftmemes",
        "#gamingmemes #cancermemes #edgymemesforedgyteens #immortalmemes #funniestmemes #desimemes #memesgraciosos",
        "#tiktok #fights #nsfw #cancer #funny"
    ]

searchTags = [
    "#nsfwmemes", "#tiktokmemes", "#dankmemes", "#bestmemes", "#gamingmemes", "#edgymemes", "#offensivememes"
]

captions = [
    "M3 try1ng to 4du7","Wh3n you'r3 ov3r 17","Fr1d4y f33ls","L1f3 in 4 nu7473ll","Mood sw1ngs b3 l1k3",
    "Sarc4sm 1s my lov3 l4ngu4g3","Wh3n you try to di37","B31ng 4n 4dul7 1s h4rd","7h4t 4wkw4rd mom3nt",
    "R34l1ty h1ts h4rd","My f4c3 wh3n","Wh3n you jus7 c4n7","Struggl3 bus","My br41n on Mond4y mornings",
    "Wh3n you'r3 d34d 1ns1d3","Try1ng to b3 produc71v3","Wh3n you'r3 low-k3y 4 ho7 m3ss","Monday blu3s",
    "Wh3n you don'7 c4r3 4nymor3","4dul71ng 1s 4 sc4m"
]

def generateTags():
    toUseTags = []
    for line in hashtags:
        toUseTags.append(random.choice(line.split()))
        toUseTags.append(random.choice(line.split()))
        toUseTags.append(random.choice(line.split()))
        toUseTags.append(random.choice(line.split()))

    toUseTags = set(toUseTags)
    toUseTags = list(toUseTags)
    return toUseTags

