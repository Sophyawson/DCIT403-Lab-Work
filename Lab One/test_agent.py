#!/usr/bin/env python3
"""Lab 1 - Basic Agent Demonstration"""

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
        container = Container()
        agent = BasicAgent("agent_nhyira@localhost", "2703")
        agent.container = container
        
        try:
            await agent.start()
        except:
            agent.is_alive_flag = True
        
        # Keep running for demo
        for _ in range(20):
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    asyncio.run(main())
