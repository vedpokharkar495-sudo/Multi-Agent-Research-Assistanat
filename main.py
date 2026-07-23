# main.py
# Command-line version of the research assistant

import sys
import json
from graph import research_assistant


def main():
    """Command-line interface for the research assistant"""

    print("Multi-Agent Research Assistant")
    print("=" * 40)

    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter research topic: ").strip()

    if not topic:
        print("Please enter a research topic")
        return

    print(f"\nResearching: {topic}")
    print("-" * 40)

    try:
        # Run research
        result = research_assistant.research(topic)

        # Print results
        print("\nResearch Plan:")
        for i, section in enumerate(result["plan"], 1):
            print(f"  {i}. {section}")

        print(f"\nIterations: {result['iterations']}")
        print(f"Verified: {result['is_verified']}")

        print("\nResearch Report:")
        print("-" * 40)
        print(result["report"])
        print("-" * 40)

        # Save to file
        filename = f"{topic.replace(' ', '_')}_report.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Research Report: {topic}\n")
            f.write("=" * 50 + "\n\n")
            f.write(result["report"])

        print(f"\nReport saved to: {filename}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()