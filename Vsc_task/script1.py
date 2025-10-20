from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional
import uuid

# =============================================================================
# 1. ISP - Separate interfaces for different responsibilities
# =============================================================================

class IBikeRepository(ABC):
    """Interface for bike data access"""
    @abstractmethod
    def save(self, bike: 'Bike') -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, bike_id: str) -> Optional['Bike']:
        pass
    
    @abstractmethod
    def find_all(self) -> List['Bike']:
        pass
    
    @abstractmethod
    def delete(self, bike_id: str) -> bool:
        pass

class IBikeService(ABC):
    """Interface for business logic"""
    @abstractmethod
    def add_bike(self, bike_data: Dict) -> str:
        pass
    
    @abstractmethod
    def rent_bike(self, bike_id: str, customer_id: str) -> bool:
        pass
    
    @abstractmethod
    def return_bike(self, bike_id: str) -> bool:
        pass

class INotificationService(ABC):
    """Interface for notifications"""
    @abstractmethod
    def send_rental_notification(self, customer_id: str, bike_id: str) -> None:
        pass

# =============================================================================
# 2. DIP - Depend on abstractions, not concretions
# =============================================================================

class BikeRepository(IBikeRepository):
    """Concrete implementation - Single Responsibility: Data access only"""
    
    def __init__(self):
        self._bikes: Dict[str, 'Bike'] = {}
    
    def save(self, bike: 'Bike') -> None:
        self._bikes[bike.id] = bike
    
    def find_by_id(self, bike_id: str) -> Optional['Bike']:
        return self._bikes.get(bike_id)
    
    def find_all(self) -> List['Bike']:
        return list(self._bikes.values())
    
    def delete(self, bike_id: str) -> bool:
        return self._bikes.pop(bike_id, None) is not None

class EmailNotificationService(INotificationService):
    """SRP: Only handles email notifications"""
    
    def send_rental_notification(self, customer_id: str, bike_id: str) -> None:
        print(f"📧 Email sent to customer {customer_id}: Bike {bike_id} rented!")

class SMSNotificationService(INotificationService):
    """SRP: Only handles SMS notifications"""
    
    def send_rental_notification(self, customer_id: str, bike_id: str) -> None:
        print(f"📱 SMS sent to customer {customer_id}: Bike {bike_id} rented!")

# =============================================================================
# 3. OCP - Open for extension via inheritance/polymorphism
# =============================================================================

class BikeStatus:
    AVAILABLE = "available"
    RENTED = "rented"
    MAINTENANCE = "maintenance"

class Bike(ABC):
    """Base class for all bikes - LSP ready"""
    
    def __init__(self, model: str, price_per_hour: float):
        self.id = str(uuid.uuid4())
        self.model = model
        self.price_per_hour = price_per_hour
        self.status = BikeStatus.AVAILABLE
        self.rental_start_time = None
    
    @abstractmethod
    def get_description(self) -> str:
        pass
    
    def is_available(self) -> bool:
        return self.status == BikeStatus.AVAILABLE
    
    def rent(self, start_time: datetime) -> bool:
        if self.is_available():
            self.status = BikeStatus.RENTED
            self.rental_start_time = start_time
            return True
        return False
    
    def return_bike(self) -> float:
        if self.status == BikeStatus.RENTED and self.rental_start_time:
            hours_rented = (datetime.now() - self.rental_start_time).total_seconds() / 3600
            cost = hours_rented * self.price_per_hour
            self.status = BikeStatus.AVAILABLE
            self.rental_start_time = None
            return cost
        return 0.0

# LSP: Subclasses can replace base class
class MountainBike(Bike):
    """OCP: Extend without modifying base Bike class"""
    
    def get_description(self) -> str:
        return f"Mountain Bike: {self.model} (${self.price_per_hour}/hr)"

class RoadBike(Bike):
    """OCP: New bike type without modifying existing code"""
    
    def get_description(self) -> str:
        return f"Road Bike: {self.model} (${self.price_per_hour}/hr)"

