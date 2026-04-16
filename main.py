import ollama
import json
import os
from datetime import datetime

CAMPAIGNS_DIR = "campaigns"
os.makedirs(CAMPAIGNS_DIR, exist_ok=True)

def save_campaign(campaign: dict):
    path = os.path.join(CAMPAIGNS_DIR, f"{campaign['id']}.json")
    with open(path, "w") as f:
        json.dump(campaign, f, indent=2)
    print(f"\n Campaign saved to {path}")


def load_campaign(campaign_id: str) -> dict | None:
    path = os.path.join(CAMPAIGNS_DIR, f"{campaign_id}.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def list_campaigns() -> list[dict]:
    campaigns = []
    for fname in os.listdir(CAMPAIGNS_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(CAMPAIGNS_DIR, fname)) as f:
                data = json.load(f)
                campaigns.append({"id": data["id"], "name": data["name"], "created": data["created"]})
    return campaigns

def ask_ollama(messages: list[dict]) -> str:
    response = ollama.chat(model="llama3.2", messages=messages)
    return response["message"]["content"]

def generate_campaign(theme: str) -> dict:
    print("\n  Generating your campaign... (this may take a minute)\n")

    prompt = f"""You are an expert Dungeons & Dragons Dungeon Master. Generate a full D&D campaign based on this theme: "{theme}".

Return ONLY valid JSON with this exact structure:
{{
  "name": "Campaign name",
  "setting": "2-3 sentence world description",
  "backstory": "2-3 sentence overarching plot",
  "factions": [
    {{"name": "Faction name", "description": "1-2 sentences", "goal": "What they want"}}
  ],
  "npcs": [
    {{"name": "NPC name", "role": "e.g. Quest Giver", "personality": "1 sentence", "secret": "Hidden detail"}}
  ],
  "quests": [
    {{"title": "Quest name", "description": "2-3 sentences", "reward": "What players get", "twist": "Unexpected complication"}}
  ],
  "locations": [
    {{"name": "Location name", "description": "1-2 sentences", "danger_level": "Low/Medium/High"}}
  ],
  "opening_scene": "A vivid 3-4 sentence description of how the campaign begins"
}}

Include 3 factions, 4 NPCs, 3 quests, and 4 locations. Return only the JSON, no other text."""

    raw = ask_ollama([{"role": "user", "content": prompt}])

    # Strip markdown code fences if present
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        campaign_data = json.loads(raw)
    except json.JSONDecodeError:
        print("  Couldn't parse JSON cleanly, saving raw response.")
        campaign_data = {"name": theme, "raw": raw}

    campaign_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    campaign = {
        "id": campaign_id,
        "created": datetime.now().isoformat(),
        "theme": theme,
        "chat_history": [],
        **campaign_data,
    }
    return campaign

def dm_chat(campaign: dict):
    print(f"\n You are now chatting with your DM for campaign: {campaign['name']}")
    print("Type 'quit' to exit, 'save' to save, 'summary' to recap the campaign.\n")

    system_prompt = f"""You are an expert Dungeon Master running this D&D campaign:

Name: {campaign.get('name')}
Setting: {campaign.get('setting')}
Backstory: {campaign.get('backstory')}
Opening Scene: {campaign.get('opening_scene')}

NPCs: {json.dumps(campaign.get('npcs', []), indent=2)}
Quests: {json.dumps(campaign.get('quests', []), indent=2)}
Locations: {json.dumps(campaign.get('locations', []), indent=2)}
Factions: {json.dumps(campaign.get('factions', []), indent=2)}

Stay in character as a DM. Be descriptive, dramatic, and helpful. Answer questions about the world, NPCs, and quests. Help the player navigate the campaign."""

    messages = [{"role": "system", "content": system_prompt}]

    # Restore previous chat history
    for entry in campaign.get("chat_history", []):
        messages.append(entry)

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("Farewell, adventurer!")
            break
        elif user_input.lower() == "save":
            save_campaign(campaign)
            continue
        elif user_input.lower() == "summary":
            print(f"\n Campaign: {campaign.get('name')}")
            print(f"Setting: {campaign.get('setting')}")
            print(f"Backstory: {campaign.get('backstory')}\n")
            continue

        messages.append({"role": "user", "content": user_input})
        print("\nDM: ", end="", flush=True)
        reply = ask_ollama(messages)
        print(reply + "\n")

        messages.append({"role": "assistant", "content": reply})

        # Save to campaign chat history (excluding system prompt)
        campaign["chat_history"] = [m for m in messages if m["role"] != "system"]

    save_campaign(campaign)

def main():
    print("╔════════════════════════╗")
    print("║       Pocket DM        ║")
    print("╚════════════════════════╝\n")

    while True:
        print("1. Generate new campaign")
        print("2. Load existing campaign")
        print("3. List campaigns")
        print("4. Quit")
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            theme = input("Enter a campaign theme (e.g. 'dark fantasy', 'pirate adventure'): ").strip()
            campaign = generate_campaign(theme)
            print(f"\n Campaign Generated: {campaign.get('name')}")
            print(f"Setting: {campaign.get('setting')}")
            print(f"\nOpening Scene:\n{campaign.get('opening_scene')}\n")
            save_campaign(campaign)
            start = input("Start chatting with your DM now? (y/n): ").strip().lower()
            if start == "y":
                dm_chat(campaign)

        elif choice == "2":
            campaigns = list_campaigns()
            if not campaigns:
                print("No campaigns found.\n")
                continue
            print("\nYour campaigns:")
            for c in campaigns:
                print(f"  [{c['id']}] {c['name']} — created {c['created'][:10]}")
            cid = input("\nEnter campaign ID to load: ").strip()
            campaign = load_campaign(cid)
            if campaign:
                print(f"\n Loaded: {campaign['name']}")
                dm_chat(campaign)
            else:
                print("Campaign not found.\n")

        elif choice == "3":
            campaigns = list_campaigns()
            if not campaigns:
                print("No campaigns found.\n")
            else:
                print("\nYour campaigns:")
                for c in campaigns:
                    print(f"  [{c['id']}] {c['name']} — created {c['created'][:10]}")
                print()

        elif choice == "4":
            print("Goodbye \n--Jerry the Dungeon Master")
            break
        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()
