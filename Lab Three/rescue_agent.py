import asyncio
import random
from pathlib import Path
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.container import run_container

# Log file path
LOG_PATH = Path(__file__).parent / "execution_trace.txt"


def log(msg: str):
    print(msg, flush=True)
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception as e:
        print(f"Failed to write log: {e}", flush=True)


class IdleState(State):
    async def run(self):
        log("State: IDLE - monitoring disaster environment")
        await asyncio.sleep(1)

        # Choose disaster type
        disaster = random.choice(["Flood", "Fire"])

        # Choose severity
        severity = random.choice(["Low", "Medium", "High", "Critical"])

        log(f"Detected Disaster: {disaster}")
        log(f"Severity Level: {severity}")

        # Store disaster info inside agent memory
        self.agent.current_disaster = disaster
        self.agent.current_severity = severity

        if severity in ["High", "Critical"]:
            self.set_next_state("RESCUING")
        else:
            log("Severity not critical. Continuing monitoring.")
            self.set_next_state("IDLE")


class RescuingState(State):
    async def run(self):
        disaster = self.agent.current_disaster

        log(f"State: RESCUING - Responding to {disaster}")

        if disaster == "Flood":
            log("Deploying rescue boats and evacuation teams...")
        elif disaster == "Fire":
            log("Dispatching fire trucks and emergency responders...")

        await asyncio.sleep(2)

        log("Rescue operation completed.")
        self.set_next_state("COMPLETED")


class CompletedState(State):
    async def run(self):
        log("State: COMPLETED - Mission finalized")
        await asyncio.sleep(0.5)
        self.set_next_state("IDLE")


class DisasterResponseAgent(Agent):
    async def setup(self):
        log("DisasterResponseAgent starting...")

        # Initialize memory
        self.current_disaster = None
        self.current_severity = None

        fsm = FSMBehaviour()

        fsm.add_state(name="IDLE", state=IdleState(), initial=True)
        fsm.add_state(name="RESCUING", state=RescuingState())
        fsm.add_state(name="COMPLETED", state=CompletedState())

        fsm.add_transition(source="IDLE", dest="RESCUING")
        fsm.add_transition(source="IDLE", dest="IDLE")
        fsm.add_transition(source="RESCUING", dest="COMPLETED")
        fsm.add_transition(source="COMPLETED", dest="IDLE")

        self.add_behaviour(fsm)


async def main():
    agent = DisasterResponseAgent("disaster@localhost", "password")
    await agent.start(auto_register=True)
    await asyncio.sleep(12)
    await agent.stop()


if __name__ == "__main__":
    run_container(main(), embedded_xmpp_server=True)