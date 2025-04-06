# Article Writing Workflow

A PocketFlow example that demonstrates an article writing workflow using a sequence of LLM calls.

## Features

- Generate a simple outline with up to 3 main sections using YAML structured output
- Write concise (100 words max) content for each section in simple terms
- Apply a conversational, engaging style to the final article

## Getting Started

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your_api_key_here
```

3. Run the application with a default topic ("AI Safety"):

```bash
python main.py
```

4. Or specify your own topic:

```bash
python main.py Climate Change
```

## How It Works

The workflow consists of three sequential nodes:

```mermaid
graph LR
    Outline[Generate Outline] --> Write[Write Content]
    Write --> Style[Apply Style]
```

Here's what each node does:

1. **Generate Outline**: Creates a simple outline with up to 3 main sections using YAML structured output
2. **Write Simple Content**: Writes a concise 100-word explanation for each section
3. **Apply Style**: Rewrites the combined content in a conversational, engaging style

## Files

- [`main.py`](./main.py): Main entry point for running the article workflow
- [`flow.py`](./flow.py): Defines the flow that connects the nodes
- [`nodes.py`](./nodes.py): Contains the node classes for each step in the workflow
- [`utils.py`](./utils.py): Utility functions including the LLM wrapper
- [`requirements.txt`](./requirements.txt): Lists the required dependencies

## Example Output

```
=== Starting Article Workflow on Topic: AI Safety ===


===== OUTLINE (YAML) =====

sections:
- Introduction to AI Safety
- Key Challenges in AI Safety
- Strategies for Ensuring AI Safety


===== PARSED OUTLINE =====

1. Introduction to AI Safety
2. Key Challenges in AI Safety
3. Strategies for Ensuring AI Safety

=========================


===== SECTION CONTENTS =====

--- Introduction to AI Safety ---
AI Safety is about making sure that artificial intelligence (AI) systems are helpful and not harmful. Imagine teaching a robot to help with chores. AI Safety is like setting ground rules for the robot so it doesn't accidentally cause trouble, like mistaking a pet for a toy. By ensuring AI systems understand their tasks and limitations, we can trust them to act safely. It's about creating guidelines and checks to ensure AI assists us without unintended consequences.

--- Key Challenges in AI Safety ---
AI safety is about ensuring that artificial intelligence systems operate in ways that are beneficial and not harmful. One key challenge is making sure AI makes decisions that align with human values. Imagine teaching a robot to fetch coffee, but it ends up knocking things over because it doesn't understand the mess it creates. Similarly, if AI systems don't fully grasp human intentions, they might act in unexpected ways. The task is to make AI smart enough to achieve goals without causing problems, much like training a puppy to follow rules without chewing on your shoes.

--- Strategies for Ensuring AI Safety ---
Ensuring AI safety is about making sure artificial intelligence behaves as expected and doesn’t cause harm. Imagine AI as a new driver on the road; we need rules and safeguards to prevent accidents. By testing AI systems under different conditions, setting clear rules for their behavior, and keeping human oversight, we can manage risks. For instance, just as cars have brakes to ensure safety, AI systems need to have fail-safes. This helps in building trust and avoiding unexpected issues, keeping both humans and AI on the right track.

===========================


===== FINAL ARTICLE =====

# Welcome to the World of AI Safety

Have you ever wondered what it would be like to have your very own robot helping you around the house? Sounds like a dream, right? But let’s hit pause for a moment. What if this robot mistook your fluffy cat for a toy? That’s exactly where AI Safety comes in. Think of AI Safety as setting some friendly ground rules for your household helper, ensuring that it knows the difference between doing chores and causing a bit of chaos. It’s all about making sure our AI allies play by the rules, making life easier without those pesky accidental hiccups.

# Navigating the Maze of AI Challenges

Picture this: you've asked your trusty robot to grab you a cup of coffee. But instead, it sends mugs flying and spills coffee because it doesn’t quite get the concept of a mess. Frustrating, isn’t it? One of the biggest hurdles in AI Safety is aligning AI decisions with our human values and intentions. It’s like training a puppy not to gnaw on your favorite pair of shoes. Our job is to teach AI how to reach its goals without stepping on our toes, all while being as reliable and lovable as a well-trained pup.

# Steering AI Toward Safe Horizons

Now, how do we keep our AI friends on the straight and narrow? Imagine AI as a new driver learning to navigate the roads of life. Just like we teach new drivers the rules of the road and equip cars with brakes for safety, we provide AI with guidelines and fail-safes to prevent any unintended mishaps. Testing AI systems in various scenarios and keeping a watchful human eye on them ensures they don’t veer off track. It’s all about building trust and creating a partnership where both humans and AI are cruising smoothly together.

# Wrapping It Up

At the end of the day, AI Safety is about creating a harmonious relationship between humans and machines, where we trust our metal companions to support us without the fear of unexpected surprises. By setting boundaries and ensuring understanding, we’re not just building smarter machines—we’re crafting a future where AI and humanity can thrive together. So, next time you’re imagining that helpful robot assistant, rest easy knowing that AI Safety is making sure it's ready to lend a hand without dropping the ball—or your coffee mug!

========================


=== Workflow Completed ===

Topic: AI Safety
Outline Length: 96 characters
Draft Length: 1690 characters
Final Article Length: 2266 characters
```
