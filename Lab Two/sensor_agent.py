"""
DCIT403 Lab 2: Sensor Agent for Disaster Environment Perception
This script implements a SensorAgent that monitors environmental conditions
and detects disaster-related events with severity levels.
"""

import asyncio
import random
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import List


class DisasterType(Enum):
    """Types of disaster events that can be detected"""
    FLOODING = "Flooding"
    FIRE = "Fire"
    EARTHQUAKE = "Earthquake"
    LANDSLIDE = "Landslide"
    STORM = "Storm"
    NONE = "No Disaster"


class SeverityLevel(Enum):
    """Severity levels for detected disasters"""
    NONE = 0
    LOW = 1
    MODERATE = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class EnvironmentalPercept:
    """Represents a single environmental observation"""
    timestamp: str
    temperature: float
    humidity: float
    wind_speed: float
    rainfall: float
    seismic_activity: float
    disaster_type: DisasterType
    severity_level: SeverityLevel
    location: str
    description: str


class DisasterEnvironment:
    """Simulates a disaster-prone environment with changing conditions"""
    
    def __init__(self, location: str = "Urban Area"):
        self.location = location
        self.current_disaster = DisasterType.NONE
        self.disaster_duration = 0
        self.base_temperature = 25.0
        self.base_humidity = 60.0
        self.base_wind_speed = 5.0
        self.base_rainfall = 0.0
        self.base_seismic = 0.0
        
    def _generate_random_event(self) -> bool:
        """Randomly trigger a disaster event (15% chance)"""
        return random.random() < 0.15
    
    def _update_conditions(self) -> tuple:
        """Update environmental conditions based on current disaster"""
        
        # Base environmental variation
        temp = self.base_temperature + random.uniform(-3, 3)
        humidity = self.base_humidity + random.uniform(-10, 10)
        wind = self.base_wind_speed + random.uniform(-2, 2)
        rain = self.base_rainfall + random.uniform(-0.5, 0.5)
        seismic = self.base_seismic + random.uniform(-0.1, 0.1)
        
        # Apply disaster modifiers
        if self.current_disaster == DisasterType.FLOODING:
            rain = max(rain, 10.0 + random.uniform(0, 20))
            humidity = min(humidity + 30, 100)
        elif self.current_disaster == DisasterType.FIRE:
            temp = max(temp, 40.0 + random.uniform(0, 30))
            humidity = max(humidity - 40, 10)
            wind = max(wind, 15.0 + random.uniform(0, 15))
        elif self.current_disaster == DisasterType.EARTHQUAKE:
            seismic = max(seismic, 4.0 + random.uniform(0, 4))
        elif self.current_disaster == DisasterType.LANDSLIDE:
            rain = max(rain, 5.0)
            seismic = max(seismic, 2.0)
        elif self.current_disaster == DisasterType.STORM:
            wind = max(wind, 30.0 + random.uniform(0, 20))
            rain = max(rain, 5.0)
            humidity = min(humidity + 20, 100)
        
        # Ensure non-negative values
        temp = max(temp, -10)
        humidity = max(min(humidity, 100), 0)
        wind = max(wind, 0)
        rain = max(rain, 0)
        seismic = max(seismic, 0)
        
        return temp, humidity, wind, rain, seismic
    
    def get_percept(self) -> EnvironmentalPercept:
        """Generate environmental percept for sensor agent"""
        
        # Update disaster state
        if self._generate_random_event() and self.current_disaster == DisasterType.NONE:
            self.current_disaster = random.choice([d for d in DisasterType if d != DisasterType.NONE])
            self.disaster_duration = random.randint(3, 10)
        
        if self.disaster_duration > 0:
            self.disaster_duration -= 1
        elif self.current_disaster != DisasterType.NONE:
            self.current_disaster = DisasterType.NONE
        
        # Get environmental conditions
        temp, humidity, wind, rain, seismic = self._update_conditions()
        
        # Determine severity level
        severity = self._calculate_severity(temp, humidity, wind, rain, seismic)
        
        # Generate description
        description = self._generate_description(temp, humidity, wind, rain, seismic, severity)
        
        return EnvironmentalPercept(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            temperature=round(temp, 2),
            humidity=round(humidity, 2),
            wind_speed=round(wind, 2),
            rainfall=round(rain, 2),
            seismic_activity=round(seismic, 2),
            disaster_type=self.current_disaster,
            severity_level=severity,
            location=self.location,
            description=description
        )
    
    def _calculate_severity(self, temp: float, humidity: float, wind: float, 
                           rain: float, seismic: float) -> SeverityLevel:
        """Calculate disaster severity based on environmental factors"""
        
        if self.current_disaster == DisasterType.NONE:
            return SeverityLevel.NONE
        
        severity_score = 0
        
        if self.current_disaster == DisasterType.FLOODING:
            if rain > 20:
                severity_score += 3
            elif rain > 10:
                severity_score += 2
            elif rain > 5:
                severity_score += 1
        
        elif self.current_disaster == DisasterType.FIRE:
            if temp > 50:
                severity_score += 3
            elif temp > 40:
                severity_score += 2
            elif temp > 35:
                severity_score += 1
        
        elif self.current_disaster == DisasterType.EARTHQUAKE:
            if seismic > 7:
                severity_score += 3
            elif seismic > 5:
                severity_score += 2
            elif seismic > 3:
                severity_score += 1
        
        elif self.current_disaster == DisasterType.LANDSLIDE:
            if rain > 10 and seismic > 3:
                severity_score += 3
            elif rain > 5 or seismic > 2:
                severity_score += 2
            else:
                severity_score += 1
        
        elif self.current_disaster == DisasterType.STORM:
            if wind > 40:
                severity_score += 3
            elif wind > 25:
                severity_score += 2
            elif wind > 15:
                severity_score += 1
        
        if severity_score >= 3:
            return SeverityLevel.CRITICAL
        elif severity_score == 2:
            return SeverityLevel.HIGH
        elif severity_score == 1:
            return SeverityLevel.MODERATE
        else:
            return SeverityLevel.LOW
    
    def _generate_description(self, temp: float, humidity: float, wind: float, 
                             rain: float, seismic: float, severity: SeverityLevel) -> str:
        """Generate a descriptive message for the percept"""
        
        if self.current_disaster == DisasterType.NONE:
            return "Normal conditions - no disaster detected"
        
        severity_text = f"[{severity.name}]"
        
        if self.current_disaster == DisasterType.FLOODING:
            return f"{severity_text} Heavy rainfall detected: {rain:.1f}mm, Humidity: {humidity:.1f}%"
        elif self.current_disaster == DisasterType.FIRE:
            return f"{severity_text} Elevated temperature detected: {temp:.1f}°C, Wind: {wind:.1f}km/h"
        elif self.current_disaster == DisasterType.EARTHQUAKE:
            return f"{severity_text} Seismic activity detected: {seismic:.2f} magnitude"
        elif self.current_disaster == DisasterType.LANDSLIDE:
            return f"{severity_text} Landslide risk - Rainfall: {rain:.1f}mm, Seismic: {seismic:.2f}"
        elif self.current_disaster == DisasterType.STORM:
            return f"{severity_text} Storm conditions - Wind: {wind:.1f}km/h, Rain: {rain:.1f}mm"
        
        return "Unknown disaster type"