class ElectricBike(Bike):
    """OCP: Easy to add new bike types"""
    
    def __init__(self, model: str, price_per_hour: float, battery_capacity: float):
        super().__init__(model, price_per_hour)
        self.battery_capacity = battery_capacity
    
    def get_description(self) -> str:
        return f"Electric Bike: {self.model} (${self.price_per_hour}/hr, {self.battery_capacity}Wh)"

# =============================================================================
# 4. SRP + DIP - Business logic separated and injected
# =============================================================================

class BikeRentalService(IBikeService):
    """Single Responsibility: Business logic only"""
    
    def __init__(self, 
                 repository: IBikeRepository, 
                 notification_service: INotificationService):
        # DIP: Depend on abstractions
        self.repository = repository
        self.notification_service = notification_service
    
    def add_bike(self, bike_data: Dict) -> str:
        """Factory pattern for OCP"""
        bike_type = bike_data.get('type', 'mountain')
        
        if bike_type == 'mountain':
            bike = MountainBike(bike_data['model'], bike_data['price_per_hour'])
        elif bike_type == 'road':
            bike = RoadBike(bike_data['model'], bike_data['price_per_hour'])
        elif bike_type == 'electric':
            bike = ElectricBike(
                bike_data['model'], 
                bike_data['price_per_hour'], 
                bike_data['battery_capacity']
            )
        else:
            raise ValueError(f"Unknown bike type: {bike_type}")
        
        self.repository.save(bike)
        return bike.id
    
    def rent_bike(self, bike_id: str, customer_id: str) -> bool:
        bike = self.repository.find_by_id(bike_id)
        if bike and bike.rent(datetime.now()):
            self.notification_service.send_rental_notification(customer_id, bike_id)
            self.repository.save(bike)
            return True
        return False
    
    def return_bike(self, bike_id: str) -> bool:
        bike = self.repository.find_by_id(bike_id)
        if bike:
            cost = bike.return_bike()
            self.repository.save(bike)
            print(f"💰 Return cost: ${cost:.2f}")
            return True
        return False

# =============================================================================
# 5. Usage Example - All SOLID principles working together
# =============================================================================

def main():
    # DIP: Inject dependencies
    repo = BikeRepository()
    email_notifier = EmailNotificationService()
    service = BikeRentalService(repo, email_notifier)
    
    # Add bikes (OCP - easy to extend new types)
    bikes_data = [
        {'type': 'mountain', 'model': 'Trek Marlin', 'price_per_hour': 10.0},
        {'type': 'road', 'model': 'Specialized Allez', 'price_per_hour': 12.0},
        {'type': 'electric', 'model': 'Rad Power', 'price_per_hour': 15.0, 'battery_capacity': 500},
        {'type': 'water bike', 'model': 'Ris Power', 'price_per_hour': 30.0, 'battery_capacity': 300},
    ]
    
    bike_ids = []
    for data in bikes_data:
        bike_id = service.add_bike(data)
        bike_ids.append(bike_id)
        print(f"➕ Added: {repo.find_by_id(bike_id).get_description()}")
    
    # Rent bikes (SRP - service handles business logic)
    print("\n🚴 Renting bikes...")
    service.rent_bike(bike_ids[0], "customer_123")
    service.rent_bike(bike_ids[1], "customer_456")
    
    # List available bikes
    print("\n📋 Available bikes:")
    available_bikes = [bike for bike in repo.find_all() if bike.is_available()]
    for bike in available_bikes:
        print(f"  - {bike.get_description()}")
    
    # Return bike
    print("\n🔄 Returning bike...")
    service.return_bike(bike_ids[0])
    
    # Switch notification service (DIP + ISP)
    print("\n📱 Switching to SMS notifications...")
    sms_service = BikeRentalService(repo, SMSNotificationService())
    sms_service.rent_bike(bike_ids[0], "customer_789")

if __name__ == "__main__":
    main()