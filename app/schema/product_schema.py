from pydantic import BaseModel, ConfigDict, Field

class CreateProductRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(
        min_length=2,
        description="Name of the product"
    )
    description: str = Field(
        min_length=5,
        description="Detailed product description"
    )
    price: float = Field(
        gt=0.0,
        description="Selling price of the product"
    )
    stock_quantity: int = Field(
        ge=0,
        serialization_alias="stockQuantity",
        description="Available inventory count (0 or more)",
    )
    category_id: int = Field(
        gt=0,
        serialization_alias="categoryId",
        description="Numeric ID of the target product category",
    )
    image_url: str | None = Field(
        min_length=8,
        serialization_alias="imageUrl",
        description="Optional valid HTTP/HTTPS image URL for the product",
    )