import httpx

from langchain_core.tools import tool
from langchain_core.tools import ToolException

from app.schema.product_schema import CreateProductRequest
from app.service.product_service import create_product


def create_product_tools(client: httpx.AsyncClient, access_token: str):

    @tool(args_schema=CreateProductRequest)
    async def create_product_tool(
        name: str,
        price: float,
        description: str,
        stock_quantity: int,
        category_id: int,
        image_url: str
    ):
        """
        Create a new product in the Swift Cart catalogue.

        Use this tool when an authorized user explicitly requests
        the creation of a new product.

        Required information:
        - Product name
        - Price
        - Description
        - Stock quantity
        - Category ID
        - Image URL
        """

        request = CreateProductRequest(
            name=name,
            price=price,
            description=description,
            stock_quantity=stock_quantity,
            category_id=category_id,
            image_url=image_url
        )

        try:
            response = await create_product(
                request=request,
                access_token=access_token,
                client=client
            )

            return {
                "success": True,
                "message": "Product created successfully.",
                "product": response
            }

        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code

            if status_code == 401:
                raise ToolException(
                    "Authentication failed. Please sign in again."
                )

            if status_code == 403:
                raise ToolException(
                    "You do not have permission to create products."
                )

            if 400 <= status_code < 500:
                raise ToolException(
                    "The backend rejected the product details. "
                    "Please verify the supplied information."
                )

            raise ToolException(
                "The product could not be created because of a backend error."
            )

        except httpx.RequestError:
            raise ToolException(
                "Unable to connect to the Swift Cart backend. "
                "Please try again later."
            )

    return [create_product_tool]