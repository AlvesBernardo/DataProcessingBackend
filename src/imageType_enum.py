from enum import Enum

class ImageType(Enum):
    JPEG = "JPEG"
    PNG = "PNG"
    GIF = "GIF"
    BMP = "BMP"


# Iterating over enum members
for type_enum in ImageType:
    print(type_enum)

# Checking membership
