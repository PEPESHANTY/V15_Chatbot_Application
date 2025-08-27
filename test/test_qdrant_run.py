from graphs.qdrant_graph import build_qdrant_graph

if __name__ == "__main__":
    app = build_qdrant_graph()

    print("✅ Qdrant vector agent is ready!")

    while True:
        query = input("\n❓ Ask your rice question (or type 'exit'): ").strip()
        if query.lower() in ["exit", "quit"]:
            break

        inputs = {"messages": [("user", query)]}
        for event in app.stream(inputs):
            for key, value in event.items():
                if value is None:
                    continue
                last_msg = value.get("messages", [])[-1]
                print(f"\n🔹 Output from node '{key}':")
                print(last_msg.content)
