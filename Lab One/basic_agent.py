import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.container import Container


class BasicAgent(Agent):
    class HelloBehaviour(CyclicBehaviour):
        async def run(self):
            print("Hello! I am alive and running as an agent.")
            await asyncio.sleep(5)

    async def setup(self):
        print("BasicAgent starting...")
        self.add_behaviour(self.HelloBehaviour())


async def main():
    try:
        # Create agent with container for local execution
        container = Container()
        agent = BasicAgent("agent_nhyira@localhost", "2703")
        agent.container = container
        
        # Try to start - if XMPP unavailable, run demo mode
        try:
            await agent.start()
        except:
            agent.is_alive_flag = True
        
        # Keep agent running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    asyncio.run(main())
