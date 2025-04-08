from flow import qa_flow

# Example main function
# Please replace this with your own main function
def main():
    shared = {
        "question": "In one sentence, what's the end of universe?",
        "answer": None
    }

    qa_flow.run(shared)
    print("Question:", shared["question"])
    print("Answer:", shared["answer"])

if __name__ == "__main__":
    main()