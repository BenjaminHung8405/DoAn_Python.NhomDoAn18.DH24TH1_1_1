from Database.Database import execute_query
from Database.HomePagedata import get_data

print("=" * 50)
print("DATABASE CONNECTION TEST")
print("=" * 50)

# Test 1: Connection
print("\n[1] Testing database connection...")
result = execute_query("SELECT COUNT(*) FROM artists")
if result:
    print(f"   ✓ Connected! Total artists: {result[0][0]}")
else:
    print("   ✗ Connection failed")

# Test 2: Tables
print("\n[2] Checking tables...")
tables = ['artists', 'albums', 'tracks', 'genres', 'languages', 'users']
for table in tables:
    result = execute_query(f"SELECT COUNT(*) FROM {table}")
    if result:
        print(f"   ✓ {table}: {result[0][0]} records")

# Test 3: HomePage data
print("\n[3] Testing HomePage data...")
data = get_data()
print(f"   ✓ Got {len(data)} sections")
for section in data:
    print(f"      - {section['name']}: {len(section['data'])} items")

print("\n" + "=" * 50)
print("TEST COMPLETED")
print("=" * 50)