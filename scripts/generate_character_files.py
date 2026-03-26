from __future__ import annotations

import re
from pathlib import Path


SOURCE_URL = "https://beebom.com/frieren-characters-name-age-class/"
SOURCE_NOTE = "Metadata/paraphrased summaries derived from the Beebom article at runtime-free extraction."


def slug(name: str) -> str:
    s = name.strip().lower().replace(" ", "_")
    s = re.sub(r"[^a-z0-9_]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "character"


def write_character_file(char_dir: Path, character: dict) -> None:
    name = character["name"]
    role = character.get("role") or ""

    debut_anime_episode = character["debut_anime_episode"]
    debut_manga_chapter = character["debut_manga_chapter"]

    role_line = f", role: {role}" if role else ""

    md = f"""---
name: "{name}"
age: "{character['age']}"
race: "{character['race']}"
class: "{character['class_name']}"
role: "{role}"
rank: "{character['rank']}"
debut_anime_episode: "{debut_anime_episode}"
debut_manga_chapter: "{debut_manga_chapter}"
source_url: "{SOURCE_URL}"
source_note: "{SOURCE_NOTE}"
---

## Overview
{character['overview']}

## Key facts
- Age: {character['age']}
- Race: {character['race']}
- Class: {character['class_name']}{role_line}
- Rank: {character['rank']}
- Debut: Anime Episode {debut_anime_episode}, Manga Chapter {debut_manga_chapter}
"""

    out_path = char_dir / f"{slug(name)}.md"
    out_path.write_text(md, encoding="utf-8")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    char_dir = repo_root / "data" / "characters"
    char_dir.mkdir(parents=True, exist_ok=True)

    characters = [
        {
            "name": "Frieren",
            "age": "1000+",
            "race": "Elf",
            "class_name": "Mage",
            "role": "",
            "rank": "Great Mage",
            "debut_anime_episode": "1",
            "debut_manga_chapter": "1",
            "overview": (
                "Frieren is the series protagonist and an elf mage with a very long lifespan, "
                "which shapes how she perceives emotions and time. She previously served as the mage "
                "for the Hero Party that defeated the Demon King. After her party's hero, Himmel, dies, "
                "she forms a new journey toward Aureole, where she hopes to revisit unresolved feelings."
            ),
        },
        {
            "name": "Fern",
            "age": "19-20",
            "race": "Human",
            "class_name": "Mage",
            "role": "",
            "rank": "First Class",
            "debut_anime_episode": "1",
            "debut_manga_chapter": "2",
            "overview": (
                "Fern is a human mage who becomes Frieren's important party member through her training "
                "and growth. Raised by Heiter after losing her parents in a war, she is later taken "
                "under Frieren's guidance. She climbs from earlier rank to First-Class mage after passing "
                "the mage exam, determined to continue becoming more capable."
            ),
        },
        {
            "name": "Stark",
            "age": "20",
            "race": "Human",
            "class_name": "Warrior",
            "role": "Vanguard",
            "rank": "Unknown",
            "debut_anime_episode": "1",
            "debut_manga_chapter": "1",
            "overview": (
                "Stark is a human warrior and the party's Vanguard role. He is trained by Eisen and carries "
                "the consequences of a painful past involving conflict around his home village. When he later meets "
                "Frieren and Fern during his duties, he becomes a core part of their group. His journey is driven "
                "by determination to overcome fear and earn the trust of his allies."
            ),
        },
        {
            "name": "Himmel",
            "age": "26 (flashbacks), 76 (post timeskip)",
            "race": "Human",
            "class_name": "Hero",
            "role": "",
            "rank": "Unknown",
            "debut_anime_episode": "1",
            "debut_manga_chapter": "1",
            "overview": (
                "Himmel the Hero is remembered as the figure who vanquished the Demon King with his party. "
                "The story opens with his death in old age, while flashbacks gradually reveal his adventures "
                "and his kindness. His legacy leaves a strong emotional imprint on Frieren and helps explain why "
                "she continues her journey after he is gone."
            ),
        },
        {
            "name": "Heiter",
            "age": "100",
            "race": "Human",
            "class_name": "Priest",
            "role": "",
            "rank": "Bishop",
            "debut_anime_episode": "1",
            "debut_manga_chapter": "1",
            "overview": (
                "Heiter is a priest whose holy magic and cheerful personality brought warmth to the Hero Party. "
                "After the party's adventures ended, he took on the role of Bishop. He also plays a major part "
                "in Fern's life, adopting her and raising her with care. Before his death, he asks Frieren to look "
                "after Fern as an apprentice."
            ),
        },
        {
            "name": "Eisen",
            "age": "100+ years old",
            "race": "Dwarf",
            "class_name": "Warrior",
            "role": "Vanguard",
            "rank": "Unknown",
            "debut_anime_episode": "1",
            "debut_manga_chapter": "1",
            "overview": (
                "Eisen is a dwarf warrior serving as Vanguard for the Hero Party, leading from the front during "
                "their long campaign. After the Demon King is defeated, he retires from that life. His path crosses "
                "Stark early on, leading to a teacher-student relationship that later fractures due to conflict. "
                "Even so, he remains a significant figure connected to Stark's development."
            ),
        },
        {
            "name": "Sein",
            "age": "Unknown",
            "race": "Human",
            "class_name": "Priest",
            "role": "",
            "rank": "Unknown",
            "debut_anime_episode": "13",
            "debut_manga_chapter": "27",
            "overview": (
                "Sein is a human priest whose age is not clearly stated, though he is one of the older members "
                "in the group. He dreams of adventures with his friend Gorilla, but he stays back to care for "
                "family obligations. Eventually, he teams up with Frieren's party to reunite with Gorilla after "
                "years of separation. The search becomes both an emotional mission and a chance for him to move on."
            ),
        },
        {
            "name": "Flamme",
            "age": "Unknown",
            "race": "Human",
            "class_name": "Mage",
            "role": "",
            "rank": "Great Mage",
            "debut_anime_episode": "4",
            "debut_manga_chapter": "7",
            "overview": (
                "Flamme is the Great Mage associated with the development of human magic. She is portrayed as a "
                "founder figure whose teachings shaped Frieren's growth. Flamme wanted magic to become something "
                "anyone could wield, but she passed away before that vision could fully spread. In the present, her "
                "will continues through her student."
            ),
        },
        {
            "name": "Serie",
            "age": "1500+",
            "race": "Elf",
            "class_name": "Mage",
            "role": "",
            "rank": "Great Mage and Head of the Continental Magic Association",
            "debut_anime_episode": "18",
            "debut_manga_chapter": "43",
            "overview": (
                "Serie is an ancient elf mage with over fifteen hundred years of experience. She leads the Continental "
                "Magic Association and acts as a prominent authority during mage examinations. She is also connected to Flamme, "
                "having taken her in and teaching her. Her breadth of knowledge and influence make her a key benchmark "
                "for other mages."
            ),
        },
        {
            "name": "Ubel",
            "age": "Unknown",
            "race": "Human",
            "class_name": "Mage",
            "role": "",
            "rank": "First Class",
            "debut_anime_episode": "18",
            "debut_manga_chapter": "37",
            "overview": (
                "Ubel is a human mage who stands out during the mage exam arc and becomes a First-Class mage. "
                "Her power is framed as dangerous and capable of cutting through opponents effectively. Although she initially "
                "faces major setbacks due to prior circumstances, the exam sequence leads to her advancement. Beneath the intimidating "
                "first impression, she is described as someone with empathy and a surprising emotional depth."
            ),
        },
        {
            "name": "Land",
            "age": "Unknown",
            "race": "Human",
            "class_name": "Mage",
            "role": "",
            "rank": "First Class",
            "debut_anime_episode": "19",
            "debut_manga_chapter": "39",
            "overview": (
                "Land is a human mage participant who becomes notable for how cleverly he navigates the mage exam. "
                "While he appears to be around the same age bracket as other competitors, his strategy involves using a clone "
                "to participate in the exam. This reveals both his resourcefulness and his willingness to take calculated risks. "
                "At the end of the arc, he achieves First-Class status."
            ),
        },
        {
            "name": "Wirbel",
            "age": "33-34",
            "race": "Human",
            "class_name": "Mage",
            "role": "",
            "rank": "First Class",
            "debut_anime_episode": "19",
            "debut_manga_chapter": "39",
            "overview": (
                "Wirbel is an experienced human mage who leads operations for the Northern Magic Corps in the far north. "
                "His reputation comes from battlefield leadership rather than youth-based assumptions. During the exam, he graduates "
                "to First-Class after passing with Serie's approval. Even though he can look younger than expected, his age and "
                "experience place him firmly in an older category."
            ),
        },
        {
            "name": "Denken",
            "age": "78-79",
            "race": "Human",
            "class_name": "Mage",
            "role": "",
            "rank": "First Class",
            "debut_anime_episode": "18",
            "debut_manga_chapter": "37",
            "overview": (
                "Denken is portrayed as one of the oldest First-Class mage exam participants, with age in the late seventies. "
                "His wisdom and deep magical knowledge influence how he approaches the exam and decisions afterward. He also carries a "
                "tragic backstory involving an attempt to save his wife, which adds gravity to his character. After receiving Serie's "
                "approval, he becomes a First-Class mage and is positioned as a recurring supporting figure."
            ),
        },
        {
            "name": "Methode",
            "age": "Unknown",
            "race": "Human",
            "class_name": "Mage",
            "role": "",
            "rank": "First Class",
            "debut_anime_episode": "22",
            "debut_manga_chapter": "46",
            "overview": (
                "Methode is a human mage who reaches First-Class status after demonstrating her value during the mage exam. "
                "Her strengths include hypnotic magic that plays an important role in the second stage. She survives the exam process "
                "despite being a second-class at the start, placing her among the rare successful candidates. After the arc, "
                "she reunites with Frieren's party during the extermination period in the Northern Plateau."
            ),
        },
        {
            "name": "Lawine",
            "age": "Unknown",
            "race": "Human",
            "class_name": "Mage",
            "role": "",
            "rank": "Third Class",
            "debut_anime_episode": "18",
            "debut_manga_chapter": "38",
            "overview": (
                "Lawine comes from an elite background and is driven by pressure to live up to expectations as a powerful mage. "
                "Specializing in ice magic, she attempts the mage exam aiming for First-Class advancement. Her exam attempt ends when "
                "she exits using a golem during the second stage. She plans to wait for the next cycle to try again in the future."
            ),
        },
        {
            "name": "Kanne",
            "age": "Unknown",
            "race": "Human",
            "class_name": "Mage",
            "role": "",
            "rank": "First Class",
            "debut_anime_episode": "18",
            "debut_manga_chapter": "38",
            "overview": (
                "Kanne is Lawine's close friend and a human mage who shares a similar academy background. "
                "She focuses on abilities such as flight and water manipulation magic. Despite her determination, fear influences "
                "her performance during key moments of the exam. Serie is said to recognize this fear quickly, which affects the outcome. "
                "Even so, the arc frames Kanne as someone who will improve and try again."
            ),
        },
        {
            "name": "Hero of the South",
            "age": "Unknown",
            "race": "Human",
            "class_name": "Hero",
            "role": "",
            "rank": "Humanity's Strongest Hero",
            "debut_anime_episode": "TBD",
            "debut_manga_chapter": "63",
            "overview": (
                "The Hero of the South is a legendary hero from before Himmel, remembered as humanity's strongest hero. "
                "He fought against the Seven Sages of Destruction sent by the Demon King and managed to defeat multiple targets. "
                "Although referenced earlier in the story, he is expected to be fully encountered through flashbacks in a later season. "
                "His reputation provides historical context for the world that Frieren eventually explores."
            ),
        },
    ]

    for c in characters:
        write_character_file(char_dir, c)

    print(f"Generated {len(characters)} character files in: {char_dir}")


if __name__ == "__main__":
    main()

