import asyncio
from app.db.neo4j_client import get_neo4j_client

async def check():
    db = get_neo4j_client()
    async with db.driver.session() as session:
        # Check nodes
        nodes = await session.run("MATCH (n:Concept) RETURN count(n) as count")
        node_count = (await nodes.single())["count"]
        print(f"Nodes: {node_count}")
        
        # Check edges
        edges = await session.run("MATCH ()-[r:RELATED_TO]->() RETURN count(r) as count")
        edge_count = (await edges.single())["count"]
        print(f"Edges: {edge_count}")
        
        # Show some edges
        sample = await session.run("MATCH (a)-[r:RELATED_TO]->(b) RETURN a.name as source, b.name as target LIMIT 5")
        for record in await sample.data():
            print(f"  {record['source']} -> {record['target']}")
    await db.close()

if __name__ == "__main__":
    asyncio.run(check())
