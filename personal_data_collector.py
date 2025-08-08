#!/usr/bin/env python3
"""
Personal Data Collector for Hanzala's Digital Replica
Helps collect and organize personal information for the digital replica
"""
import json
import os
import datetime
from typing import Dict, List, Any

class PersonalDataCollector:
    """Tool to collect and organize personal data for digital replica."""
    
    def __init__(self):
        self.data_dir = "hanzala_personal_data"
        self.categories = {
            "personal_stories": "Personal stories and memories",
            "family_memories": "Family relationships and memories",
            "life_events": "Significant life events",
            "values_beliefs": "Personal values and beliefs",
            "communication_style": "How you communicate",
            "emotional_patterns": "How you handle emotions",
            "decision_making": "How you make decisions",
            "humor_expressions": "Your humor and expressions",
            "professional_experiences": "Work and career experiences",
            "mentorship_advice": "Advice you give to others",
            "life_philosophy": "Your life philosophy",
            "future_hopes": "Your dreams and aspirations",
            "relationships": "How you connect with others",
            "challenges_overcome": "Difficult times and how you handled them",
            "achievements": "Your proudest moments",
            "legacy_messages": "Messages for future generations"
        }
        
        self.setup_data_structure()
    
    def setup_data_structure(self):
        """Create the data collection directory structure."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        for category in self.categories.keys():
            category_dir = os.path.join(self.data_dir, category)
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)
        
        # Create metadata file
        metadata = {
            "created_date": datetime.datetime.now().isoformat(),
            "categories": self.categories,
            "total_entries": 0,
            "last_updated": datetime.datetime.now().isoformat()
        }
        
        with open(os.path.join(self.data_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)
    
    def add_personal_story(self, title: str, story: str, tags: List[str] = None, date: str = None):
        """Add a personal story or memory."""
        entry = {
            "title": title,
            "story": story,
            "tags": tags or [],
            "date": date or datetime.datetime.now().isoformat(),
            "category": "personal_stories"
        }
        
        filename = f"{title.lower().replace(' ', '_')}.json"
        filepath = os.path.join(self.data_dir, "personal_stories", filename)
        
        with open(filepath, "w") as f:
            json.dump(entry, f, indent=2)
        
        print(f"✅ Added personal story: {title}")
    
    def add_family_memory(self, family_member: str, memory: str, relationship: str = None, date: str = None):
        """Add a family memory."""
        entry = {
            "family_member": family_member,
            "memory": memory,
            "relationship": relationship,
            "date": date or datetime.datetime.now().isoformat(),
            "category": "family_memories"
        }
        
        filename = f"{family_member.lower().replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}.json"
        filepath = os.path.join(self.data_dir, "family_memories", filename)
        
        with open(filepath, "w") as f:
            json.dump(entry, f, indent=2)
        
        print(f"✅ Added family memory: {family_member}")
    
    def add_life_event(self, event_title: str, description: str, impact: str, date: str = None):
        """Add a significant life event."""
        entry = {
            "event_title": event_title,
            "description": description,
            "impact": impact,
            "date": date or datetime.datetime.now().isoformat(),
            "category": "life_events"
        }
        
        filename = f"{event_title.lower().replace(' ', '_')}.json"
        filepath = os.path.join(self.data_dir, "life_events", filename)
        
        with open(filepath, "w") as f:
            json.dump(entry, f, indent=2)
        
        print(f"✅ Added life event: {event_title}")
    
    def add_value_belief(self, value: str, description: str, examples: List[str] = None):
        """Add a personal value or belief."""
        entry = {
            "value": value,
            "description": description,
            "examples": examples or [],
            "category": "values_beliefs"
        }
        
        filename = f"{value.lower().replace(' ', '_')}.json"
        filepath = os.path.join(self.data_dir, "values_beliefs", filename)
        
        with open(filepath, "w") as f:
            json.dump(entry, f, indent=2)
        
        print(f"✅ Added value/belief: {value}")
    
    def add_communication_style(self, aspect: str, description: str, examples: List[str] = None):
        """Add information about communication style."""
        entry = {
            "aspect": aspect,
            "description": description,
            "examples": examples or [],
            "category": "communication_style"
        }
        
        filename = f"{aspect.lower().replace(' ', '_')}.json"
        filepath = os.path.join(self.data_dir, "communication_style", filename)
        
        with open(filepath, "w") as f:
            json.dump(entry, f, indent=2)
        
        print(f"✅ Added communication style: {aspect}")
    
    def add_professional_experience(self, role: str, company: str, experience: str, learnings: List[str] = None, date: str = None):
        """Add a professional experience."""
        entry = {
            "role": role,
            "company": company,
            "experience": experience,
            "learnings": learnings or [],
            "date": date or datetime.datetime.now().isoformat(),
            "category": "professional_experiences"
        }
        
        filename = f"{role.lower().replace(' ', '_')}_{company.lower().replace(' ', '_')}.json"
        filepath = os.path.join(self.data_dir, "professional_experiences", filename)
        
        with open(filepath, "w") as f:
            json.dump(entry, f, indent=2)
        
        print(f"✅ Added professional experience: {role} at {company}")
    
    def add_mentorship_advice(self, topic: str, advice: str, context: str = None, examples: List[str] = None):
        """Add advice you give to others."""
        entry = {
            "topic": topic,
            "advice": advice,
            "context": context,
            "examples": examples or [],
            "category": "mentorship_advice"
        }
        
        filename = f"{topic.lower().replace(' ', '_')}.json"
        filepath = os.path.join(self.data_dir, "mentorship_advice", filename)
        
        with open(filepath, "w") as f:
            json.dump(entry, f, indent=2)
        
        print(f"✅ Added mentorship advice: {topic}")
    
    def add_legacy_message(self, audience: str, message: str, context: str = None):
        """Add a message for future generations."""
        entry = {
            "audience": audience,
            "message": message,
            "context": context,
            "date": datetime.datetime.now().isoformat(),
            "category": "legacy_messages"
        }
        
        filename = f"{audience.lower().replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}.json"
        filepath = os.path.join(self.data_dir, "legacy_messages", filename)
        
        with open(filepath, "w") as f:
            json.dump(entry, f, indent=2)
        
        print(f"✅ Added legacy message for: {audience}")
    
    def interactive_data_collection(self):
        """Interactive data collection session."""
        print("🤖 Welcome to Hanzala's Personal Data Collector!")
        print("This tool will help you collect information for your digital replica.")
        print("Let's start collecting your personal data...\n")
        
        while True:
            print("\n📋 Available Categories:")
            for i, (category, description) in enumerate(self.categories.items(), 1):
                print(f"{i}. {description}")
            print("0. Exit")
            
            try:
                choice = int(input("\nSelect a category (0-16): "))
                if choice == 0:
                    break
                elif 1 <= choice <= len(self.categories):
                    category = list(self.categories.keys())[choice - 1]
                    self.collect_category_data(category)
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def collect_category_data(self, category: str):
        """Collect data for a specific category."""
        print(f"\n📝 Collecting data for: {self.categories[category]}")
        
        if category == "personal_stories":
            title = input("Story title: ")
            story = input("Tell your story: ")
            tags = input("Tags (comma-separated): ").split(",") if input("Add tags? (y/n): ").lower() == 'y' else []
            self.add_personal_story(title, story, tags)
        
        elif category == "family_memories":
            family_member = input("Family member name: ")
            memory = input("Share your memory: ")
            relationship = input("Your relationship: ")
            self.add_family_memory(family_member, memory, relationship)
        
        elif category == "life_events":
            event_title = input("Event title: ")
            description = input("Describe the event: ")
            impact = input("How did it impact you? ")
            self.add_life_event(event_title, description, impact)
        
        elif category == "values_beliefs":
            value = input("Value or belief: ")
            description = input("Describe this value: ")
            examples = input("Examples (comma-separated): ").split(",") if input("Add examples? (y/n): ").lower() == 'y' else []
            self.add_value_belief(value, description, examples)
        
        elif category == "communication_style":
            aspect = input("Communication aspect: ")
            description = input("Describe your style: ")
            examples = input("Examples (comma-separated): ").split(",") if input("Add examples? (y/n): ").lower() == 'y' else []
            self.add_communication_style(aspect, description, examples)
        
        elif category == "professional_experiences":
            role = input("Job role: ")
            company = input("Company: ")
            experience = input("Describe your experience: ")
            learnings = input("What did you learn? (comma-separated): ").split(",") if input("Add learnings? (y/n): ").lower() == 'y' else []
            self.add_professional_experience(role, company, experience, learnings)
        
        elif category == "mentorship_advice":
            topic = input("Advice topic: ")
            advice = input("Your advice: ")
            context = input("Context (optional): ")
            examples = input("Examples (comma-separated): ").split(",") if input("Add examples? (y/n): ").lower() == 'y' else []
            self.add_mentorship_advice(topic, advice, context, examples)
        
        elif category == "legacy_messages":
            audience = input("For whom? (e.g., 'my children', 'future generations'): ")
            message = input("Your message: ")
            context = input("Context (optional): ")
            self.add_legacy_message(audience, message, context)
        
        else:
            print(f"📝 Please manually add data to the {category} folder.")
    
    def generate_summary(self):
        """Generate a summary of collected data."""
        summary = {
            "total_entries": 0,
            "categories": {},
            "last_updated": datetime.datetime.now().isoformat()
        }
        
        for category in self.categories.keys():
            category_dir = os.path.join(self.data_dir, category)
            if os.path.exists(category_dir):
                files = [f for f in os.listdir(category_dir) if f.endswith('.json')]
                summary["categories"][category] = len(files)
                summary["total_entries"] += len(files)
        
        summary_file = os.path.join(self.data_dir, "summary.json")
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📊 Data Collection Summary:")
        print(f"Total entries: {summary['total_entries']}")
        for category, count in summary["categories"].items():
            print(f"- {self.categories[category]}: {count} entries")
        
        return summary

def main():
    """Main function to run the data collector."""
    collector = PersonalDataCollector()
    
    print("🤖 Hanzala's Personal Data Collector")
    print("=" * 50)
    print("This tool will help you collect personal data for your digital replica.")
    print("Your data will be organized and ready for AI training.")
    print("=" * 50)
    
    # Run interactive collection
    collector.interactive_data_collection()
    
    # Generate summary
    collector.generate_summary()
    
    print(f"\n✅ Data collection complete!")
    print(f"📁 Your data is saved in: {collector.data_dir}")
    print(f"📋 Next steps:")
    print(f"   1. Review and add more data")
    print(f"   2. Process the data for AI training")
    print(f"   3. Integrate with your digital replica system")

if __name__ == "__main__":
    main()
