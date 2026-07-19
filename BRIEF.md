# BRIEF — Hi-Five (repo: Aryagarg23/Hi-Five)
Slug: hi-five. Hackathon: SASEhack Fall 2024 (University of Cincinnati), October 2024. Prizes: none listed.
Team: Raihan Rafeek, Shawn Lasrado, Shashwat Mishra, Arya Garg. IMPORTANT honesty note: Arya's code never got committed from his machine that weekend — the git history shows only the other three. Credit him as a team member but do not invent commits; the Devpost team list also shows the other three. Original repo: https://github.com/Rai1975/SASEHackProject
What: anonymous social platform matching people on personality compatibility, not photos. Users take an OCEAN assessment (Openness, Conscientiousness, Extroversion, Agreeableness, Neuroticism) + pick interest tags; vector embeddings find compatible users; matches get a 48-hour anonymous chat window; if both opt in, identities reveal and the friendship goes permanent.
Tech: Next.js + MUI frontend (login, user cards, swipe, chat, friends), Neo4j for users/relationships, BGE-en-icl + RoBERTa-base-go-emotions for embeddings and similarity.
Devpost: https://devpost.com/software/hi-five-dt0gvj
Prototype idea: synthetic OCEAN vectors for ~12 fake users, cosine compatibility, chart 1: compatibility heatmap (users x users, sequential blue), chart 2: distribution of match scores with the accept threshold marked (reference line dashed #e85b30).
