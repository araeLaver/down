#!/usr/bin/env python3
"""
Demo version of the continuous meeting generator - generates meetings every 2 minutes for testing
"""

import os
import time
from datetime import datetime, timedelta
from continuous_meeting_generator import ContinuousMeetingGenerator

class DemoMeetingGenerator(ContinuousMeetingGenerator):
    def __init__(self):
        super().__init__()
        self.meetings_dir = "demo_meetings"

        # Create demo meetings directory
        if not os.path.exists(self.meetings_dir):
            os.makedirs(self.meetings_dir)
            print(f"Created demo directory: {self.meetings_dir}")

    def run_demo(self, num_meetings=3, interval_minutes=2):
        """Run a demo version with shorter intervals"""
        print("Demo Business Meeting Generator Started")
        print(f"Demo files saved to: {os.path.abspath(self.meetings_dir)}")
        print(f"Generating {num_meetings} meetings every {interval_minutes} minutes...")
        print("Press Ctrl+C to stop early")
        print("\n")

        try:
            for i in range(num_meetings):
                print(f"\n--- Generating Demo Meeting {i+1}/{num_meetings} ---")

                # Generate and save meeting
                filepath = self.generate_and_save_meeting()

                if filepath:
                    if i < num_meetings - 1:  # Don't wait after the last meeting
                        next_meeting_time = datetime.now() + timedelta(minutes=interval_minutes)
                        print(f"\nNext demo meeting scheduled: {next_meeting_time.strftime('%H:%M:%S')}")
                        print(f"Waiting {interval_minutes} minutes...")
                        time.sleep(interval_minutes * 60)  # Convert to seconds
                else:
                    print("Meeting generation failed, skipping...")

            print(f"\n\nDemo completed!")
            print(f"Generated {self.meeting_count} meetings")
            print(f"Files saved to: {os.path.abspath(self.meetings_dir)}")

        except KeyboardInterrupt:
            print(f"\n\nDemo stopped early.")
            print(f"Generated {self.meeting_count} meetings so far")
            print(f"Files saved to: {os.path.abspath(self.meetings_dir)}")

def main():
    """Run the demo"""
    demo = DemoMeetingGenerator()
    demo.run_demo(num_meetings=3, interval_minutes=1)  # 1 minute for quick demo

if __name__ == "__main__":
    main()