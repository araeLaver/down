#!/usr/bin/env python3
"""
Continuous Business Meeting Generator
Automatically generates business meeting agendas every 30 minutes using the realistic_business_generator module.
Each meeting is saved to a timestamped file and includes 35-40 business opportunities.
"""

import os
import sys
import time
import json
from datetime import datetime, timedelta
from realistic_business_generator import RealisticBusinessGenerator

# Set encoding for Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

class ContinuousMeetingGenerator:
    def __init__(self):
        self.generator = RealisticBusinessGenerator()
        self.meetings_dir = "generated_meetings"
        self.meeting_count = 0

        # Create meetings directory if it doesn't exist
        if not os.path.exists(self.meetings_dir):
            os.makedirs(self.meetings_dir)
            print(f"Created directory: {self.meetings_dir}")

    def format_meeting_content(self, meeting_data):
        """Format the meeting data into a readable text format"""
        content = []
        content.append("=" * 80)
        content.append(f"BUSINESS MEETING: {meeting_data['meeting_type']}")
        content.append(f"GENERATED TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("=" * 80)
        content.append("")

        # Meeting Agenda
        content.append("MEETING AGENDA:")
        content.append("-" * 40)
        for i, agenda_item in enumerate(meeting_data['agenda'], 1):
            content.append(f"{i}. {agenda_item}")
        content.append("")

        # Key Decisions
        content.append("KEY DECISIONS:")
        content.append("-" * 40)
        for i, decision in enumerate(meeting_data['key_decisions'], 1):
            content.append(f"{i}. {decision}")
        content.append("")

        # Action Items
        content.append("ACTION ITEMS:")
        content.append("-" * 40)
        for i, action in enumerate(meeting_data['action_items'], 1):
            content.append(f"{i}. {action}")
        content.append("")

        # Top Priority Business
        content.append("TOP PRIORITY BUSINESS:")
        content.append("-" * 40)
        top_biz = meeting_data['top_priority_business']
        content.append(f"Business Name: {top_biz['business']['name']}")
        content.append(f"Type: {top_biz['type']}")
        content.append(f"Category: {top_biz.get('category', 'N/A')}")
        if 'description' in top_biz['business']:
            content.append(f"Description: {top_biz['business']['description']}")
        content.append(f"Initial Investment: {top_biz['business'].get('startup_cost', 'N/A')}")
        revenue = top_biz['business'].get('monthly_revenue', top_biz['business'].get('revenue_potential', 'N/A'))
        content.append(f"Expected Revenue: {revenue}")
        content.append(f"Priority: {top_biz['priority']}")
        content.append("")

        # All Business Opportunities (35-40 ideas)
        content.append(f"ALL BUSINESS OPPORTUNITIES ({len(meeting_data['opportunities'])} ideas):")
        content.append("=" * 60)

        for i, opp in enumerate(meeting_data['opportunities'], 1):
            content.append(f"\n{i}. {opp['business']['name']}")
            content.append(f"   Type: {opp['type']}")
            content.append(f"   Category: {opp.get('category', 'N/A')}")
            if 'description' in opp['business']:
                content.append(f"   Description: {opp['business']['description']}")
            content.append(f"   Initial Investment: {opp['business'].get('startup_cost', 'N/A')}")
            revenue = opp['business'].get('monthly_revenue', opp['business'].get('revenue_potential', 'N/A'))
            content.append(f"   Expected Revenue: {revenue}")
            content.append(f"   Difficulty: {opp['business'].get('difficulty', 'N/A')}")
            content.append(f"   Priority: {opp['priority']}")

        content.append("\n" + "=" * 60)

        # High Viability Themes
        if meeting_data.get('high_viability_themes'):
            content.append(f"\nHIGH-REVENUE THEMES ({len(meeting_data['high_viability_themes'])} items):")
            content.append("-" * 40)
            for i, theme in enumerate(meeting_data['high_viability_themes'], 1):
                content.append(f"\n{i}. {theme['idea']['name']}")
                content.append(f"   Theme Type: {theme['theme_type']}")
                content.append(f"   Category: {theme['category']}")
                content.append(f"   Market Size: {theme['market_size']}")
                content.append(f"   ROI Score: {theme['roi_score']}")
                content.append(f"   Implementation Complexity: {theme['implementation_complexity']}")
                if 'description' in theme['idea']:
                    content.append(f"   Description: {theme['idea']['description']}")

        # Validated Business Models
        content.append(f"\nVALIDATED BUSINESS MODELS:")
        content.append("-" * 40)
        for i, model in enumerate(meeting_data['validated_models'], 1):
            content.append(f"\n{i}. {model['model']}")
            content.append(f"   Success Rate: {model['success_rate']}")
            content.append(f"   Pros: {model['pros']}")
            content.append(f"   Cons: {model['cons']}")
            content.append(f"   Examples: {', '.join(model['examples'])}")

        content.append("\n" + "=" * 80)
        content.append("MEETING END")
        content.append("=" * 80)

        return "\n".join(content)

    def generate_and_save_meeting(self):
        """Generate a business meeting and save it to a file"""
        try:
            # Generate meeting data
            meeting_data = self.generator.generate_business_meeting_agenda()

            # Create timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"business_meeting_{timestamp}.txt"
            filepath = os.path.join(self.meetings_dir, filename)

            # Format and save meeting content
            meeting_content = self.format_meeting_content(meeting_data)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(meeting_content)

            self.meeting_count += 1

            # Display summary on screen
            self.display_meeting_summary(meeting_data, filepath)

            return filepath

        except Exception as e:
            error_msg = f"Error generating meeting: {str(e)}"
            print(f"ERROR: {error_msg}")
            return None

    def display_meeting_summary(self, meeting_data, filepath):
        """Display a summary of the generated meeting on screen"""
        print("\n" + "=" * 80)
        print(f"New Business Meeting Generated (#{self.meeting_count})")
        print(f"File: {filepath}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        print(f"\nMeeting Type: {meeting_data['meeting_type']}")
        print(f"Total Business Opportunities: {len(meeting_data['opportunities'])}")
        print(f"High-Revenue Themes: {len(meeting_data.get('high_viability_themes', []))}")

        # Top business opportunity
        top_biz = meeting_data['top_priority_business']
        print(f"\nTop Priority Business: {top_biz['business']['name']}")
        print(f"   Type: {top_biz['type']}")
        print(f"   Initial Investment: {top_biz['business'].get('startup_cost', 'N/A')}")
        revenue = top_biz['business'].get('monthly_revenue', top_biz['business'].get('revenue_potential', 'N/A'))
        print(f"   Expected Revenue: {revenue}")
        print(f"   Priority Level: {top_biz['priority']}")

        # Business opportunities breakdown
        priority_counts = {}
        type_counts = {}

        for opp in meeting_data['opportunities']:
            priority = opp['priority']
            biz_type = opp['type']
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
            type_counts[biz_type] = type_counts.get(biz_type, 0) + 1

        print(f"\nPriority Distribution:")
        for priority, count in sorted(priority_counts.items(), key=lambda x: {'매우 높음': 3, '높음': 2, '보통': 1}.get(x[0], 0), reverse=True):
            print(f"   {priority}: {count}")

        print(f"\nBusiness Type Distribution:")
        for biz_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {biz_type}: {count}")

        print(f"\nNext meeting in: 30 minutes")
        print("=" * 80)

    def run_continuous(self):
        """Run the continuous meeting generator"""
        print("Continuous Business Meeting Generator Started")
        print(f"Meeting files saved to: {os.path.abspath(self.meetings_dir)}")
        print("Generating new meetings every 30 minutes...")
        print("Press Ctrl+C to stop")
        print("\n")

        try:
            while True:
                # Generate and save meeting
                filepath = self.generate_and_save_meeting()

                if filepath:
                    next_meeting_time = datetime.now() + timedelta(minutes=30)
                    print(f"\nNext meeting scheduled: {next_meeting_time.strftime('%H:%M:%S')}")
                    print("Waiting 30 minutes...")
                else:
                    print("Meeting generation failed, retrying in 5 minutes...")
                    time.sleep(300)  # Wait 5 minutes on error
                    continue

                # Wait for 30 minutes (1800 seconds)
                time.sleep(1800)

        except KeyboardInterrupt:
            print(f"\n\nContinuous generator stopped.")
            print(f"Total meetings generated: {self.meeting_count}")
            print(f"Files saved to: {os.path.abspath(self.meetings_dir)}")
            print("Program terminated.")

def main():
    """Main function to run the continuous meeting generator"""
    generator = ContinuousMeetingGenerator()
    generator.run_continuous()

if __name__ == "__main__":
    main()