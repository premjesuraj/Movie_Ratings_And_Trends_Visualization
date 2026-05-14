"""
=============================================================
  Movie Ratings & Trends Visualization — IMDb Dataset
  OUTPUT: Single self-contained HTML file (no server needed)
  Libraries: pandas, seaborn, plotly, matplotlib
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")           # non-interactive backend — safe for Spyder
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import base64
import io
import warnings
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════
#  1.  DATASET  (replace with pd.read_csv("imdb.csv") if you
#      have the real file — keep the same column names)
# ═══════════════════════════════════════════════════════════
np.random.seed(42)

genres = ["Action","Drama","Comedy","Thriller","Romance",
          "Sci-Fi","Horror","Animation","Documentary","Adventure"]
genre_base = {"Action":6.5,"Drama":7.2,"Comedy":6.3,"Thriller":7.0,
              "Romance":6.6,"Sci-Fi":7.1,"Horror":5.9,"Animation":7.5,
              "Documentary":7.4,"Adventure":6.8}

# ── Real IMDb movie titles per genre ────────────────────────────────────────
genre_titles = {
    "Action": [
        "The Dark Knight","Mad Max: Fury Road","Die Hard","Gladiator","John Wick",
        "The Terminator","Speed","Mission: Impossible","Heat","Top Gun: Maverick",
        "The Raid","Crouching Tiger Hidden Dragon","Avengers: Endgame","Black Panther",
        "Edge of Tomorrow","Inception","Skyfall","Casino Royale","The Matrix",
        "Iron Man","Thor: Ragnarok","Captain America: Civil War","Wonder Woman",
        "Man of Steel","Batman v Superman","Aquaman","Shazam","The Suicide Squad",
        "Fast & Furious","The Rock","Con Air","Face/Off","Broken Arrow",
        "Point Break","Speed Racer","Wanted","Salt","Atomic Blonde",
        "The Bourne Identity","The Bourne Supremacy","The Bourne Ultimatum",
        "Taken","96 Hours","The Equalizer","Jack Reacher","Unstoppable",
        "Non-Stop","The Grey","Sicario","Hell or High Water",
        "Logan","Deadpool","X-Men: Days of Future Past","Doctor Strange",
        "Ant-Man","Spider-Man: No Way Home","Black Widow","Eternals",
        "Shang-Chi","No Time to Die","Dunkirk","Interstellar","Tenet",
        "The Dark Knight Rises","Batman Begins","Pacific Rim","Godzilla",
        "King Kong","Transformers","G.I. Joe","RoboCop","Total Recall",
        "Predator","The Expendables","Commando","First Blood","Rambo",
        "Lethal Weapon","Beverly Hills Cop","48 Hrs","Running Man","Cobra",
        "Hard to Kill","Out for Justice","Under Siege","Above the Law",
        "Fire Down Below","The Glimmer Man","Exit Wounds","Half Past Dead",
        "Cradle 2 the Grave","Belly of the Beast","Out for a Kill",
        "The Foreigner","Assassination Games","A Good Day to Die Hard",
    ],
    "Drama": [
        "The Shawshank Redemption","The Godfather","Schindler's List","Forrest Gump",
        "12 Angry Men","One Flew Over the Cuckoo's Nest","Goodfellas","Fight Club",
        "The Silence of the Lambs","American Beauty","A Beautiful Mind","Rain Man",
        "The Green Mile","Million Dollar Baby","Good Will Hunting","Dead Poets Society",
        "Whiplash","Spotlight","The Social Network","Black Swan","Requiem for a Dream",
        "There Will Be Blood","No Country for Old Men","The Departed","Mystic River",
        "21 Grams","Babel","Crash","Traffic","Magnolia","Boogie Nights",
        "Adaptation","Eternal Sunshine of the Spotless Mind","Lost in Translation",
        "Her","Manchester by the Sea","Moonlight","Birdman","The Revenant",
        "12 Years a Slave","Dallas Buyers Club","Silver Linings Playbook",
        "The King's Speech","The Artist","Argo","Lincoln","Django Unchained",
        "The Grand Budapest Hotel","Boyhood","Nightcrawler","Gone Girl",
        "Prisoners","Zodiac","Zodiac","Zodiac","The Hurt Locker","Zero Dark Thirty",
        "American Sniper","Hacksaw Ridge","Dunkirk","1917","Saving Private Ryan",
        "Full Metal Jacket","Apocalypse Now","Platoon","Born on the Fourth of July",
        "Coming Home","The Deer Hunter","Heaven & Earth","JFK","Nixon",
        "Ali","Malcolm X","Selma","Marshall","Just Mercy","The Trial of the Chicago 7",
        "Judas and the Black Messiah","The Two Popes","Marriage Story","Roma",
        "Parasite","Portrait of a Lady on Fire","The Favourite","Cold War",
        "Three Billboards Outside Ebbing Missouri","Lady Bird","Call Me by Your Name",
        "Phantom Thread","Darkest Hour","The Post","Molly's Game","I Tonya",
        "Sully","Bridge of Spies","The Big Short","Spotlight","The Revenant",
        "Mad Max: Fury Road","The Martian","Room","Brooklyn","Carol",
    ],
    "Comedy": [
        "Some Like It Hot","Annie Hall","The Big Lebowski","Groundhog Day",
        "Ferris Bueller's Day Off","Home Alone","Mrs. Doubtfire","Clueless",
        "The Truman Show","Office Space","Superbad","Knocked Up","The Hangover",
        "Bridesmaids","Anchorman","Step Brothers","Talladega Nights","Blades of Glory",
        "Semi-Pro","Nacho Libre","Stranger Than Fiction","Adaptation",
        "Lost in Translation","About Schmidt","As Good as It Gets","Jerry Maguire",
        "You've Got Mail","When Harry Met Sally","Sleepless in Seattle",
        "My Best Friend's Wedding","Notting Hill","Four Weddings and a Funeral",
        "Love Actually","Bridget Jones's Diary","The Full Monty","Calendar Girls",
        "About a Boy","High Fidelity","Grosse Pointe Blank","Say Anything",
        "Rushmore","The Royal Tenenbaums","The Life Aquatic","Bottle Rocket",
        "Punch-Drunk Love","I Heart Huckabees","Eternal Sunshine","Synecdoche New York",
        "Adaptation","Being John Malkovich","American Splendor","Sideways",
        "Election","Heathers","Pump Up the Volume","Reality Bites","Empire Records",
        "Clerks","Mallrats","Chasing Amy","Dogma","Jay and Silent Bob Strike Back",
        "Zack and Miri Make a Porno","Observe and Report","Paul","Cop Out",
        "The 40-Year-Old Virgin","Funny People","This Is 40","Trainwreck",
        "Judd Apatow","Neighbors","Bad Neighbors","Bad Teacher","Bad Moms",
        "Rough Night","Girls Trip","Game Night","Ready or Not","The Other Guys",
        "Get Him to the Greek","Forgetting Sarah Marshall","I Love You Man",
        "Role Models","Tropic Thunder","Pineapple Express","Observe and Report",
        "Scott Pilgrim vs. the World","Nick and Norah's Infinite Playlist",
        "Juno","Little Miss Sunshine","Napoleon Dynamite","Garden State",
        "The Squid and the Whale","Happiness","Welcome to the Dollhouse",
    ],
    "Thriller": [
        "Psycho","Rear Window","Vertigo","North by Northwest","The Birds",
        "Se7en","The Usual Suspects","Memento","Oldboy","Gone Girl",
        "Prisoners","Zodiac","The Girl with the Dragon Tattoo","Chinatown",
        "Rosemary's Baby","The Shining","Cape Fear","Basic Instinct",
        "Fatal Attraction","Dressed to Kill","Body Double","Blue Velvet",
        "Wild at Heart","Mulholland Drive","Lost Highway","Twin Peaks: Fire Walk with Me",
        "Manhunter","Hannibal","Red Dragon","Silence of the Lambs","Copycat",
        "Taking Lives","Along Came a Spider","Kiss the Girls","The Bone Collector",
        "Seven","The Talented Mr. Ripley","Ripley's Game","Purple Noon",
        "American Psycho","The Machinist","Shutter Island","Black Swan",
        "Fracture","Primal Fear","Presumed Innocent","Jagged Edge","Suspect",
        "The Firm","The Pelican Brief","The Client","A Time to Kill",
        "Double Jeopardy","The General's Daughter","Domestic Disturbance",
        "Unlawful Entry","Pacific Heights","Single White Female","The Hand That Rocks the Cradle",
        "Sleeping with the Enemy","Fear","The Crush","Obsessed","Swimfan",
        "Swimfan","The Perfect Guy","No Good Deed","Acrimony","Slender Man",
        "Countdown","Escape Room","Escape Room: Tournament of Champions",
        "The Hunt","Ready or Not","Parasite","Get Out","Us","Nope",
        "Knives Out","Glass Onion","Rian Johnson","Clue","Murder on the Orient Express",
        "Death on the Nile","The Mousetrap","Ten Little Indians","And Then There Were None",
        "Crooked House","Ordeal by Innocence","The ABC Murders","Curtain",
    ],
    "Romance": [
        "Casablanca","Roman Holiday","Breakfast at Tiffany's","An Affair to Remember",
        "Doctor Zhivago","Out of Africa","The English Patient","Cold Mountain",
        "Titanic","Romeo + Juliet","Shakespeare in Love","Moulin Rouge!",
        "Chicago","La La Land","The Notebook","A Walk to Remember",
        "Message in a Bottle","Dear John","The Lucky One","Safe Haven",
        "Nights in Rodanthe","The Best of Me","Longest Ride","See Me",
        "Five Feet Apart","After","The Kissing Booth","To All the Boys I've Loved Before",
        "P.S. I Love You","Love Rosie","Me Before You","The Fault in Our Stars",
        "The Vow","Safe Haven","The Choice","Everything Everything",
        "Love Simon","Call Me by Your Name","Brokeback Mountain","Moonlight",
        "Carol","Portrait of a Lady on Fire","Blue Is the Warmest Color",
        "Weekend","Beginners","The Kids Are All Right","Far from Heaven",
        "Brokeback Mountain","Milk","Philadelphia","The Normal Heart",
        "And the Band Played On","Longtime Companion","Making Love","Personal Best",
        "Desert Hearts","Go Fish","But I'm a Cheerleader","D.E.B.S.",
        "Imagine Me & You","Gray Matters","The L Word","Fingersmith",
        "Affinity","Tipping the Velvet","Oranges Are Not the Only Fruit",
        "My Summer of Love","Aimee & Jaguar","Saving Face","Nina's Heavenly Delights",
        "Loving Annabelle","Bloomington","Below Her Mouth","Vita & Virginia",
        "Portrait of a Lady on Fire","Ammonite","The World to Come","Summerland",
        "The Half of It","Elisa & Marcela","Disobedience","The Price of Salt",
        "Elena Undone","When Night Is Falling","Mädchen in Uniform","Therese and Isabelle",
    ],
    "Sci-Fi": [
        "2001: A Space Odyssey","Blade Runner","The Matrix","Inception","Interstellar",
        "Arrival","Gravity","The Martian","Ex Machina","Annihilation",
        "Moon","Coherence","Primer","Predestination","Looper",
        "Edge of Tomorrow","Source Code","Minority Report","Total Recall",
        "RoboCop","Terminator 2: Judgment Day","The Terminator","T3: Rise of the Machines",
        "Terminator Salvation","Terminator: Dark Fate","Terminator: Genisys",
        "Star Wars: A New Hope","The Empire Strikes Back","Return of the Jedi",
        "The Phantom Menace","Attack of the Clones","Revenge of the Sith",
        "The Force Awakens","The Last Jedi","The Rise of Skywalker","Rogue One","Solo",
        "Star Trek","Star Trek: The Wrath of Khan","Star Trek III","Star Trek IV",
        "Star Trek V","Star Trek VI","Star Trek: Generations","Star Trek: First Contact",
        "Star Trek: Insurrection","Star Trek: Nemesis","Star Trek (2009)","Star Trek Into Darkness",
        "Star Trek Beyond","Close Encounters of the Third Kind","E.T.","Contact",
        "Signs","War of the Worlds","Independence Day","Men in Black","Mars Attacks!",
        "District 9","Elysium","Chappie","Alita: Battle Angel","Ghost in the Shell",
        "Akira","Neon Genesis Evangelion","Paprika","Metropolis","The Day the Earth Stood Still",
        "Forbidden Planet","Invasion of the Body Snatchers","The Blob","Them!",
        "The Thing from Another World","The Thing","The Fly","Videodrome","Scanners",
        "Naked Lunch","Crash","eXistenZ","A History of Violence","Eastern Promises",
        "A Dangerous Method","Maps to the Stars","Cosmopolis","Possessor","Crimes of the Future",
    ],
    "Horror": [
        "The Exorcist","Halloween","A Nightmare on Elm Street","Friday the 13th",
        "The Texas Chain Saw Massacre","Psycho","The Shining","Rosemary's Baby",
        "The Omen","Poltergeist","Carrie","Christine","It","It Chapter Two",
        "Pet Sematary","Children of the Corn","The Mist","1408","Dreamcatcher",
        "Misery","Dolores Claiborne","Gerald's Game","The Haunting of Hill House",
        "Shirley Jackson","Hell House LLC","The Innkeepers","The House of the Devil",
        "Ti West","The Sacrament","In a Valley of Violence","Blumhouse",
        "Get Out","Us","Nope","The Purge","Sinister","Insidious","The Conjuring",
        "Annabelle","Annabelle: Creation","The Nun","The Curse of La Llorona",
        "Lights Out","Hush","Oculus","Ouija: Origin of Evil","Happy Death Day",
        "M3GAN","Five Nights at Freddy's","Scream","Scream 2","Scream 3",
        "Scream 4","Scream (2022)","Scream VI","I Know What You Did Last Summer",
        "Urban Legend","Final Destination","Final Destination 2","The Ring",
        "The Grudge","Dark Water","Pulse","One Missed Call","Shutter",
        "A Tale of Two Sisters","Audition","Battle Royale","Ichi the Killer",
        "Ringu","Ju-On","Dark Water","Noroi","Paranormal Activity",
        "REC","Cloverfield","Chronicle","The Bay","Trollhunter",
        "V/H/S","The Blair Witch Project","Book of Shadows","The Visit",
        "Split","Glass","Unbreakable","Signs","The Village","Lady in the Water",
        "The Happening","Devil","After Earth","The Last Airbender","Old","Knock at the Cabin",
    ],
    "Animation": [
        "Spirited Away","Princess Mononoke","My Neighbor Totoro","Nausicaä",
        "Castle in the Sky","Kiki's Delivery Service","Only Yesterday","Pom Poko",
        "Whisper of the Heart","The Cat Returns","Howl's Moving Castle","Ponyo",
        "The Secret World of Arrietty","From Up on Poppy Hill","The Wind Rises",
        "The Tale of the Princess Kaguya","When Marnie Was There","The Red Turtle",
        "Grave of the Fireflies","Isao Takahata","Panda! Go, Panda!","Hols: Prince of the Sun",
        "Toy Story","Toy Story 2","Toy Story 3","Toy Story 4","A Bug's Life",
        "Monsters, Inc.","Monsters University","Finding Nemo","Finding Dory",
        "The Incredibles","Incredibles 2","Cars","Cars 2","Cars 3","Ratatouille",
        "WALL-E","Up","Brave","Inside Out","Inside Out 2","Coco","Soul","Luca",
        "Turning Red","Lightyear","Elemental","The Lion King","The Little Mermaid",
        "Beauty and the Beast","Aladdin","Mulan","Tarzan","Hercules","The Hunchback of Notre Dame",
        "The Emperor's New Groove","Lilo & Stitch","Brother Bear","Home on the Range",
        "Chicken Little","Meet the Robinsons","Bolt","The Princess and the Frog",
        "Tangled","Winnie the Pooh","Wreck-It Ralph","Ralph Breaks the Internet",
        "Frozen","Frozen II","Big Hero 6","Zootopia","Moana","Encanto","Strange World",
        "Wish","The Shrek","Shrek 2","Shrek the Third","Shrek Forever After",
        "Puss in Boots","Puss in Boots: The Last Wish","Madagascar","Over the Hedge",
        "Bee Movie","Kung Fu Panda","Kung Fu Panda 2","Kung Fu Panda 3","How to Train Your Dragon",
    ],
    "Documentary": [
        "Man on Wire","Won't You Be My Neighbor?","Free Solo","13th","I Am Not Your Negro",
        "Bowling for Columbine","Fahrenheit 9/11","An Inconvenient Truth","Super Size Me",
        "Blackfish","The Cove","Food, Inc.","Fed Up","Forks Over Knives","PlantPure Nation",
        "What the Health","Cowspiracy","Seaspiracy","Earthlings","Dominion",
        "Amy","Montage of Heck","Searching for the Wrong-Eyed Jesus","The Last Waltz",
        "Gimme Shelter","Don't Look Back","No Direction Home","I'm Still Here",
        "Shut Up & Sing","DiG!","Anvil: The Story of Anvil","Metallica: Some Kind of Monster",
        "The Eyes of Tammy Faye","Capturing the Friedmans","Dear Zachary",
        "The Act of Killing","The Look of Silence","Shoah","Night and Fog",
        "Triumph of the Will","The Battle of the Bulge","Patton","A Bridge Too Far",
        "Das Boot","The Thin Red Line","Letters from Iwo Jima","Flags of Our Fathers",
        "The Pacific","Band of Brothers","Generation Kill","Restrepo","Korengal",
        "Which Way Is the Front Line from Here?","The Waiting Room","The House I Live In",
        "The Invisible War","The Hunting Ground","On the Record","Allen v. Farrow",
        "Tiger King","The Last Dance","OJ: Made in America","ESPN 30 for 30",
        "Hoop Dreams","When We Were Kings","Senna","Icarus","Athlete A","Bad Sport",
        "The Two Escobars","Four Falls of Buffalo","The Book of Manning","Broke",
        "Kareem Abdul-Jabbar","Magic & Bird: A Courtship of Rivals","Jordan Rides the Bus",
    ],
    "Adventure": [
        "Indiana Jones and the Raiders of the Lost Ark","Temple of Doom","Last Crusade",
        "Kingdom of the Crystal Skull","The Mummy","The Mummy Returns","The Mummy: Tomb of the Dragon Emperor",
        "National Treasure","National Treasure: Book of Secrets","The Da Vinci Code",
        "Angels & Demons","Inferno","Origin","The Lost Symbol","Jurassic Park",
        "The Lost World: Jurassic Park","Jurassic Park III","Jurassic World",
        "Jurassic World: Fallen Kingdom","Jurassic World Dominion","The Land Before Time",
        "Ice Age","Ice Age: The Meltdown","Ice Age: Dawn of the Dinosaurs",
        "Ice Age: Continental Drift","Ice Age: Collision Course","The Croods","The Croods: A New Age",
        "Epic","Rio","Rio 2","Ferdinand","The Pirates! Band of Misfits","Treasure Planet",
        "Atlantis: The Lost Empire","The Road to El Dorado","The Prince of Egypt",
        "Sinbad: Legend of the Seven Seas","Joseph: King of Dreams","The Swan Princess",
        "Quest for Camelot","The King and I","Anastasia","Balto","All Dogs Go to Heaven",
        "An American Tail","An American Tail: Fievel Goes West","Thumbelina",
        "The Pebble and the Penguin","Rock-a-Doodle","A Troll in Central Park",
        "The Pirates of Dark Water","Pirates of the Caribbean","Dead Man's Chest",
        "At World's End","On Stranger Tides","Dead Men Tell No Tales",
        "The Goonies","Stand by Me","The Sandlot","Little Giants","Rookie of the Year",
        "Angels in the Outfield","Heavyweights","Mighty Ducks","D2: The Mighty Ducks",
        "D3: The Mighty Ducks","The Big Green","Air Bud","Homeward Bound",
        "Homeward Bound II: Lost in San Francisco","Beethoven","Beethoven's 2nd",
    ],
}

# Build N rows by sampling from real title lists
all_rows = []
N=1000;
for genre, title_list in genre_titles.items():
    n_genre = N // len(genres)
    sampled = np.random.choice(title_list, size=n_genre, replace=True)
    yrs   = np.random.randint(1970, 2024, n_genre)
    base  = genre_base[genre]
    rats  = np.clip(base + (yrs-1970)*0.005 + np.random.normal(0,0.8,n_genre), 1, 10).round(1)
    votes = (np.random.pareto(1.5, n_genre) * 20_000 + 500).astype(int)
    rev   = np.clip((rats-4)*40 + np.random.normal(0,60,n_genre)
                    + (yrs-1970)*1.2, 0.5, 900).round(1)
    runtimes = np.clip(np.random.normal(110,25,n_genre),70,210).astype(int)
    for i in range(n_genre):
        all_rows.append({
            "title":     sampled[i],
            "genre":     genre,
            "year":      yrs[i],
            "rating":    rats[i],
            "votes":     votes[i],
            "revenue_m": rev[i],
            "runtime":   runtimes[i],
        })

df = pd.DataFrame(all_rows)
# Drop duplicate title+year combos to keep it realistic
df = df.drop_duplicates(subset=["title","year"]).reset_index(drop=True)
N  = len(df)

df["decade"] = ((df["year"] // 10) * 10).astype(str) + "s"
decade_order = sorted(df["decade"].unique())
df.to_csv("imdb_dataset.csv", index=False)
print("CSV dataset exported successfully!")

print("Dataset ready:", df.shape)

# ═══════════════════════════════════════════════════════════
#  2.  MATPLOTLIB / SEABORN  → base64-encoded PNG
# ═══════════════════════════════════════════════════════════
sns.set_theme(style="darkgrid")
palette = sns.color_palette("tab10", n_colors=len(genres))

fig, axes = plt.subplots(3, 2, figsize=(16, 18), facecolor="#0D0D0D")
fig.suptitle("🎬 Movie Ratings & Trends — IMDb Dataset",
             fontsize=20, fontweight="bold", color="white", y=0.98)

for ax in axes.flat:
    ax.set_facecolor("#1A1A2E")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444")

# Plot 1 — Rating distribution
ax = axes[0, 0]
sns.histplot(df["rating"], bins=30, kde=True, color="#E8534A", ax=ax)
ax.axvline(df["rating"].mean(), color="gold", lw=2, linestyle="--",
           label=f"Mean: {df['rating'].mean():.2f}")
ax.set_title("Distribution of IMDb Ratings", fontweight="bold")
ax.set_xlabel("IMDb Rating"); ax.set_ylabel("Count")
ax.legend(labelcolor="white", facecolor="#1A1A2E")

# Plot 2 — Avg rating by genre
ax = axes[0, 1]
avg_genre = df.groupby("genre")["rating"].mean().sort_values()
colors = [palette[genres.index(g)] for g in avg_genre.index]
bars = ax.barh(avg_genre.index, avg_genre.values, color=colors, edgecolor="#333")
ax.bar_label(bars, fmt="%.2f", padding=4, fontsize=9, color="white")
ax.set_xlim(0, 10)
ax.set_title("Average IMDb Rating by Genre", fontweight="bold")
ax.set_xlabel("Average Rating")

# Plot 3 — Avg rating by decade
ax = axes[1, 0]
dec_avg = df.groupby("decade")["rating"].mean().reindex(decade_order)
ax.plot(dec_avg.index, dec_avg.values, marker="o", color="#00BFFF",
        linewidth=2.5, markersize=8)
ax.fill_between(dec_avg.index, dec_avg.values, alpha=0.15, color="#00BFFF")
ax.set_title("Average Rating Trend by Decade", fontweight="bold")
ax.set_xlabel("Decade"); ax.set_ylabel("Average Rating")
ax.tick_params(axis="x", rotation=45)

# Plot 4 — Box plot by genre
ax = axes[1, 1]
order = df.groupby("genre")["rating"].median().sort_values(ascending=False).index
sns.boxplot(data=df, x="genre", y="rating", order=order,
            palette="tab10", ax=ax, width=0.6)
ax.set_title("Rating Distribution by Genre", fontweight="bold")
ax.set_xlabel("Genre"); ax.set_ylabel("Rating")
ax.tick_params(axis="x", rotation=45)

# Plot 5 — Rating vs Revenue
ax = axes[2, 0]
sc = ax.scatter(df["rating"], df["revenue_m"],
                c=df["year"], cmap="plasma", alpha=0.5, s=20)
cb = plt.colorbar(sc, ax=ax); cb.set_label("Year", color="white")
cb.ax.yaxis.set_tick_params(color="white")
plt.setp(cb.ax.yaxis.get_ticklabels(), color="white")
ax.set_title("IMDb Rating vs Box-Office Revenue", fontweight="bold")
ax.set_xlabel("IMDb Rating"); ax.set_ylabel("Revenue (USD Million)")

# Plot 6 — Genre pie
ax = axes[2, 1]
genre_counts = df["genre"].value_counts()
wedges, texts, autotexts = ax.pie(
    genre_counts, labels=genre_counts.index,
    autopct="%1.1f%%", colors=palette, startangle=140, pctdistance=0.82)
for t in texts: t.set_color("white")
for at in autotexts: at.set_fontsize(8); at.set_color("white")
ax.set_title("Movie Count by Genre", fontweight="bold")

plt.tight_layout(rect=[0, 0, 1, 0.97])

# Encode figure to base64
buf = io.BytesIO()
plt.savefig(buf, format="png", dpi=130, bbox_inches="tight",
            facecolor=fig.get_facecolor())
buf.seek(0)
static_b64 = base64.b64encode(buf.read()).decode("utf-8")
plt.close()
print("✅ Static charts encoded")

# ═══════════════════════════════════════════════════════════
#  3.  PLOTLY  → HTML div strings (no external CDN needed)
# ═══════════════════════════════════════════════════════════

def plotly_div(fig, div_id):
    """Return a standalone <div> string for a Plotly figure."""
    return fig.to_html(full_html=False, include_plotlyjs=False, div_id=div_id)

DARK = "#0D0D0D"
PANEL = "#1A1A2E"
TEXT  = "#E0E0E0"
common = dict(template="plotly_dark", paper_bgcolor=DARK,
              plot_bgcolor=PANEL, font=dict(color=TEXT))

# Chart A — Avg rating by genre
avg_g = df.groupby("genre")["rating"].mean().sort_values(ascending=False).reset_index()
figA = go.Figure(go.Bar(
    x=avg_g["genre"], y=avg_g["rating"],
    marker=dict(color=avg_g["rating"], colorscale="Viridis", showscale=True),
    text=avg_g["rating"].round(2), textposition="outside",
))
figA.update_layout(**common, title="Average Rating by Genre",
                   height=420, xaxis_title="Genre", yaxis_title="Avg Rating",
                   yaxis_range=[0, 10])

# Chart B — Votes vs Rating scatter
figB = px.scatter(df, x="votes", y="rating", color="genre",
                  hover_name="title", opacity=0.6, size_max=8,
                  color_discrete_sequence=px.colors.qualitative.Vivid,
                  title="Votes vs Rating (coloured by Genre)",
                  labels={"votes":"Votes","rating":"Rating"})
figB.update_layout(**common, height=420)
figB.update_traces(marker=dict(size=5))

# Chart C — Movies released per year
per_year = df.groupby("year").size().reset_index(name="count")
figC = go.Figure(go.Scatter(
    x=per_year["year"], y=per_year["count"],
    mode="lines+markers", fill="tozeroy",
    line=dict(color="#00BFFF", width=2),
    marker=dict(size=5),
))
figC.update_layout(**common, title="Movies Released per Year",
                   height=380, xaxis_title="Year", yaxis_title="Count")

# Chart D — Runtime vs Rating
figD = px.scatter(df, x="runtime", y="rating", color="revenue_m",
                  hover_name="title", opacity=0.6,
                  color_continuous_scale="Plasma",
                  title="Runtime vs Rating (coloured by Revenue)",
                  labels={"runtime":"Runtime (min)","rating":"Rating",
                          "revenue_m":"Revenue $M"})
figD.update_layout(**common, height=420)
figD.update_traces(marker=dict(size=5))

# Chart E — Revenue by decade (box)
figE = go.Figure()
for i, dec in enumerate(decade_order):
    sub = df[df["decade"] == dec]
    figE.add_trace(go.Box(y=sub["revenue_m"], name=dec, showlegend=False,
                          marker_color=px.colors.sequential.Plasma[
                              i % len(px.colors.sequential.Plasma)]))
figE.update_layout(**common, title="Box-Office Revenue by Decade",
                   height=420, xaxis_title="Decade", yaxis_title="Revenue ($M)")

# Chart F — Genre × Decade heatmap
heat = df.pivot_table(index="genre", columns="decade",
                      values="rating", aggfunc="mean")
figF = go.Figure(go.Heatmap(
    z=heat.values, x=heat.columns.tolist(), y=heat.index.tolist(),
    colorscale="RdYlGn", zmin=5, zmax=8.5,
    colorbar=dict(title="Rating"),
    text=np.round(heat.values, 2), texttemplate="%{text}",
))
figF.update_layout(**common, title="Avg Rating Heatmap: Genre × Decade", height=420)

# Chart G — Top 10 rated movies (table)
top10 = (df[df["votes"] >= 3000]
         .nlargest(10, "rating")
         [["title","genre","year","rating","votes","revenue_m"]]
         .reset_index(drop=True))
top10.index += 1
figG = go.Figure(go.Table(
    header=dict(
        values=["#","Title","Genre","Year","Rating","Votes","Revenue $M"],
        fill_color="#4C72B0", font=dict(color="white", size=13),
        align="center", height=36,
    ),
    cells=dict(
        values=[top10.index, top10["title"], top10["genre"],
                top10["year"], top10["rating"],
                top10["votes"].apply(lambda x: f"{x:,}"),
                top10["revenue_m"]],
        fill_color=[[PANEL, "#16213E"] * 5],
        font=dict(color=TEXT, size=12),
        align="center", height=30,
    ),
))
figG.update_layout(**common, title="Top 10 Highest-Rated Movies", height=420)

print("✅ Plotly charts built")

# ═══════════════════════════════════════════════════════════
#  4.  ASSEMBLE FULL HTML FILE
# ═══════════════════════════════════════════════════════════

import plotly.io as pio
plotlyjs_cdn = '<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>'

divA = plotly_div(figA, "chartA")
divB = plotly_div(figB, "chartB")
divC = plotly_div(figC, "chartC")
divD = plotly_div(figD, "chartD")
divE = plotly_div(figE, "chartE")
divF = plotly_div(figF, "chartF")
divG = plotly_div(figG, "chartG")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>IMDb Movie Ratings & Trends Dashboard</title>
{plotlyjs_cdn}
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@300;400;600&display=swap');

  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background: #0D0D0D;
    color: #E0E0E0;
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
  }}

  /* ── Header ── */
  header {{
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    padding: 40px 24px 30px;
    text-align: center;
    border-bottom: 2px solid #f5c518;
    position: relative;
    overflow: hidden;
  }}
  header::before {{
    content: "";
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(245,197,24,.15) 0%, transparent 70%);
  }}
  header h1 {{
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(1.6rem, 4vw, 2.8rem);
    color: #f5c518;
    letter-spacing: 2px;
    position: relative;
  }}
  header p {{
    margin-top: 10px;
    font-size: 0.95rem;
    color: #aaa;
    position: relative;
  }}
  .imdb-badge {{
    display: inline-block;
    background: #f5c518;
    color: #000;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 6px;
    margin-bottom: 12px;
  }}

  /* ── Stats bar ── */
  .stats-bar {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 16px;
    padding: 20px 24px;
    background: #111;
    border-bottom: 1px solid #222;
  }}
  .stat-card {{
    background: #1A1A2E;
    border: 1px solid #2a2a4a;
    border-radius: 10px;
    padding: 14px 28px;
    text-align: center;
    min-width: 140px;
  }}
  .stat-card .val {{
    font-size: 1.8rem;
    font-weight: 700;
    color: #f5c518;
    font-family: 'Orbitron', sans-serif;
  }}
  .stat-card .lbl {{
    font-size: 0.78rem;
    color: #888;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }}

  /* ── Section labels ── */
  .section-label {{
    text-align: center;
    margin: 36px 0 8px;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.85rem;
    letter-spacing: 3px;
    color: #f5c518;
    text-transform: uppercase;
  }}
  .divider {{
    width: 60px; height: 2px;
    background: #f5c518;
    margin: 0 auto 24px;
    border-radius: 2px;
  }}

  /* ── Grid layouts ── */
  .main {{ max-width: 1400px; margin: 0 auto; padding: 0 16px 60px; }}

  .grid-2 {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(560px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
  }}
  .grid-1 {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
    margin-bottom: 20px;
  }}

  /* ── Chart card ── */
  .card {{
    background: #1A1A2E;
    border: 1px solid #2a2a4a;
    border-radius: 14px;
    overflow: hidden;
    transition: box-shadow .25s;
  }}
  .card:hover {{
    box-shadow: 0 0 24px rgba(245,197,24,.18);
  }}
  .card-header {{
    padding: 14px 20px;
    background: linear-gradient(90deg, #16213E, #1A1A2E);
    border-bottom: 1px solid #2a2a4a;
    font-size: 0.82rem;
    color: #f5c518;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-weight: 600;
  }}
  .card-body {{ padding: 8px; }}

  /* ── Static image card ── */
  .static-img {{
    width: 100%;
    border-radius: 8px;
    display: block;
  }}

  /* ── Footer ── */
  footer {{
    text-align: center;
    padding: 24px;
    background: #111;
    color: #555;
    font-size: 0.8rem;
    border-top: 1px solid #222;
  }}
</style>
</head>
<body>

<!-- ── Header ─────────────────────────────────────────── -->
<header>
  <div class="imdb-badge">IMDb</div>
  <h1>🎬 Movie Ratings &amp; Trends Dashboard</h1>
  <p>Comprehensive analysis of {N:,} movies &nbsp;|&nbsp; 1970 – 2023 &nbsp;|&nbsp;
     Pandas · Seaborn · Plotly · Matplotlib</p>
</header>

<!-- ── Stats bar ──────────────────────────────────────── -->
<div class="stats-bar">
  <div class="stat-card">
    <div class="val">{N:,}</div>
    <div class="lbl">Total Movies</div>
  </div>
  <div class="stat-card">
    <div class="val">{df['rating'].mean():.2f}</div>
    <div class="lbl">Avg Rating</div>
  </div>
  <div class="stat-card">
    <div class="val">{df['genre'].nunique()}</div>
    <div class="lbl">Genres</div>
  </div>
  <div class="stat-card">
    <div class="val">{df['year'].min()}–{df['year'].max()}</div>
    <div class="lbl">Year Range</div>
  </div>
  <div class="stat-card">
    <div class="val">${df['revenue_m'].mean():.0f}M</div>
    <div class="lbl">Avg Revenue</div>
  </div>
  <div class="stat-card">
    <div class="val">{df['votes'].sum():,}</div>
    <div class="lbl">Total Votes</div>
  </div>
</div>

<div class="main">

  <!-- ── Section 1: Static Overview ── -->
  <p class="section-label">Static Overview (Seaborn + Matplotlib)</p>
  <div class="divider"></div>
  <div class="grid-1">
    <div class="card">
      <div class="card-header">📊 6-Panel Static Analysis</div>
      <div class="card-body">
        <img class="static-img"
             src="data:image/png;base64,{static_b64}"
             alt="Static IMDb Charts"/>
      </div>
    </div>
  </div>

  <!-- ── Section 2: Interactive Charts ── -->
  <p class="section-label">Interactive Charts (Plotly)</p>
  <div class="divider"></div>

  <div class="grid-2">
    <div class="card">
      <div class="card-header">🏆 Avg Rating by Genre</div>
      <div class="card-body">{divA}</div>
    </div>
    <div class="card">
      <div class="card-header">🔵 Votes vs Rating</div>
      <div class="card-body">{divB}</div>
    </div>
  </div>

  <div class="grid-2">
    <div class="card">
      <div class="card-header">📅 Movies Released per Year</div>
      <div class="card-body">{divC}</div>
    </div>
    <div class="card">
      <div class="card-header">⏱️ Runtime vs Rating</div>
      <div class="card-body">{divD}</div>
    </div>
  </div>

  <div class="grid-2">
    <div class="card">
      <div class="card-header">💰 Revenue by Decade</div>
      <div class="card-body">{divE}</div>
    </div>
    <div class="card">
      <div class="card-header">🌡️ Genre × Decade Rating Heatmap</div>
      <div class="card-body">{divF}</div>
    </div>
  </div>

  <!-- ── Section 3: Top 10 Table ── -->
  <p class="section-label">Top 10 Highest-Rated Movies</p>
  <div class="divider"></div>
  <div class="grid-1">
    <div class="card">
      <div class="card-header">🥇 Top 10 Table</div>
      <div class="card-body">{divG}</div>
    </div>
  </div>

</div><!-- /main -->

<footer>
  Generated with Python · Pandas · Seaborn · Matplotlib · Plotly
  &nbsp;|&nbsp; Data: Synthetic IMDb-style dataset
</footer>

</body>
</html>"""

# ═══════════════════════════════════════════════════════════
#  5.  WRITE THE FILE
# ═══════════════════════════════════════════════════════════
OUTPUT_FILE = "imdb_dashboard.html"   # ← change path if needed

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅  Done!  Open  '{OUTPUT_FILE}'  in any browser.")
print(f"   File size: {len(html) / 1024:.1f} KB")
print(df.head())