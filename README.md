# Hi-Five

Anonymous friend-matching on personality, not photos: take an OCEAN assessment, get matched by vector similarity, chat under a whimsical alias for 48 hours, then decide whether to reveal.

Built in 36-ish hours at SASEhack Fall 2024 (University of Cincinnati), October 2024.

## What it does

You answer free-text prompts for each of the five OCEAN traits (Openness, Conscientiousness, Extroversion, Agreeableness, Neuroticism) and pick some interest tags. The app embeds your answers, finds the users whose vectors sit closest to yours, and surfaces them as swipeable cards under a randomly generated alias like "Whimsical Wombat" — no name, no photo.

Swipe right on someone and, if they swipe back, you get a real-time chat. New matches start on a 48-hour clock. If both people opt to reveal before it runs out, the alias drops and the account goes into a permanent friends list. If not, the match just expires.

The bet was that swiping on personality compatibility surfaces better friend matches than swiping on a photo.

## How it works

- **Frontend**: Next.js + MUI. Onboarding takes the OCEAN prompts and tags, then renders swipeable user cards, a matches screen, a friends list, and chat (`app/components/`, `app/api/chat/`).
- **Embeddings**: each OCEAN answer gets embedded separately (`src/server/API/generate_embeds.py`) via BGE-en-icl, with RoBERTa-base-go-emotions in the mix for the emotional-tone side of the answers. Each person ends up with five stored vectors — `O_embed`, `C_embed`, `E_embed`, `A_embed`, `N_embed` — rather than one blended one.
- **Storage**: Neo4j. Users are `Person` nodes carrying their five embeddings, tags, alias, and bio (`src/server/neo4j_db/CRUD.py`, `graph.py`).
- **Matching**: a Cypher query pulls every `Person` node and computes cosine similarity per trait against the querying user directly in the graph (`src/server/neo4j_db/relationship_scoring.py`). The five per-trait similarities get averaged, then blended with Jaccard similarity over interest tags: `0.6 * vector_similarity + 0.4 * tag_jaccard`. Top matches come back through a Flask API (`src/server/app/app.py`) that the Next.js frontend calls for cards, swipes, friend requests, and messages.
- **Reveal window**: friendship duration and the 48-hour countdown are tracked client-side off `friendshipStartDate` (`app/Utils/getFriendshipDuration.tsx`).

## Run the UI

From the repository root, install the JavaScript dependencies and start the Next.js app:

```sh
npm install
npm run dev
```

Open `http://localhost:3000`. This starts the UI only. The Flask API requires Neo4j and a separate embedding service; the checked-in backend still contains placeholder Neo4j connection values and an embedding endpoint outside this repository, so a working full-stack setup cannot be reproduced from this checkout alone.

## Prototype

`prototype/ocean_matching_demo.py` draws the matching pipeline as designed at the hackathon — no synthetic users, no measured results, just the flow and the real scoring formula pulled from `src/server/neo4j_db/relationship_scoring.py`: `score = 0.6 * vector_similarity + 0.4 * tag_jaccard`, where `vector_similarity` is the mean cosine similarity across the five OCEAN trait embeddings and `tag_jaccard` is Jaccard similarity over interest tags. It also lays out the 48-hour anonymous chat window as a timeline and the reveal/dissolve branch at the end of it.

The diagram needs Python and Matplotlib. Run it from the repository root:

```sh
python -m pip install matplotlib
python prototype/ocean_matching_demo.py
```

It writes one PNG to `prototype/figures/` (ignored by Git; regenerate locally):

![Hi-Five matching pipeline: OCEAN assessment and interest tags feed embeddings and tag sets, combined into score = 0.6 * vector_similarity + 0.4 * tag_jaccard, producing a match that opens a 48-hour anonymous chat window, after which both people opting in reveals identities or the match dissolves](https://vircgxpcwyvniemqmdyi.supabase.co/storage/v1/object/public/media/writing/Hi-Five/matching_flow.png)

## Team

- Raihan Rafeek — [rai-1975.com](https://www.rai-1975.com/)
- Shawn Lasrado — [github.com/ShawnJoshua03](https://github.com/ShawnJoshua03)
- Shashwat Mishra
- Arya Garg — on the team, but honestly: his code never made it off his machine that weekend, so the git history and the Devpost team list only show the other three.

Originally hacked together in [Rai1975/SASEHackProject](https://github.com/Rai1975/SASEHackProject).

## Links

- [Devpost project](https://devpost.com/software/hi-five-dt0gvj)
- [Writeup](https://aryagarg23.com/writing/hi-five)
- [aryagarg23.com](https://aryagarg23.com)
- [Devpost profile](https://devpost.com/Aryagarg23)

## More hackathon builds

- [Gyrus](https://github.com/Aryagarg23/Gyrus) — agentic browser that supports curiosity instead of replacing it (WeaveHacks 2025)
- [WhiteBox](https://github.com/Aryagarg23/WhiteBox) — traceable GraphRAG over medical literature (Future of Data 2024, 1st place)
- [G-Code-Assembler](https://github.com/Aryagarg23/G-Code-Assembler) — G-code assembly + STL visualization (MakeUC 2024, Kinetic Vision winner)
- [Terminally-Addicted](https://github.com/Aryagarg23/Terminally-Addicted) — Spotify, GitHub, GPT and YouTube without leaving the terminal (HackOHI/O 2024)
- [Memento](https://github.com/Aryagarg23/Memento) — digital memory journal for Alzheimer's patients and caregivers (RevolutionUC 2024, 3rd overall)
- [Buycott](https://github.com/Aryagarg23/Buycott) — barcode scan → parent company → NLP stance on social issues (MakeUC 2023, 1st overall)
- [SignLink](https://github.com/Aryagarg23/SignLink) — video calls with real-time ASL fingerspelling to text (BoilerMake X 2023)
- [Kuka Arm Viz](https://github.com/Aryagarg23/Visualizing-Kuka-7-Node-Robot-Arm) — interactive 7-DOF robot arm in WebGL with inverse kinematics (RevolutionUC 2023)
- [Friction](https://github.com/Aryagarg23/Friction) — speculative OS + hardware that protects flow state with physical friction (Fig Build 2026)
