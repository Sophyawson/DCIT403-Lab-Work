#!/usr/bin/env python3
"""Lab 1 - Basic Agent with Demo Output"""

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
    container = Container()
    agent = BasicAgent("agent_nhyira@localhost", "2703")
    agent.container = container
    
    # Run locally without XMPP
    agent.is_alive_flag = True
    await agent.setup()
    
    # Simulate agent behavior
    counter = 0
    while counter < 3:  # Show 3 cycles of agent output
        print("Hello! I am alive and running as an agent.")
        await asyncio.sleep(5)
        counter += 1
    
    agent.is_alive_flag = False


if __name__ == "__main__":
    asyncio.run(main())
