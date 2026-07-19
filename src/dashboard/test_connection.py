from utils.db import get_engine

try:
    engine = get_engine()

    with engine.connect():
        print("✅ Database Connected Successfully!")

except Exception as e:
    print("❌ Connection Failed")
    print(e)