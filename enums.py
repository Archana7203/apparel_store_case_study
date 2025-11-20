import enum

class GenderEnum(enum.Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

class ActiveStatusEnum(enum.Enum):
    Active = "Active"
    Inactive = "Inactive"

class AddressTypeEnum(enum.Enum):
    Office = "Office"
    Home = "Home"
    Other = "Other"

class EmploymentEnum(enum.Enum):
    Employed = "Employed"
    Unemployed = "Unemployed"
    Student = "Student"
    Retired = "Retired"
    Other = "Other"

class ProductGenderEnum(enum.Enum):
    Men = "Men"
    Women = "Women"
    Unisex = "Unisex"
    Other = "Other"

class OccasionEnum(enum.Enum):
    Office = "Office"
    DailyWear = "DailyWear"
    Travel = "Travel"
    Festival = "Festival"

class StyleEnum(enum.Enum):
    Casual = "Casual"
    Formal = "Formal"

class SeasonEnum(enum.Enum):
    Summer = "Summer"
    Winter = "Winter"