class SensorAgent:
    """Agent that perceives environmental conditions and logs disaster events"""
    
    def __init__(self, agent_id: str, location: str = "Urban Area", log_file: str = "event_logs.txt"):
        self.agent_id = agent_id
        self.location = location
        self.environment = DisasterEnvironment(location)
        self.log_file = log_file
        self.perceived_events: List[EnvironmentalPercept] = []
        self.active = False
        self._initialize_log()
    
    def _initialize_log(self):
        """Initialize the event log file"""
        with open(self.log_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("DISASTER ENVIRONMENT EVENT LOG\n")
            f.write(f"Agent ID: {self.agent_id}\n")
            f.write(f"Location: {self.location}\n")
            f.write(f"Log Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
    
    def _log_percept(self, percept: EnvironmentalPercept):
        """Log a perceived event to file"""
        with open(self.log_file, 'a') as f:
            f.write(f"Timestamp: {percept.timestamp}\n")
            f.write(f"Location: {percept.location}\n")
            f.write(f"Temperature: {percept.temperature}°C\n")
            f.write(f"Humidity: {percept.humidity}%\n")
            f.write(f"Wind Speed: {percept.wind_speed} km/h\n")
            f.write(f"Rainfall: {percept.rainfall} mm\n")
            f.write(f"Seismic Activity: {percept.seismic_activity} magnitude\n")
            f.write(f"Disaster Type: {percept.disaster_type.value}\n")
            f.write(f"Severity Level: {percept.severity_level.name}\n")
            f.write(f"Description: {percept.description}\n\n")
    
    def perceive(self) -> EnvironmentalPercept:
        """Perceive current environmental conditions"""
        percept = self.environment.get_percept()
        self.perceived_events.append(percept)
        self._log_percept(percept)
        return percept
    
    def print_percept(self, percept: EnvironmentalPercept):
        """Print perceived information to console"""
        if percept.severity_level != SeverityLevel.NONE:
            print(f"[SensorAgent] Disaster detected | Severity: {percept.severity_level.name}")
    
    async def start_monitoring(self, duration: int = 60, interval: int = 5):
        """Start periodic monitoring of environment"""
        self.active = True
        start_time = datetime.now()
        
        print(f"SensorAgent started and monitoring environment...")
        
        while self.active:
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed > duration:
                break
            
            percept = self.perceive()
            self.print_percept(percept)
            
            await asyncio.sleep(interval)
        
        self.active = False
        print(f"\nMonitoring complete. Total events logged: {len(self.perceived_events)}")
    
    def get_statistics(self) -> dict:
        """Generate statistics from perceived events"""
        if not self.perceived_events:
            return {}
        
        disasters_detected = {}
        severities = {level.name: 0 for level in SeverityLevel}
        
        for percept in self.perceived_events:
            disaster = percept.disaster_type.value
            disasters_detected[disaster] = disasters_detected.get(disaster, 0) + 1
            severities[percept.severity_level.name] += 1
        
        return {
            "total_percepts": len(self.perceived_events),
            "disasters_detected": disasters_detected,
            "severities": severities,
            "avg_temperature": sum(p.temperature for p in self.perceived_events) / len(self.perceived_events),
            "avg_humidity": sum(p.humidity for p in self.perceived_events) / len(self.perceived_events),
            "avg_wind_speed": sum(p.wind_speed for p in self.perceived_events) / len(self.perceived_events),
            "max_rainfall": max(p.rainfall for p in self.perceived_events),
            "max_seismic": max(p.seismic_activity for p in self.perceived_events)
        }


async def main():
    """Main execution function"""
    # Create sensor agent
    sensor_agent = SensorAgent(
        agent_id="SensorAgent_Alpha",
        location="Downtown Urban Area",
        log_file="Lab Two/event_logs.txt"
    )
    
    # Run monitoring cycle
    await sensor_agent.start_monitoring(duration=30, interval=3)


if __name__ == "__main__":
    asyncio.run(main())
